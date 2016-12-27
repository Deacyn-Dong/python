# -*- coding: utf-8 -*-
# @Author: Deacyn-Dong
# @Date:   2016-12-28 00:04:12
# @Last Modified by:   Deacyn-Dong
# @Last Modified time: 2016-12-28 00:08:30

# Python爬虫实战-模拟登陆教务处

import requests
import sys
import os.path
import json
from bs4 import BeautifulSoup
from PIL import Image

# 非linux环境加这句
type=sys.getfilesystemencoding()

headers = {
	"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
	"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36",
	"Host":"jwpt.neuq.edu.cn",
	"Connection":"keep-alive"
}

def get_captcha():
	captcha_url = 'http://jwpt.neuq.edu.cn/ACTIONVALIDATERANDOMPICTURE.APPPROCESS'
	r = session.get(captcha_url,headers=headers)
	with open('captcha.jpg','wb') as f:
		f.write(r.content)
		f.close()
	try:
		im = Image.open('captcha.jpg')
		im.show()
		im.close()
	except:
		print(u'请到 %s 目录找到captcha.jpg 手动输入' % os.path.abspath('captcha.jpg'))
	captcha = input("please input the captcha\n>")
	return captcha

def login(username,password):
	post_url = "http://jwpt.neuq.edu.cn/ACTIONLOGON.APPPROCESS?mode=4"

	post_data = {
		"WebUserNO":username,
		"Password":password,
		"Agnomen":get_captcha(),
		"strStudentNO":"",
		"strPassword":""
	}

	login_page = session.post(post_url,data=post_data,headers=headers)
	# login_code = login_page.text
	# 通过打印状态码测试
	print login_page.status_code

def get_grades():
	grade_url = "http://jwpt.neuq.edu.cn/ACTIONQUERYGRADUATESCHOOLREPORTBYSELF.APPPROCESS"
	content = session.get(grade_url).text
	soup = BeautifulSoup(content,'lxml')

	for i in xrange(1,2):
		same_class = soup.select('tr[style="height:23px"]')[i].select("td")

		data = {
			"term":same_class[0].text.replace(u'\xa0', ''),
			"course_title":same_class[2].text.replace(u'\xa0', ''),
			"period":same_class[4].text.replace(u'\xa0', ''),
			"credit":same_class[5].text.replace(u'\xa0', ''),
			"grade":same_class[6].text.replace(u'\xa0', ''),
			"GPA":same_class[7].text.replace(u'\xa0', ''),
			
		}
		data_result = json.dumps(data, ensure_ascii=False, encoding='UTF-8')
		print data_result

if __name__ == '__main__':
	usrname = raw_input('请输入你的学号\n>'.decode('utf-8').encode(type))
	password = raw_input("请输入你的密码\n>".decode('utf-8').encode(type))
	login(usrname, password)
	get_grades()