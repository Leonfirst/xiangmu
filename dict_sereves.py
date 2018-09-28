from socket import *
import os
import sys
import traceback
import signal 
from mypymysql import Mypymysql

class Mysercer(object):
    def __init__(self):
        self.mysql = Mypymysql()
    # 登录
    def do_login(self,name,password):
        p = self.mysql.myselect('users',name)
        if p:
            if p[0][0] == password:
                self.connfd.send('登录成功'.encode())
                # 记录此进程用户名
                self.user = name
            else:
                self.connfd.send('密码错误'.encode())
        else:
            self.connfd.send('账号不存在'.encode())
    
    # 注册
    def do_enroll(self,name,password):
        b = self.mysql.myinsert('users',[name,password])
        if b:
            self.connfd.send('注册成功'.encode())
        else:
            self.connfd.send('用户名已使用'.encode())
    # 查单词
    def query_word(self):
        while True:
            data = self.connfd.recv(1024).decode()
            if data == 'end':
                break
            gloze = self.mysql.myselect('words',data)
            if gloze:
                self.connfd.send(gloze[0][0].encode())
                # 把单词加入到历史记录
                self.mysql.myinsert('record',[self.user,data])
            else:
                self.connfd.send('单词不存在'.encode())
    # 查历史记录
    def query_histories(self):
        l = self.mysql.myselect('record',self.user)
        if not l:
            self.connfd.send(b'no histories')
        s = ''
        # 最新十条记录
        for j in l[-1:-11:-1]:
            line = 'name: '+j[0]+\
                   '   word: '+j[1]+\
                   '   time: '+str(j[2])+'#'
            s += line
        self.connfd.send(s.encode())
        # 等待查询更多或退出
        w = connfd.recv(1024).decode()
        if w =='more':
            s = ''
            for j in l[-11::-1]:
                line = 'name: '+j[0]+\
                       '   word: '+j[1]+\
                       '   time: '+str(j[2])+'#'
                s += line
            self.connfd.send(s.encode())




    # 处理客户端请求主程序
    def client_handler(self,connfd):
        self.connfd = connfd
        while True:
            data = connfd.recv(1024).decode()
            if not data:break
            L = data.split('#')
            print(L)
            if L[0] == 'login':
                self.do_login(L[1],L[2])
            elif L[0] == 'enroll':
                self.do_enroll(L[1],L[2])
            elif L[0] == 'word':
                self.query_word()
            elif L[0] == 'histories':
                self.query_histories()

        self.connfd.close()
        sys.exit('客户端退出')






HOST = '0.0.0.0'
PORT = 7650
ADDR = (HOST,PORT)

print('socket 套接字被创建')
socked = socket()
socked.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
socked.bind(ADDR)
socked.listen(5)

#忽略子进程信号
signal.signal(signal.SIGCHLD,signal.SIG_IGN)

m = Mysercer()

while True:
    try:
        connfd,addr = socked.accept()
        print(addr,'连入')
    except KeyboardInterrupt:
        socked.close()
        sys.exit('服务器退出')
    except Exception:
        traceback.print_exc()
        continue

    pid = os.fork()

    if pid == 0:
        print('创建紫禁城')
        socked.close()
        
        m.client_handler(connfd)
    else:
    	connfd.close()
    	continue