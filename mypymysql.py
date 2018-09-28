import pymysql


class Mypymysql(object):
	def __init__(self):
		self.do_create()

	def do_create(self):
		self.db = pymysql.connect(
							host = '127.0.0.1',
							user = 'root',
							password = '123456',
							database = 'dict',
							charset = 'utf8'
							)
		self.cur = self.db.cursor()
		

	def close(self):
		self.cur.close()
		self.db.close()
	def myupdate(self):
		pass
	# 接受两个参数 table:表名 L:插入内容列表
	# 插入成功/失败返回布尔值
	def myinsert(self,table,L):

		if table == 'record':
			sql_insert = 'insert into record (name,word) values(%s,%s);'
		elif table == 'users':
			sql_insert = 'insert into users (name,password) values(%s,%s);'
		elif table == 'words':
			sql_insert = 'insert into words (word,gloze) values(%s,%s);'
		try:
			self.cur.execute(sql_insert,L)
			self.db.commit()
			return True
		except Exception as e:
			self.db.rollback()
			return False

	# 接受两个参数 table:表名 s:姓名或单词
	# users表返回密码
	# words表返回解释
	# record表返回所有记录
	# 所有返回结果均以元祖嵌套方式返回 如 (('123456'),)
	def myselect(self,table,s):
		if table == 'record':
			sql_insert = 'select * from record where name=%s;'
		elif table == 'users':
			sql_insert = 'select password from users where name=%s;'
		elif table == 'words':
			sql_insert = 'select gloze from words where word=%s;'
		
		self.cur.execute(sql_insert,s)
		return self.cur.fetchall()



# 测试
if __name__ == '__main__':
	m = Mypymysql()
	l = m.myselect('record','leon')
	s = ''
        # 最新十条记录
        for i in l[-1:-11:-1]:
            for j in i:
                line = 'name: '+j[0]+\
                       '   word: '+j[1]+\
                       '   time: '+str(j[2])+'#'
                s += line
	m.myselect('words','world')