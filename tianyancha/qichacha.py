#-*- coding-8 -*-
import requests
import lxml
import sys
from bs4 import BeautifulSoup
import time
import urllib
 
def craw(url,key_word,x):
    User_Agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'
    headers = {
            'Host':'www.qichacha.com',
            'Connection': 'keep-alive',
            'Accept':r'text/html, */*; q=0.01',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent':r'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
            'Accept-Encoding':'gzip, deflate, br',
            'Accept-Language':'zh-CN,zh;q=0.9',
            'referer':'https://www.qcc.com/web/search?key=%E4%B8%AD%E8%81%94%E9%87%8D%E7%A7%91',
            'Cookie':r'acw_tc=d35ba34716077835164942267e5d9686a29649a023a835b1c1ee03073e; QCCSESSID=8sipq5jith9rf9tc8u760q32i4; UM_distinctid=176575dc75b381-0dc3060807be8e-59442e11-e1000-176575dc75c2c4; CNZZDATA1254842228=1374206502-1607780862-null%7C1607780862; hasShow=1; _uab_collina=160778353857793069527369; zg_did=%7B%22did%22%3A%20%22176575dea06e2-073e9e218330f7-59442e11-e1000-176575dea0782%22%7D; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201607783541268%2C%22updated%22%3A%201607783574822%2C%22info%22%3A%201607783541283%2C%22superProperty%22%3A%20%22%7B%5C%22%E5%BA%94%E7%94%A8%E5%90%8D%E7%A7%B0%5C%22%3A%20%5C%22%E4%BC%81%E6%9F%A5%E6%9F%A5%E7%BD%91%E7%AB%99%5C%22%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22diag.qichacha.com%22%2C%22cuid%22%3A%20%22undefined%22%7D',
            }
 
    try:
        response = requests.get(url,headers = headers)
        print("####### response = ")
        print(response)
        if response.status_code != 200:
            response.encoding = 'utf-8'
            print(response.status_code)
            print('ERROR')    
        soup = BeautifulSoup(response.text,'lxml')
    except Exception as e:
        print('请求都不让，这企查查是想逆天吗？？？e =',e)

         
if __name__ == '__main__':
    global g_name_list
    global g_tag_list
    global r_name_list
    global g_money_list
    global g_date_list
    global r_email_list
    global r_phone_list
    global g_addr_list
    global g_state_list
     
    g_name_list=[]
    g_tag_list=[]
    r_name_list=[]
    g_money_list=[]
    g_date_list=[]
    r_email_list=[]
    r_phone_list=[]
    g_addr_list=[]
    g_state_list=[]
 
    key_word = "中联重科"
    num = 1
    sleep_time = 1
    key_word = urllib.parse.quote(key_word)
     
    print('正在搜索，请稍后')
     
    url = r'https://www.qcc.com/web/search?key=%E4%B8%89%E4%B8%80%E9%87%8D%E5%B7%A5'
    s1 = craw(url,key_word,1)
    print("############## s1 = ")
    print(s1)