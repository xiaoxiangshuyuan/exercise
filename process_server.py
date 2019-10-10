from socket import *
from multiprocessing import Process
import sys
import signal

HOST = '0.0.0.0'
PORT = 8888
ADDR = (HOST,PORT)

def handle(connfd):
    print("Connect from ",connfd.getpeername())
    while True:
        data = c.recv(1024)
        if not data:
            break
        print(data.decode())
        c.send(b'OK')
    c.close()
    sys.exit(0)

# 创建监听套接字
s = socket()
s.setsockopt(SOL_SOCKET,SO_REUSEADDR,True)
s.bind(ADDR)
s.listen(3)

signal.signal(signal.SIGCHLD,signal.SIG_IGN)

# 循环等待客户端连接
while True:
    try:
        c,addr = s.accept()
    except KeyboardInterrupt:
        s.close()
        break
    except Exception as e:
        print(e)
        continue

    # 创建进程
    p = Process(target=handle,args=(c,))
    p.daemon = True # 进程退出分支线程退出
    p.start()

