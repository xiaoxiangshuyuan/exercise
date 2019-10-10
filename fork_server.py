from socket import *
import os
import sys
import signal

# 创建监听套接字
HOST = '0.0.0.0'
PORT = 8888
ADDR = (HOST, PORT)


def client_handle(connfd):
    while True:
        data = connfd.recv(1024)
        if not data:
            break
        print(data.decode())
        connfd.send(b'OK')

s = socket()
s.setsockopt(SOL_SOCKET, SO_REUSEADDR, True)
s.bind(ADDR)
s.listen(5)

# 处理僵尸进程
signal.signal(signal.SIGCHLD, signal.SIG_IGN)

# 接收客户端连接
while True:
    try:
        c, addr = s.accept()
    except KeyboardInterrupt:
        sys.exit("服务器退出")
    except Exception as e:
        print(e)
        continue

    # 创建子进程处理客户端请求
    pid = os.fork()

    if pid == 0:
        s.close()
        client_handle(c)  # 处理请求
        sys.exit(0)
    else:
        c.close()