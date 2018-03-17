'''
  搜索某一类商品(比如空调,我正想买一台空调),给出所有品牌和厂家的分析报告

  rbguo 2018-03-15 created 


  遇到的一些问题：
  	1.直接右键查看源代码发现产品的参数被天猫转义了 如tr><th>空调品牌</th><td>&nbsp;Midea/&#32654;&#30340;</td>
  	 可以使用html模块转回来
	 import html
	rt_str = html.unescape('&#32654;&#30340');
	print(rt_str)

	2. 详情页里面的价格右键源代码看不到，这可能是js还没有完全加载,需要用selenium开一个浏览器，selenium会等完全
	加载后返回



'''
from selenium import webdriver
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
import time

### 
def get_goods_urls():
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
		goods_urls = []
		writer.writerow(['商品型号','详情页'])
		for p_tag in p_tags:
			prod_name  = p_tag.get_text()  
			prod_url = p_tag.a.get('href')
			info_list = []
			info_list.append(prod_name)
			info_list.append(prod_url)
			#print(prod_name)
			#print(prod_url)
			writer.writerow(info_list)
			goods_urls.append('http:'+prod_url)
	return goods_urls


def get_detail_page_info(detail_url):
	header={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.3 Safari/537.36'}
	
	req = requests.get(detail_url,headers=header)

	req_html = req.content.decode('gbk')   ### 注意这里如果要自己编码，必须content，而不能req.text  ### content是二进制 
	#print(html)	 ## winxp上cmd是gbk 若是winxp这里打印会出错，win10没问题

	with codecs.open('detail_page.html','w+',encoding = 'gbk') as f:
		f.write(req_html)
	soup = BeautifulSoup(req_html,'lxml')
	tbody0 = soup.find_all('tbody')[0]
	soup = BeautifulSoup(str(tbody0))
	th_tags = soup.find_all('th')
	parmam_name_list = []
	for th_tag in th_tags:
		param_name = th_tag.get_text()
		parmam_name_list.append(param_name)
	td_tags = soup.find_all('td')
	parmam_val_list = []
	for td_tag in td_tags:
		param_val = td_tag.get_text()
		param_val = "".join(param_val.split()) ### 去掉 &nbsp 即\xa0
		print(param_val)
		parmam_val_list.append(param_val)

	parmam_name_list.remove('尺寸规格')
	parmam_name_list.remove('基本参数')
	parmam_name_list.remove('技术参数')

	#print(parmam_name_list,len(parmam_name_list))
	#print(parmam_val_list,len(parmam_val_list))
	return [parmam_name_list,parmam_val_list]
def get_current_price(detail_page_url):
	options = webdriver.ChromeOptions()
	options.add_argument('user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.3 Safari/537.36"')
	driver = webdriver.Chrome(chrome_options=options)
	driver.get(detail_page_url)
	time.sleep(2)
	html = driver.page_source
	with codecs.open('detail_page_semuum.html','w+',encoding = 'utf=8') as f:
		f.write(html)
	print(html)
	soup = BeautifulSoup(html,'lxml')
	
	try:	## 参加家年华的话价格取家年华的价
		dl_tag = soup.find_all('dl','tm-happy11-panel')[0]  ### 嘉年华价格
		print(str(dl_tag))
		soup = BeautifulSoup(str(dl_tag),'lxml')
		dt_tag = soup.find_all('span','tm-price')[0]
		current_price = dt_tag.get_text()
		print('家年华价 = ',current_price)
	except:## 否则选取促销价
		try:
			div_tag = soup.find_all('div','tm-promo-price')[0]
			print(str(div_tag))
			soup = BeautifulSoup(str(div_tag),'lxml')
			dt_tag = soup.find_all('span','tm-price')[0]
			current_price = dt_tag.get_text()
			print('促销价 = ',current_price)
		except:
			span_tag = soup.find_all('span','tm-price')[0]
			print(str(span_tag))
			current_price = span_tag.get_text()
			print('价格 = ',current_price)

		

	driver.close()
	return current_price
	

if __name__ == '__main__':
	
	### 获取空调类所有的商品详情页
	goods_urls = get_goods_urls()

	### 获取每件商品的参数项目和对应的值，当前价格  [ [项目list],[值list] ] 
	#  list_name_val[0] 为参数项目的列表
	#      如 ['内机包装尺寸', '内机尺寸', '内机毛重', '外机包装尺寸',...]
	#  list_name_val【1] 为参数的值的list
	#      如 ['985x377x305mm', '889x294x212mm', '13kg', '882x362x595mm', ...]
	#      
	#      
	#get_current_price(goods_urls[6])
	
	
	list_name_val = get_detail_page_info(goods_urls[0])
	print(list_name_val)
	with codecs.open('all_goods_param.csv','a+',encoding = 'gbk') as market_file:
		writer = csv.writer(market_file)

		#list_name_val[0].append('当前价格')
		#writer.writerow(list_name_val[0])  ### 各种参数的名称,作为表头

		#cur_price = get_current_price(goods_urls[0])
		#list_name_val[1].append(cur_price)
		#writer.writerow(list_name_val[1])

		
		for goods_url in goods_urls[23:]:
			
			list_name_val = get_detail_page_info(goods_url)

			cur_price = get_current_price(goods_url)
			list_name_val[1].append(cur_price)
			writer.writerow(list_name_val[1])	### 以后每个就只要写入值就可以了
	
		
	

