# -*- coding: utf-8 -*-
# @Author: Deacyn-Dong
# @Date:   2016-12-27 23:54:57
# @Last Modified by:   Deacyn-Dong
# @Last Modified time: 2016-12-28 00:03:49

# Python爬虫实战-ajax体验之抓取拉钩招聘信息

import time
import requests
import json
import re

headers= {
	"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36",
	"Referer":"https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput=",
	"Connection":"keep-alive"
}
items = []

def get_content(pn):
	url = "https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false"
	data = {
		"first":"true",
		"pn":pn,
		"kd":"python"
	}
	html = requests.post(url,headers=headers,data=data).text
	html = json.loads(html)
	for i in range(15):
		item = []
		item.append(html['content']['positionResult']['result'][i]['positionName'])
		item.append(html['content']['positionResult']['result'][i]['salary'])
		item.append(html['content']['positionResult']['result'][i]['positionAdvantage'])
		item.append(html['content']['positionResult']['result'][i]['workYear'])
		items.append(item)
	return items

def write():
	pageNum = 1
	while pageNum <=4:
		get_content(pageNum)
		pageNum += 1
		for i in items:
			print u'职位: %s 薪资: %s 福利:%s 要求:%s \n'  %(i[0],i[1],i[2],i[3])
		time.sleep(2)

if __name__ == '__main__':
	write()