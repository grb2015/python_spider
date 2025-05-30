# -*- coding: utf-8 -*-
# @Author: Teiei
# @Date:   2017-12-17 20:00:55
# @Last Modified by:   Teiei
# @Last Modified time: 2017-12-19 22:39:03
# @ history:
#	博汇科技的url(http://stockdata.stock.hexun.com/688004.shtml)打开跟其他的不一样，导致程序出错。添加try except忽略

#	20250415 added
#	和讯网更新，之前的省份数据打不开了。http://datainfo.stock.hexun.com/hybk/dy.aspx
#   这里也打不开了，all_provices.json
#	需要重新用一种方法从这里获取数据：https://stockdata.hexun.com/gszl/jbgk.aspx

import re
import requests
import urllib,codecs,csv
from bs4 import BeautifulSoup
import datetime
import time
import json 
 
################################################################################
#	brief : 封装request请求
#
#
#
#
################################################################################
def gethtml(url):
	print("url = ")
	print(url)
	reqheader = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'}
	i = 0
	while i < 10:
		try:
			req = requests.get(url,headers=reqheader,timeout=20)
			return req
		except requests.exceptions.RequestException as e:
			print("############################# [gethtml] 异常 ,i =",i,file=log_file)
			print(e,file=log_file)
			print("############################# [gethtml] 异常 ,i =",i)
			print(e)
			i += 1
	return None


def get_one_commany_info(detail_url):
	req = gethtml(detail_url)
	if req:
		html = req.text
		utf_8_html = html.encode('utf-8')
		#with open('get_commany_info.html','wb+') as f:   ### 不正确
		#			f.write(utf_8_html)
		#print('### detail html ',html,file=log_file)
		#time.sleep(1)
		soup = BeautifulSoup(html,'lxml')
		td_tags = soup.find_all('td')  ##<td> class为空  <td>华数传媒</td
		brief_commany_name = td_tags[1].get_text()
		detail_commany_name = td_tags[5].get_text()
		industry = td_tags[13].get_text()
		province = td_tags[17].get_text()
		registe_addr = td_tags[31].get_text()
		work_addr = td_tags[35].get_text()
		web_site = td_tags[73].get_text()
		shangshi_data = td_tags[41].get_text()
		info_list = []
		info_list.append(brief_commany_name)
		info_list.append(detail_commany_name)
		info_list.append(industry)
		info_list.append(province)
		info_list.append(registe_addr)
		info_list.append(work_addr)
		info_list.append(web_site)
		info_list.append(shangshi_data)
		print(info_list)
		#print(info_list,file=log_file)
		return info_list
	return []


'''
	取得一个省的所有上市公司的详情页并存入detail_urls.json
'''
def  get_one_province_detail_urls_store_in_json(url):
	req = gethtml(url)
	if req:
		html = req.text

		soup = BeautifulSoup(html,'lxml')
		option_tag_end = soup.find_all('option')[-1]  ###最后一个
		total_page = option_tag_end.get_text()
		print('total_page = ',total_page,file=log_file)  ### 共多少页
		detail_urls = []
		urls = []
		for i in range(1,int(total_page)+1):
			url1 = url+'&page=%s'%(i)
			print(' ###  format url = ',url1,file=log_file)
			req = gethtml(url1)
			if req:
				html = req.text
				#print(html,file=log_file)
				soup = BeautifulSoup(html,'lxml')
				a_tags = soup.find_all('a','amal')
				
				for  a_tag in a_tags:
					# print(a_tag.get_text(),file=log_file)  ### 公司简称
					# print(a_tag.get_text()) 
					urls.append(a_tag.get('href'))
					#print(urls,file=log_file)
		print('#### final urls = ',urls,file=log_file)
		len_urls = len(urls)
		i = 0
		
		for url in urls:  
			#print('  for  url1  = ',url,file=log_file)
			if i%2: # url连续两个是重复的
			# if True:
				#print('get_one_province_detail_urls_store_in_json... [%d/%d] '%(i,len_urls),file=log_file)
				try:
					print('get_one_province_detail_urls_store_in_json... [%d/%d] '%(i,len_urls))
					print('  ##################################### for  url  = ',url,file=log_file)
					print('  for  url  = ',url)
					req = gethtml(url)
					if req:
						html = req.text
						#utf_8_html = html.encode('utf-8')
						#with open('detail.html','wb+') as f:
						#	f.write(utf_8_html)
							
						# print(html,file=log_file)
						soup = BeautifulSoup(html,'lxml')
						a_tag0 = soup.find_all('a',id='a_leftmenu_dt4_1')[0]  ### 公司资料网页
						detail_url = a_tag0.get('href')
						#print(detail_url,file=log_file)
						detail_urls.append(detail_url)

						### 获取当前年度(或半年度)销售额和利润
						info_list = []
						a_tag0 = soup.find_all('div','cwdesc')[0]  ### class = cwdesc
						profit_str = a_tag0.get_text()
						re_result = re.match(r'.+?收入(.+?)万元.*?利润(.+?)万元', profit_str)
						if re_result:
							turnover = re_result.group(1)
							profit = re_result.group(2)
							info_list.append(turnover)
							info_list.append(profit)
						
						a_tag0 = soup.find_all('a',id = 'navName')[0]  ### 获得当前的公司名称
						name_and_code = a_tag0.get_text() 
						info_list.append(name_and_code)
						writer2.writerow(info_list)
						print(info_list)
					
				except Exception  as e:
					print("############################# 异常",file=log_file)
					print(e,file=log_file)
					print("############################# 异常")
					print(e)
					pass

			i = i+1
		print('detail_urls = ',detail_urls,file=log_file)   #### 该省所有上市公司的详情页


		with open('detail_urls.json', 'w+') as josn_fd: ## 创建6-1.json
				json.dump(detail_urls, josn_fd)
		
		

		

