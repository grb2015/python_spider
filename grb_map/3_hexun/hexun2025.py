# -*- coding: utf-8 -*-
# @Author: Teiei
# @Date:   2025-4-15 9:00:55
# @Last Modified by:   Teiei
# @Last Modified time: 2017-12-19 22:39:03
# @ history:
#	和讯网更新，之前的省份数据打不开了。http://datainfo.stock.hexun.com/hybk/dy.aspx
#   这里也打不开了，all_provices.json
#	需要重新用一种方法从这里获取数据：https://stockdata.hexun.com/gszl/jbgk.aspx  这里找到
#		https://stockdata.hexun.com/gszl/data/jsondata/jbgk.ashx?count=20000&titType=null&page=1&callback=hxbase_json15
#		但是即使加了cookie，也还是别对方网站策略挡在外面了。由 Tencent Cloud EdgeOne 提供防护

#	另外一种思路是获取到股票代码，然后通过此页查询 https://stockdata.hexun.com/gszl/s600519.shtml 关键是此页页有了防爬策略 。 

# 调研了直接爬取：
# 上交所 ：无法爬取
# 深交所： 公司数量太少，未研究
# 新浪  ： 没有找到目标地址
# 东方财务： 没有找到接口
# 同花顺： 没有找到接口
# 雪球 ： 未研究,需要登录
# deepseek : 给不出具体可用的代码，只能作为搜索参考
#
#
# 最终方案：可以从上交所和深交所官方网站下载excel，然后用akshared上通过股票代码查询公司其它信息的方案
#  akshared是专门研究财经的 ： https://akshare.akfamily.xyz/data/stock/stock.html#id8
# 上交所:https://www.sse.com.cn/assortment/stock/list/share/
# 深交所: https://www.szse.cn/market/product/stock/list/index.html
# 北交所：待完善https://www.bse.cn/nq/listedcompany.html

import re
import requests
import urllib,codecs,csv
from bs4 import BeautifulSoup
import datetime
import time
import json 
import pandas as pd
import akshare as ak
import erea
 



'''
	breif	: 	根据股票代码获取图片其它信息(来自雪球网)
	param	: 	stock_code : string "601127"

'''
def get_stock_info_by_code(stock_code):
	print(stock_code)
	if stock_code[0]=='6': #上交所
		param = "SH"+stock_code
	else:
		param = "SZ"+stock_code
	df = ak.stock_individual_basic_info_xq(param)
	return df



'''
	breif	: 	获取市值(来自东方财富)
	param	: 	stock_code : string "601127"

'''
def get_stock_value_by_code(stock_code):
	df = ak.stock_individual_info_em(symbol=stock_code)
	# print(df)
	return df



'''
	breif :	读取股票名单，然后根据股票代码在akshare查其它数据后返回为一个df
	params:	
		share_type 类别 （"沪A股,"沪科创板")
'''

