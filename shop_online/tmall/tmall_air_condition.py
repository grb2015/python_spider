'''
  搜索某一类商品(比如空调,我正想买一台空调),给出所有品牌和厂家的分析报告

  rbguo 2018-03-15 created 
'''
from urllib import request
from urllib import error
from urllib import parse
from http import cookiejar
import urllib
import re
import codecs
import csv
import requests
import time
from bs4 import BeautifulSoup
import json

### 
def get_tmall():
	header={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.3 Safari/537.36'}
	### url是在天猫搜索"空调后"的结果页
	url= 'https://list.tmall.com/search_product.htm?spm=a220m.1000858.1000721.1.693e14908tHauf&cat=50930001&q=%BF%D5%B5%F7&sort=s&style=g&search_condition=23&sarea_code=430600&from=sn_1_cat-qp&active=2&shopType=any#J_crumbs'    

	req = requests.get(url,headers=header)
	#print('respense.getcode(,file=log_file) = %s\n\n'%req.getcode())
	html = req.content.decode('gbk')   ### 注意这里如果要自己编码，必须content，而不能req.text  ### content是二进制 
	#print(html)	 ## winxp上cmd是gbk 若是winxp这里打印会出错，win10没问题
	with codecs.open('tmall.txt','w+',encoding = 'gbk') as f:
		f.write(html)
	soup = BeautifulSoup(html,'lxml')
	p_tags = soup.find_all('p','productTitle')
	with codecs.open('tmall_air_conditioner.csv','w+',encoding = 'gbk') as market_file:
		writer = csv.writer(market_file)
		writer.writerow(['商品型号','详情页'])
		for p_tag in p_tags:
			prod_name  = p_tag.get_text()  
			prod_url = p_tag.a.get('href')
			info_list = []
			info_list.append(prod_name)
			info_list.append(prod_url)
			print(prod_name)
			print(prod_url)
			writer.writerow(info_list)

if __name__ == '__main__':
	get_tmall()