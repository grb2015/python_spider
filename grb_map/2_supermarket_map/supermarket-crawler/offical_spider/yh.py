# -*- coding: utf-8 -*-
# @Author: Teiei
# @Date:   2017-12-02 19:03:25
# @Last Modified by:   Teiei
# @Last Modified time: 
# @breif 抓取全国永辉超市门店信息
# history:
# 20250415 原来的url无法获取，更新新的 http://www.yonghui.com.cn/store_md
import codecs
import csv
import requests
from bs4 import BeautifulSoup
import time
import re
def get_hy():
	with codecs.open('china_offical_yh.csv','w+',encoding = 'gbk') as market_file:
		writer = csv.writer(market_file)
		writer.writerow(['品牌','省','市','分店名称','地址','电话','开店日期'])
		page1to8_urls = [
			'http://www.yonghui.com.cn/mapi/proajax?act=5&seltype=0&keyword=&p=0&rnd=504.17244157972266',
			'http://www.yonghui.com.cn/mapi/proajax?act=5&seltype=0&keyword=&p=2&rnd=657.8245444726886',
			'http://www.yonghui.com.cn/mapi/proajax?act=5&seltype=0&keyword=&p=3&rnd=12.89561468853928',
			'http://www.yonghui.com.cn/mapi/proajax?act=5&seltype=0&keyword=&p=4&rnd=418.9635622505301',
			'http://www.yonghui.com.cn/mapi/proajax?act=5&seltype=0&keyword=&p=5&rnd=162.32521407619282',
			'http://www.yonghui.com.cn/mapi/proajax?act=5&seltype=0&keyword=&p=6&rnd=587.2934854558861',
			'http://www.yonghui.com.cn/mapi/proajax?act=5&seltype=0&keyword=&p=7&rnd=306.9766691198954',
			'http://www.yonghui.com.cn/mapi/proajax?act=5&seltype=0&keyword=&p=8&rnd=768.4928311305584',
		]

		header={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.3 Safari/537.36'}
		for url in page1to8_urls:
			req = requests.get(url,headers=header)
			html = req.text
			print(html)
			# return 
			# html = req.content.decode('gbk')  ### 注意这里如果要自己编码，必须content，而不能req.text
			# print(html)							### content是二进制 
			print("\n\n\n")
			soup = BeautifulSoup(html,'lxml')
			print(soup)
			# li_tags = soup.find_all('table',width='747')
			li_tags = soup.find_all('li')
			# print("\n\n\n")
			# print(li_tags)
			# print(len(li_tags))
			# print("\n\n\n")
			#print('########### li_tags = ',li_tags)
			for li_tag in li_tags:
				print(li_tag)
				soup = BeautifulSoup(str(li_tag),'lxml')
				i_tags = soup.find_all('i')
				store_info = i_tags[0].get_text()
				print(store_info)
				# province = store_info.split(' ')
				store_info_list = re.split(r'\s+', store_info)
				if( len (store_info_list) ) == 3:  #['分店名称：', '北京', '西城区陶然亭店']
					print(store_info_list)
					province = store_info_list[1]  # 省
					city = store_info_list[1]  # 市
					store_name = store_info_list[2] # 分店名称
				else:
					print(store_info_list)
					province = store_info_list[1]  # 省
					city = store_info_list[2]  # 市
					store_name = store_info_list[3] # 分店名称
				addr_info = i_tags[1].get_text()	# 地址
				# print (" addr _str  = ")
				# print(addr_str)
				# addr_list  =   addr_str.split(':')
				addr= re.split(r'：+', addr_info)[1]  # ['地址', '福建省莆田市荔城区西天尾镇荔城北大道3100号九华广场']
				try:
					phone_info = i_tags[2].get_text()	# 电话
					phone = re.split(r'：+', phone_info)[1] 
					setup_info = i_tags[3].get_text()	# 成立日期
					setup_date =  re.split(r'：+', setup_info)[1] 
					info_list = []
					info_list.append('永辉')
					info_list.append(province)
					info_list.append(city)
					info_list.append(store_name)
					info_list.append(addr)
					info_list.append(phone)
					info_list.append(setup_date)
					# print(info_list)
					writer.writerow(info_list)
				except Exception as e:
					print(e)
					pass
		

if __name__ == '__main__':

	get_hy()