def read_data_from_json():
	with open('detail_urls.json', 'r') as f:
		data = json.load(f)
	return data  ### list 
'''
	读取存放在json文件中的公司详情页,并逐一获取具体信息写到 all_prince_commanpy_info.csv
'''
def get_all_commany_info_from_json_urls():
	urls = read_data_from_json()


	for url in urls:
		print('### detal_url = ',url,file=log_file)
		url = url[:-1]
		print('### detal_url[:-1] = ',url,file=log_file)
		result_info_list  = []
		result_info_list = get_one_commany_info(url)   ## "http://stockdata.stock.hexun.com/gszl/s002112.shtml "
		writer.writerow(result_info_list)					### 最后面有个空格,要去掉，不然不行

'''
	获取所有省份(31个)的入口地址
'''
def get_all_provices_index_urls():
	url  = 'https://stockdata.hexun.com/gszl/data/jsondata/jbgk.ashx?count=20&titType=null&page=1&callback=hxbase_json15'
	all_provices = []
	req = gethtml(url)
	print("Req = ")
	print(req)
	if req:
		html = req.text

		soup = BeautifulSoup(html,'lxml')
		a_tags = soup.find_all('a','amal')
			
		for  a_tag in a_tags:
			print(a_tag.get_text(),file=log_file)  ### 公司简称
			all_provices.append('http://datainfo.stock.hexun.com/hybk/'+a_tag.get('href'))
		with open('all_provices.json', 'w+') as josn_fd: ## 存放每个省份的入口地址
				json.dump(all_provices, josn_fd)

		print(all_provices,file=log_file)
		print(len(all_provices),file=log_file)
		return all_provices
	return []

if __name__ == '__main__':
	log_file = codecs.open("./china_rt_log.txt", 'w+',encoding ='utf-8') 

	csv_fd = codecs.open('all_prince_commanpy_info.csv','w+',encoding ='utf-8')
	writer = csv.writer(csv_fd)
	writer.writerow(["公司简称","公司全名","行业","所在省","注册地","办公地","官网","上市日期"])

	csv_fd2 = codecs.open('all_prince_commanpy_profit.csv','w+',encoding ='utf-8')
	writer2 = csv.writer(csv_fd2)
	writer2.writerow(["公司简称","营业额","利润(万元)"])


	all_provices = get_all_provices_index_urls()
	print("all_provinces = ")
	print(all_provices)
	#get_one_province_detail_urls_store_in_json(all_provices[7])
	#get_all_commany_info_from_json_urls()
	#print('---------------------------------------------------',file=log_file)
	#get_one_province_detail_urls_store_in_json(all_provices[-6])
	#get_all_commany_info_from_json_urls()
	
	
	# for province_url  in all_provices[:8]:
	for province_url  in all_provices:
			print('##### province_url = ',province_url,file=log_file)
			print('##### province_url = ',province_url)
			get_one_province_detail_urls_store_in_json(province_url)
			get_all_commany_info_from_json_urls()
	
	
	
	#url = 'http://datainfo.stock.hexun.com/hybk/dygs.aspx?fld_areano=305000000'

	#get_one_province(url)
	#d_url = 'http://stockdata.stock.hexun.com/gszl/s000411.shtml'
	#d_url = 'http://stockdata.stock.hexun.com/gszl/s000156.shtml'
	#get_one_commany_info(d_url)
	#get_all_commany_info()