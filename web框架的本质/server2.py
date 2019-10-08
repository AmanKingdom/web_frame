import socket

"""

更进一步，将获取到的请求信息切分解析

然后根据用户请求的url判断请求的内容并返回相应内容

"""


# 视图函数：（记得视图函数的使命：接收分析用户想要做些什么并返回处理的结果，所以要传入请求内容）

def views1(request):
    """
    处理用户请求、返回响应信息，返回静态页面
    :param request: 用户请求的所有信息
    :return:想要返回html页面，可以从文件获取
    """

    with open('login.html', 'rb') as f:
        return_data = f.read()

    return return_data


def views2(request):
    """
    如果返回动态数据呢？没错，这就是模板语言，返回动态页面，仅包含一段时间
    :param request:
    :return:
    """
    with open('login.html', 'r', encoding='utf-8') as f:
        return_data = f.read()

    import time
    now_time = time.time()
    return_data = return_data.replace('{{ xxx }}', str(now_time))

    return bytes(return_data, encoding='utf-8')


def get_user_data():
    def exists_table(cursor, table_name):
        """
        判断cursor所指的数据库中是否存在某张表
        :param cursor: 传入conn.cursor()
        :param table_name:传入表名的字符串即可
        :return:
        """
        cursor.execute("show tables")
        for item in cursor.fetchall():
            if table_name == item[0]:
                return True
        return False

    import MySQLdb

    db_conn = MySQLdb.connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='dgut520!',
        db='web_test_database',
    )

    cur = db_conn.cursor()

    if not exists_table(cur, 'user'):
        cur.execute("create table user(id INT , name VARCHAR (20), password VARCHAR (20))")

    # 添加数据的两种方式
    cur.execute("insert into user values('1', 'aaa', '123456')")

    sql_many = "insert into user values (%s,%s,%s)"
    cur.executemany(sql_many, [
        ('2', 'bbb', '123456'),
        ('3', 'ccc', '123456'),
    ])

    cur.execute("select id, name, password from user")
    return_data = cur.fetchall()
    cur.close()
    db_conn.autocommit(on=True)
    db_conn.close()
    return return_data


def views3(request):
    """
    返回动态页面。从数据库取出放入模板再返回
    :param request:
    :return:
    """
    with open('views3.html', 'r', encoding='utf-8') as f:
        html = f.read()

    table_data = get_user_data()
    tbody = ''
    for row in table_data:
        tbody = tbody + '<tr><td>%d</td><td>%s</td><td>%s</td></tr>' % row
    html = html.replace('{{ tbody }}', tbody)

    return bytes(html, encoding='utf-8')


def views4(requests):
    """
    使用第三方模板引擎jinja2渲染网页返回
    :param requests:
    :return:
    """
    with open('views4.html', 'r', encoding='utf-8') as f:
        html = f.read()

    table_data = get_user_data()

    from jinja2 import Template
    template = Template(html)
    return_data = template.render({'users': table_data})
    return bytes(return_data, encoding='utf-8')


# 路由：
urlpatterns = [
    ('/views1', views1),
    ('/views2', views2),
    ('/views3', views3),
    ('/views4', views4),
]

if __name__ == '__main__':
    socket_server = socket.socket()
    socket_server.bind(('localhost', 8080))
    socket_server.listen(5)

    while True:
        conn, addr = socket_server.accept()
        data = conn.recv(2048)

        data = str(data, encoding='utf-8')
        print(data)
        headers, bodys = data.split('\r\n\r\n')

        temp_list = headers.split('\r\n')
        # 对首行做解析，url 就是用户请求时的url
        method, url, protocal = temp_list[0].split(' ')  # 对应 GET /index?p=123 HTTP/1.1

        views_func = None
        for item in urlpatterns:
            if item[0] == url:
                views_func = item[1]
                break

        if views_func:
            response = views_func(data)
        else:
            response = b'404 Not Found'

        conn.send(b"HTTP/1.1 200 OK\r\n\r\n")  # 发送响应头
        conn.send(response)
        conn.close()
