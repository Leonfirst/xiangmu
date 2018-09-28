from socket import *
import sys
from time import sleep
import getpass




HOST = sys.argv[1]
PORT = int(sys.argv[2])
ADDR = (HOST,PORT)


class Myclient(object):
	def __init__(self,ADDR):
		self.ADDR = ADDR

		self.create_socket()
		self.first_interface()

	def create_socket(self):
		self.socked = socket()
		self.socked.connect(self.ADDR)
	# 登录
	def do_login(self):
		name = input('用户名:')
		password = getpass.getpass('密码:')
		s = 'login#%s#%s'%(name,password)
		self.socked.send(s.encode())
		data = self.socked.recv(1024).decode()
		print('lll')
		if data == '登录成功':
			# 进入二级页面
			self.second_interface()
		else:
			print(data)
	# 注册
	def enroll(self):
		while True:
			name = input('用户名(#退出注册):')
			if name == '#':
				break
			password = input('密码:')
			if password != input('确认密码:'):
				print('密码不一致')
				continue
			s = 'enroll#%s#%s'%(name,password)
			self.socked.send(s.encode())
			data = self.socked.recv(1024).decode()
			print(data)
			if data == '注册成功':
				break

	# 查单词
	def query_word(self):
		self.socked.send(b'word')
		while True:
			word = input('单词(#退出):')
			if word == '#':
				self.socked.send(b'end')
				break
			self.socked.send(word.encode())
			gloze = self.socked.recv(1024).decode()
			print('解释:',gloze)

	# 查看历史记录
	def query_histories(self):
		self.socked.send(b'histories')
		data = self.socked.recv(2048).decode()
		L = data.split('#')
		for line in L:
			print(line)

		# 如果记录满十条提示可以查询更多
		if len(L) == 11:
			a = input('1.查询更多记录\
					   \n2.退出记录查询')
			if a == '1':
				self.socked.send(b'more')
				data = self.socked.recv(4096).decode()
				L = data.split('#')
				for line in L:
					print(line)
				return
		self.socked.send(b'no')





	# 第一界面
	def first_interface(self):
		while True:
			a = input('''
				=========Welcome========
				--1.登录  2.注册  3.退出--
				========================
				''')
			if a == '1':
				self.do_login()
			elif a == '2':
				self.enroll()
			elif a == '3':
				self.socked.close()
				sys.exit('客户端退出')


	def second_interface(self):
		while True:
			a = input('''
				+==========++++++==========+
				--1.查单词  2.历史记录  3.退出--
				============================
				''')
			if a == '1':
				self.query_word()
			elif a == '2':
				self.query_histories()
			elif a == '3':
				self.first_interface()


if __name__ == '__main__':
	m = Myclient(ADDR)
	m.first_interface()