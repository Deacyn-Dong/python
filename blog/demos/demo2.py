# -*- coding: utf-8 -*-
# @Author: Deacyn-Dong
# @Date:   2016-12-27 23:31:48
# @Last Modified by:   Deacyn-Dong
# @Last Modified time: 2016-12-27 23:47:54

# Python爬虫实战-爬取盗墓笔记小说存入数据库

import requests
import re
import MySQLdb
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

headers = {
	"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36",
	"Host":"www.quanshu.net",
	"Connection":"keep-alive"
}


def get_list(url):
	response = requests.get(url,headers=headers)
	response.encoding = "gb2312"
	reg = re.compile(r'<li><a href="(.*?)" title=".*?">(.*?)</a></li>')
	urllist = re.findall(reg,response.text)
	return urllist 
# print get_list("http://www.quanshu.net/book/9/9055")

def get_text(url):
	response = requests.get(novel_url+"/"+url,headers=headers)
	response.encoding = 'gbk'
	reg = re.compile(r'style5\(\);</script>(.*?)<script type="text/javascript">style6')
	content = re.findall(reg,response.text)
	return content[0]

class Sql(object):
	conn = MySQLdb.connect(
		host="localhost",
		port=3306,
		user="xxxxxx",
		passwd="xxxxxx",
		db="novel",
		charset="utf8"
	)
# 	# 测试是否连接成功
# 	# def testConnect(self):
# 	# 	cur = self.conn.cursor()
# 	# 	cur.execute("SELECT VERSION()")
# 	# 	data = cur.fetchone()
# 	# 	print "Database version : %s " % data
# 	# 	self.conn.close()
	def insert(self,title,content):
		cur = self.conn.cursor()
		cur.execute("insert into dmbj(title,content) values('%s','%s')" %(title,content))
		self.conn.commit()
		# cur.close()   

if __name__ == '__main__':
	mysql = Sql()
	novel_url = "http://www.quanshu.net/book/9/9055"
	for i in get_list(novel_url):
		title = i[1]
		print "正在爬取文章,章节名为 %s" %title
		content = get_text(i[0])
		print "正在插入数据库\n"
		mysql.insert(title,content)
		print "插入数据库成功"

	mysql.conn.close()
	print "任务成功"