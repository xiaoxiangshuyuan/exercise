from socket import * 
import sys 
import time

# 服务器地址
ADDR = ('127.0.0.1',8888)

# 具体功能
class FtpClient(object):
    def __init__(self,sockfd):
        self.sockfd = sockfd
    
    def do_list(self):
        self.sockfd.send(b'L') # 发送请求
        # 等待回复
        data = self.sockfd.recv(128).decode()
        if data == 'OK':
            data = self.sockfd.recv(4096).decode()
            files = data.split('#')
            for file in files:
                print(file)
        else:
            # 无法完成
            print(data)
    
    def do_quit(self):
        self.sockfd.send(b'Q')
        self.sockfd.close()
        sys.exit("谢谢使用")

    def do_get(self,filename):
        self.sockfd.send(("G "+filename).encode())
        data = self.sockfd.recv(128).decode()
        if data == 'OK':
            fd = open(filename,'wb')
            while True:
                data = self.sockfd.recv(1024)
                if data == b'##':
                    break 
                fd.write(data)
            fd.close()
        else:
            print(data)

    def do_put(self,filename):
        try:
            f = open(filename,'rb')
        except IOError:
            print('没有该文件')
            return 
        # 获取文件名称去除可能的路径
        filename = filename.split('/')[-1]
        self.sockfd.send(('P '+filename).encode())
        data = self.sockfd.recv(128).decode()
        if data == 'OK':
            while True:
                data = f.read(1024)
                if not data:
                    time.sleep(0.1)
                    self.sockfd.send(b'##')
                    break
                self.sockfd.send(data)
            f.close()
        else:
            print(data)

# 网络连接
def main():
    sockfd = socket()

    try:
        sockfd.connect(ADDR)
    except Exception as e:
        print("连接失败",e)
        return 

    ftp = FtpClient(sockfd)

    while True:
        print("\n========命令选项==========")
        print("***       list       ***")
        print("***     get file     ***")
        print("***     put file     ***")
        print("***       quit       ***")
        print("===========================")
    
        cmd = input("输入命令>>")
        if cmd.strip() == 'list':
            ftp.do_list()
        elif cmd.strip() == 'quit':
            ftp.do_quit()
        elif cmd[:3] == 'get':
            filename = cmd.split(' ')[-1]
            ftp.do_get(filename)
        elif cmd[:3] == 'put':
            filename = cmd.split(' ')[-1]
            ftp.do_put(filename)



main()

