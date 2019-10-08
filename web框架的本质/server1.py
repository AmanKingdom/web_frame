import socket

"""

关于请求内容：

如果用户的 GET 请求如果带有明文参数，比如 localhost:8080/index?p=123，那么在接收到的数据中，请求头的第一行则为：

    GET /index?p=123 HTTP/1.1

如果是 POST 请求，数据则不在这，而是在\r\n\r\n后的数据体内

关于响应内容（可以在浏览器查看 Response Headers）：

响应体则是浏览器页面上看到的东西，本质就是字符串，只是浏览器解析后变漂亮了

在下面程序中，conn.send()的发送内容就是响应内容，
如果要按照HTTP协议规范则不能只是随便发一些字节就可以了，还要有各种附加信息，比如发送响应头：

conn.send(b"HTTP/1.1 200 OK\r\n\r\n")

"""


socket_server = socket.socket()
socket_server.bind(('localhost', 8080))
socket_server.listen(5)


if __name__ == '__main__':
    while True:
        conn, addr = socket_server.accept()
        data = conn.recv(2048)
        print('接收到客户端的请求信息：', data, '\n类型为：', type(data))
        print('转为字符串：\n', str(data, encoding='utf-8'))
        # conn.send(b"HTTP/1.1 200 OK\r\n\r\n")     # 发送响应头
        conn.send(b'abcd')
        conn.close()
