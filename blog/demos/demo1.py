# -*- coding: utf-8 -*-
# @Author: Deacyn-Dong
# @Date:   2016-12-27 23:04:27
# @Last Modified by:   Deacyn-Dong
# @Last Modified time: 2016-12-27 23:30:49

# Python爬虫实战-爬取58同城二手平板交易信息

import requests
import json
from bs4 import BeautifulSoup

headers = {
	"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
	"Connection":"keep-alive"
}

def get_one_page(url):
	response = requests.get(url,headers=headers)
	#若没有lxml库则为:soup = BeautifulSoup(response.text)
	soup = BeautifulSoup(response.text,'lxml')
	# 逐条获取信息
	title = soup.title.text
	price = soup.select('span.price_now i')
	# print price
	look_time = soup.select('span.look_time')
	want_person = soup.select('span.want_person')
	place = soup.select('div.palce_li i')
	# 各项信息存入字典
	data = {
		'title':title,
		'price':price[0].text,
		'look_time':look_time[0].text.replace(u'次浏览',''),
		'want_person':want_person[0].text.replace(u'人想买',''),
		'place':place[0].text
	}
	# 字典序列化为json，方便调试
	data_result = json.dumps(data, ensure_ascii=False, encoding='UTF-8')
	return data_result
	# return data

def get_links(urls):
	links = []
	response = requests.get(urls,headers=headers)
	soup = BeautifulSoup(response.text,'lxml')
	# 页面改版代码轻微改动
	try:
		for link in soup.select('div.infocon')[1].select('table.tbimg td.t a.t'):
			links.append(link.get('href'))
		return links
	except:
		for link in soup.select('table.tbimg td.t a.t'):
			links.append(link.get('href'))
		return links
		pass

def get_every_page(end_page):
	page = 1
	while page <= end_page:
		new_page = 'http://qhd.58.com/pbdnipad/0/pn{}/'.format(page)
		urls = get_links(new_page)
		for url in urls:
			print get_one_page(url)
		page += 1
		
if __name__ == '__main__':
	# 参数自己指定
	get_every_page(2)

	# cmd输入
	# page_num = raw_input("please input your desired page number\n>")
	# get_every_page(page_num)