def Struct_df_SH(columns,share_type,sourcefile):
	df_SH = pd.DataFrame(columns=columns)
	df_SH_source = pd.read_excel(sourcefile)   # 读取上交所的excel
	df_SH_source = pd.read_excel('bourse_SH_tech.xls')   # 读取上交所的excel
	print("df_SH:")
	print(df_SH)
	df_SH["类别"] = "沪A股"
	print(" type df_SH")
	print(type(df_SH))
	print(" type(df_SH[\"类别\"] ")
	print(type(df_SH["类别"] ))
	print(df_SH)
	df_SH["股票代码"] = df_SH_source["A股代码"]
	df_SH["公司简称"] = df_SH_source["证券简称"]
	df_SH["类别"] = share_type
	# print( df_SH_source["上市日期"] )
	# print( type(df_SH_source["上市日期"]) )
	df_SH["上市日期"] =  pd.to_datetime(df_SH_source["上市日期"].astype(str), format='%Y%m%d')
	print(df_SH)
	# print(df_SH_source.index.size)

	


	# for in in range(df.index.size):
	for i in range(2):
	# for i in range(df_SH_source.index.size):
		stock_code = str( df_SH['股票代码'][i] )
		df_row = df_SH.loc[i]	#获取第i行

		df_single_company_info = get_stock_info_by_code(str(stock_code))

		df_tmp = df_single_company_info [ df_single_company_info["item"] ==  "provincial_name" ]# # 注意这里的列名只有item和value,所以要这样寻找
		provincial_name = df_tmp['value'].iloc[0]

		df_tmp = df_single_company_info [ df_single_company_info["item"] ==  "district_encode" ]
		district_encode = df_tmp['value'].iloc[0]

		df_tmp = df_single_company_info [ df_single_company_info["item"] ==  "org_name_cn" ] 
		org_name_cn = df_tmp['value'].iloc[0]

		df_tmp = df_single_company_info [ df_single_company_info["item"] ==  "affiliate_industry" ] 
		affiliate_industry = df_tmp['value'].iloc[0]["ind_name"]

		df_tmp = df_single_company_info [ df_single_company_info["item"] ==  "reg_address_cn" ] 
		reg_address_cn = df_tmp['value'].iloc[0]

		df_tmp = df_single_company_info [ df_single_company_info["item"] ==  "office_address_cn" ] 
		office_address_cn = df_tmp['value'].iloc[0]

		df_tmp = df_single_company_info [ df_single_company_info["item"] ==  "org_website" ] 
		org_website =  df_tmp['value'].iloc[0]  

		df_tmp = df_single_company_info [ df_single_company_info["item"] ==  "established_date" ]    #  成立日期（时间戳）
		int_timestamp = df_tmp['value'].iloc[0]
		established_date = pd.to_datetime(int_timestamp, unit="ms").strftime("%Y-%m-%d") # 时间戳转为1999-01-01格式
		print(" established_date = ")
		print( established_date  )
		df_tmp = df_single_company_info [ df_single_company_info["item"] ==  "staff_num" ] 
		staff_num = df_tmp['value'].iloc[0]


		# df_row["省"] = provincial_name  
		df_row["行政区划"] = district_encode
		df_row["公司全名"] = org_name_cn
		df_row["行业"] =  affiliate_industry
		df_row["注册地"] =  reg_address_cn
		df_row["办公地"] =  office_address_cn
		df_row["官网"] =  org_website
		df_row["成立日期"] =  established_date
		df_row["员工人数"] =  staff_num

		# http接口获取市值
		df_stock_value_info = get_stock_value_by_code(str(stock_code))
		df_tmp = df_stock_value_info [ df_stock_value_info["item"] ==  "总市值" ] 
		market_value = df_tmp['value'].iloc[0]
		df_row["总市值(亿)"] = round(market_value/100000000,2) # 保留两位小数

		# http接口，通过行政编码获取省市区的格式化数据。
		eara_list = erea.get_division_info(df_row["行政区划"])
		df_row["省"] = eara_list[0]  
		df_row["市"] = eara_list[1]  
		df_row["县"] = eara_list[2]  

		# print(eara_list)

		df_SH.loc[i] = df_row
		print(df_SH)
		time.sleep(0.5)
	return df_SH



'''
	breif :	读取深交所的A股和创业板名单，然后根据股票代码在akshare查其它数据后返回为一个df
'''

