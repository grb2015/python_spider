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

#          行政编码
# 生益科技	441900
# 酒钢宏兴	620200
# 中炬高新	442000
# 中国海油	052001
# 中国移动	052001
# 明阳智能	442000
# 华立股份	441900
# 依顿电子	442000
# 安达智能	441900
# 利扬芯片	441900
# 生益电子	441900
# 开普云	441900
# 百济神州	013002
# 赛微微电	441900
# 博力威	441900
# 华虹公司	052001

# 安达智能	441900
# 利扬芯片	441900
# 生益电子	441900
# 开普云	441900
# 百济神州	013002
# 赛微微电	441900
# 博力威	441900
# 华虹公司	052001
# 华润微	013002
# 诺诚健华	013002
# 精智达	440309
# 优利德	441900
# 鼎通科技	441900
# 奥普特	441900
# 格科微	013002
# 中芯国际	013002
# 九号公司	013002
# 激智科技	



# 以上公司都是无法通过接口行政编码获取到格式化地址


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

#################################################################################################
#	breif	: 根据股票代码识别出类别(辅助函数)
#
#
#################################################################################################

def assign_category(code):
    if code.startswith(("00")):
        return "深A股"
    elif code.startswith("30"):
        return "深创业板"
    else:
        return "其他板块"  # 预留扩展


##############################################################################################################
	# breif :	获取单个公司的信息
	# params:	str 	stock_code 股票代码str
##############################################################################################################

def get_single_info(stock_code):
	info = {}
	flag = False
	count = 0 
	while flag == False and count<5:
		try:
			df_single_company_info = get_stock_info_by_code(stock_code)

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

			df_tmp = df_single_company_info [ df_single_company_info["item"] ==  "staff_num" ] 
			staff_num = df_tmp['value'].iloc[0]


			# http接口获取市值
			df_stock_value_info = get_stock_value_by_code(str(stock_code))
			df_tmp = df_stock_value_info [ df_stock_value_info["item"] ==  "总市值" ] 
			market_value = df_tmp['value'].iloc[0]
			time.sleep(0.5)
			print("time sleep 0.5...")
			# http接口，通过行政编码获取省市区的格式化数据。
			eara_list = erea.get_division_info(district_encode)

			
			info['总市值(亿)'] = round(market_value/100000000,2)
			info['行政区划'] = district_encode
			info['公司全名'] = org_name_cn
			info['行业'] = affiliate_industry
			info['注册地'] = reg_address_cn
			info['办公地'] = office_address_cn
			info['官网'] = org_website
			info['成立日期'] = established_date
			info['员工人数'] = staff_num
			if len(eara_list) == 3 :
				info['省'] = eara_list[0]  
				info['市'] = eara_list[1]  
				info['县'] = eara_list[2]  
			elif len(eara_list) == 2 :  #东莞等比较特殊，市下面直接是镇
				info['省'] = eara_list[0]  
				info['市'] = eara_list[1] 
				info['县'] = " "
			elif len(eara_list) == 1 :  #东莞等比较特殊，市下面直接是镇
				info['省'] = eara_list[0]  
				info['市'] = " "
				info['县'] = " "
			else:
				info['省'] = " "
				info['市'] = " "
				info['县'] = " "
			print("single_info  = ")
			print(info)
			flag = True
		except Exception as e:
			print("### exception get_single_info ")
			print(e)
			print(e,file=log_file)
			time.sleep(5)
			print("再次尝试...")
			flag = False
			count = count + 1
			print("正在尝试第"+count+"次")
			pass
	return info

##############################################################################################################
	# breif :	读取股票名单，然后根据股票代码在akshare查其它数据后返回为一个df
	# params:	
##############################################################################################################

def Struct_df(columns,sourcefile):
	df = pd.DataFrame(columns=columns)
	# df = pd.DataFrame(columns=columns).astype('string')
	df_source = pd.read_excel(sourcefile)    
	if df_source.index.size < 1:
		return df 

	if sourcefile == 'bourse_SH.xls' or sourcefile == 'bourse_SH_tech.xls' :
		df["股票代码"] = df_source["A股代码"]
		df["公司简称"] = df_source["证券简称"]
		df["上市日期"] =  pd.to_datetime(df_source["上市日期"].astype(str), format='%Y%m%d')
		if  sourcefile == 'bourse_SH.xls':
			df["类别"] = "沪A股"
		else:
			df["类别"] = "沪科创板"
	elif sourcefile == 'bourse_SZ.xlsx': 
		df["股票代码"] = df_source["A股代码"].astype(str).str.zfill(6)  ## 000001会被识别为1，excel表也改不了。这里将1改为000001
		df["公司简称"] = df_source["A股简称"]
		df["上市日期"] = df_source["A股上市日期"]
		df["类别"] = df["股票代码"].apply(assign_category)



	# for in in range(df.index.size):
	# for i in range(2):
	for i in range(df_source.index.size):
		try:
			single_info = get_single_info(str( df['股票代码'][i] ))
			if single_info :
				df.loc[i,"总市值(亿)"] = single_info['总市值(亿)']
				df.loc[i,"行政区划"] = single_info['行政区划']
				df.loc[i,"公司全名"] = single_info['公司全名']
				df.loc[i,"行业"] =  single_info['行业']
				df.loc[i,"注册地"] =  single_info['注册地']
				df.loc[i,"办公地"] =  single_info['办公地']
				df.loc[i,"官网"] =  single_info['官网']
				df.loc[i,"成立日期"] =  single_info['成立日期']
				df.loc[i,"员工人数"] =  single_info['员工人数']
				df.loc[i,"省"] = single_info['省']
				df.loc[i,"市"] = single_info['市']
				df.loc[i,"县"] = single_info['县']

		except Exception as e:
			print("### exception  Struct_df")
			print(e)
			print(e,file=log_file)
			pass
	return df	
		
	





if __name__ == '__main__':

	log_file = codecs.open("./china_rt_log.txt", 'w+',encoding ='utf-8') 
	# 保存为 CSV 文件（防止中文乱码，兼容 Excel）
	target_file_name = "all_province_commanpy_info_all_country_formated_addr.csv"
	columns = ["类别","省","市","县","公司简称","行政区划","公司全名","行业","员工人数","总市值(亿)","股票代码","注册地","办公地","官网","成立日期","上市日期"]

	# # 	沪主板A股
	df1 = Struct_df(columns,'bourse_SH.xls')
	print("######  df1"  )
	print(df1)
	print(df1,file=log_file)
	print("df1.index.size = " )
	print(df1.index.size )
	if df1.index.size >0 :
		df1.to_csv(target_file_name, index=False, encoding="utf_8_sig")

	print("time sleep 1 ...")
	# # 沪科创板
	df2= Struct_df(columns,'bourse_SH_tech.xls')
	if df2.index.size >0 :
		df2.to_csv(target_file_name,mode="a" ,header=False, index=False, encoding="utf_8_sig") # 追加,header=False避免重复写入列名
	print("###### df2"  )
	print("df2.index.size = " )
	print(df2.index.size )
	print(df2)
	print(df2,file=log_file)
	print("time sleep 1 ...")


	# 深主板A股 & 深创业板
	df3= Struct_df(columns,'bourse_SZ.xlsx')
	print("df3.index.size = " )
	print(df3.index.size )
	if df3.index.size >0 :
		df3.to_csv(target_file_name,mode="a" ,header=False, index=False, encoding="utf_8_sig") # 追加,header=False避免重复写入列名
	print("###### df3"  )
	print(df3)
	print(df3,file=log_file)

	

	


	








