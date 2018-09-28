from mypymysql import Mypymysql
import re


def main():
	a = 0
	b = 0
	c = 0
	m = Mypymysql()
	with open('./dict.txt') as f:
		for data in f:

			if data == '\n':
				break
			word = re.match(r'\S+',data).group()
			# 记录word最长长度
			if a < len(word):a=len(word)
			gloze = data[len(word):].strip()
			# 记录gloze最长长度
			if b < len(gloze):b=len(gloze)
			# 记录成功插入条数
			c += 1
			# 将数据插入到数据库表words中
			if not m.myinsert('words',[word,gloze]):
				print('插入第%d条失败'%(c+1))
				break

		print('word和gloze最长分别是',a,b,'成功插入了%d条数据'%c)
			
if __name__ == '__main__':
	main()