def Struct_df_SZ(columns):
	df_SZ = pd.DataFrame(columns=columns)
	df_SZ_source = pd.read_excel('bourse_SZ.xlsx')   # 读取深交所的excel  股票代码000001读取出来为1了
	print("df_SZ_source")
	print(df_SZ_source)
	print("df_SZ_source  A股代码")
	print(df_SZ_source[["A股代码","A股简称"]])
	
	df_SZ["股票代码"] = df_SZ_source["A股代码"].astype(str).str.zfill(6)  ## 000001会被识别为1，excel表也改不了。这里将1改为000001
	df_SZ["公司简称"] = df_SZ_source["A股简称"]
	df_SZ["上市日期"] = df_SZ_source["A股上市日期"]
	# print("日期：")
	# print(df_SZ["上市日期"] )
	# return  df_SZ
	df_SZ["公司全名"] = df_SZ_source["公司全称"]
	# df_SZ["行业"] = df_SZ_source["所属行业"]
	# df_SZ["省"] = df_SZ_source["省    份"]
	# df_SZ["市"] = df_SZ_source["城     市"]
	df_SZ["官网"] = df_SZ_source["公司网址"]
	df_SZ["注册地"] = df_SZ_source["注册地址"]
	
	
	print(df_SZ)

	# for in in range(df.index.size):
	for i in range(2):
	# for i in range(df_SZ_source.index.size):
		stock_code = str( df_SZ['股票代码'][i] )
		df_row = df_SZ.loc[i]	#获取第i行

		print("__________________获取接口数据1 begin ___________________________________________")
		print(stock_code)
		df_single_company_info = get_stock_info_by_code(str(stock_code))
		print(df_single_company_info,file=log_file)
		print(df_single_company_info)
		print("__________________获取接口数据1 end ___________________________________________")


		# df_tmp = df_single_company_info [ df_single_company_info["item"] ==  "provincial_name" ]# # 注意这里的列名只有item和value,所以要这样寻找
		# provincial_name = df_tmp['value'].iloc[0]

		df_tmp = df_single_company_info [ df_single_company_info["item"] ==  "district_encode" ]
		district_encode = df_tmp['value'].iloc[0]

		# df_tmp = df_single_company_info [ df_single_company_info["item"] ==  "org_name_cn" ] 
		# org_name_cn = df_tmp['value'].iloc[0]

		df_tmp = df_single_company_info [ df_single_company_info["item"] ==  "affiliate_industry" ] 
		affiliate_industry = df_tmp['value'].iloc[0]["ind_name"]

		# df_tmp = df_single_company_info [ df_single_company_info["item"] ==  "reg_address_cn" ] 
		# reg_address_cn = df_tmp['value'].iloc[0]

		df_tmp = df_single_company_info [ df_single_company_info["item"] ==  "office_address_cn" ] 
		office_address_cn = df_tmp['value'].iloc[0]

		# df_tmp = df_single_company_info [ df_single_company_info["item"] ==  "org_website" ] 
		# org_website =  df_tmp['value'].iloc[0]  

		df_tmp = df_single_company_info [ df_single_company_info["item"] ==  "established_date" ]    #  成立日期（时间戳）
		int_timestamp = df_tmp['value'].iloc[0]
		established_date = pd.to_datetime(int_timestamp, unit="ms").strftime("%Y-%m-%d") # 时间戳转为1999-01-01格式

		df_tmp = df_single_company_info [ df_single_company_info["item"] ==  "staff_num" ] 
		staff_num = df_tmp['value'].iloc[0]


		# df_row["省"] = provincial_name  
		df_row["行政区划"] = district_encode
		# df_row["公司全名"] = org_name_cn
		df_row["行业"] =  affiliate_industry
		# df_row["注册地"] =  reg_address_cn
		df_row["办公地"] =  office_address_cn
		# df_row["官网"] =  org_website
		df_row["成立日期"] =  established_date
		df_row["员工人数"] =  staff_num
		print("类别 = ")
		print(stock_code[0:2])
		if stock_code[0:2] =="30" :
			df_row["类别"] = "深A股"
		elif stock_code[0:2] =="00":
			df_row["类别"] = "深创业板"


		df_stock_value_info = get_stock_value_by_code(str(stock_code))
		df_tmp = df_stock_value_info [ df_stock_value_info["item"] ==  "总市值" ] 
		market_value = df_tmp['value'].iloc[0]
		df_row["总市值(亿)"] = round(market_value/100000000,2) # 保留两位小数


		# http接口，通过行政编码获取省市区的格式化数据。
		eara_list = erea.get_division_info(df_row["行政区划"])
		df_row["省"] = eara_list[0]  
		df_row["市"] = eara_list[1]  
		df_row["县"] = eara_list[2]  
		
		df_SZ.loc[i] = df_row
		print(df_SZ)
		time.sleep(0.5)
	return df_SZ





if __name__ == '__main__':

	log_file = codecs.open("./china_rt_log.txt", 'w+',encoding ='utf-8') 
	# 保存为 CSV 文件（防止中文乱码，兼容 Excel）
	target_file_name = "all_province_commanpy_info_all_country_formated_addr.csv"
	columns = ["类别","省","市","县","公司简称","行政区划","公司全名","行业","员工人数","总市值(亿)","股票代码","注册地","办公地","官网","成立日期","上市日期"]

	print("######")
	# 	沪主板A股
	df_sh = Struct_df_SH(columns,"沪A股",'bourse_SH.xls')
	print(df_sh)
	print(df_sh,file=log_file)

	df_sh.to_csv(target_file_name, index=False, encoding="utf_8_sig")

	
	# 沪科创板
	df_sh_tech= Struct_df_SH(columns,"沪科创板",'bourse_SH_tech.xls')
	df_sh_tech.to_csv(target_file_name,mode="a" ,header=False, index=False, encoding="utf_8_sig") # 追加,header=False避免重复写入列名


	# 深主板A股 & 深创业板
	df_sz = Struct_df_SZ(columns)
	df_sz.to_csv(target_file_name,mode="a" ,header=False, index=False, encoding="utf_8_sig") # 追加,header=False避免重复写入列名
	print("----------------------")
	print("----------------------",file=log_file)
	print(df_sz)
	print(df_sz,file=log_file)


	

	


	# df_merged = pd.concat([df_sh, df_sz], ignore_index=True) # 设置 ignore_index=True 以重新索引
	# df_merged.to_csv("all_province_commanpy_info_all_country_formated_addr.csv", index=False, encoding="utf_8_sig")








