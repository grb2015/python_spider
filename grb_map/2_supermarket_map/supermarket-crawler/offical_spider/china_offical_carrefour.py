'''
  通过家乐福官网 爬取家乐福全国所有的门店信息

  原理 ： 通过header的cookie选项来指定要获取的城市，即_C4CookieKeyCityNum={}字段
  todo : 
    1.连续发请求会出错，必须time.sleep() 而且time.sleep()也不是很好，要等很久还不一定能取得  rbguo fix 2017-11-29   使用代理
    2.for i in range(10): 这里应该要取得全国城市的数量 rbguo fix 2017-11-29   使用代理
    3.todo  上海6个页面返回的都是一个第一个页面了         rbguo fix 2017-11-29  
    4.需要提高速度，减小sleep()时间。另外，file_log有些没有打上。
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
import random

def get_carrefour():

  with codecs.open('china_offical_carrefour.csv', 'w+', encoding='utf-8') as market_file:  
    writer = csv.writer(market_file)
    writer.writerow(["品牌","商场名","地址"])
    #http://www.carrefour.com.cn/ws/city.ashx   这个网址可查询citynum对应的cityname
    proxy_pool = []
    with open('proxy.txt','r+') as f:
      lines = f.readlines() 
    for line in lines:
      proxy_pool.append(line.strip())  ### 去掉'\n'
    print(proxy_pool)

    #proxies = { "http": "223.15.179.137:3128"} 
    proxies = { } ## 让每次最先无代理的
    for i in range(100):
      i = i+1
      print("### city num = ",i)


      header={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:57.0) Gecko/20100101 Firefox/57.0',
               'Cookie':\
                'ASP.NET_SessionId=szgsnf3wzixv3b01vikajhps; \
                 _C4CookieKeyCityNum={}; \
                 Hm_lvt_ad969e28d61c1bff627763d1cccefe7b=1511771124; \
                 Hm_lpvt_ad969e28d61c1bff627763d1cccefe7b=1511771124;\
                 __utmt=1;\
                  __utma=148273317.89550502.1511771124.1511771124.1511771124.1;\
                   __utmb=148273317.1.10.1511771124;\
                    __utmc=148273317;\
                     __utmz=148273317.1511771124.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)'.format(i)}
     

if(__name__ == '__main__'):
    log_file = open("./china_carrfour_log.txt", 'w+') 
    get_carrefour()
    log_file.close()
