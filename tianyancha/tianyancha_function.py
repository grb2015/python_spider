# brief     :   输入不规则的公司名字，在天眼查里面获取公司规范化的全名
# history   :   rbg created 20201213
# note      :   

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
##################################################################
#   breif   :   模拟在天眼查首页输入框中输入关键字查询,得到返回结果列表
#   input   :   keywords    :   [str]   要搜索的关键词
#   returns :   response    ：  [str}   网页数据
#   note    :
##################################################################
def get_complete_compnay_name(keywords):
    proxies = { } ## 让每次最先无代理的
    proxy_pool = []
    with open('proxy.txt','r+') as f:
      lines = f.readlines() 
    for line in lines:
      proxy_pool.append(line.strip())  ### 去掉'\n'
    print(proxy_pool)
    try:
        url = "https://www.tianyancha.com/search?key=%s"%(keywords) 
        headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
                "Cookie": "jsid=SEM-BAIDU-PZ-SY-20201109-BIAOTI; TYCID=3c59f8c03c7d11eb9def2f8baf70ca36; sajssdk_2015_cross_new_user=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22176571f0d65102-00ec6e84389a29-59442e11-921600-176571f0d66381%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E8%87%AA%E7%84%B6%E6%90%9C%E7%B4%A2%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E5%A4%A9%E7%9C%BC%E6%9F%A5%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fwww.baidu.com%2Fother.php%22%7D%2C%22%24device_id%22%3A%22176571f0d65102-00ec6e84389a29-59442e11-921600-176571f0d66381%22%7D; ssuid=5785470860; _ga=GA1.2.712634124.1607779424; _gid=GA1.2.284145277.1607779424; csrfToken=4MUN0aJbhfoTfv0pGPDCjxUL; bannerFlag=true; refresh_page=0; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1607784044; _gat_gtag_UA_123487620_1=1; relatedHumanSearchGraphId=23718623; relatedHumanSearchGraphId.sig=qzugegiZm0JJHXrAT_NmRMEXCaT3npwYnT8Pxodg06c; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1607784056",
                "Content-Type": "application/json; charset=UTF-8",
                "Accept-Encoding": "gzip, deflate, br",
        }
        response = requests.get(url=url, headers=headers,proxies=proxies).text  # 起始URL
        # print("### response = ",response)
    except Exception as e:
        print("###### e")

    print("######### response = ")
    print(response)
    # 写数据结果到html文件中
    print('### response = ',response)
    with open('tianyancha.html','w',encoding='utf-8') as f:
        f.write(response)
    complete_company_name = None
    try:
        soup = BeautifulSoup(response,'lxml')
        company_tags = soup.find_all(name='div',attrs={"class":"header"})
        print('########### table_tags[0] = ',company_tags[0])
        print('########### table_tags[0].a.get_text() = ',company_tags[0].a.get_text())
        complete_company_name = company_tags[0].a.get_text()
    except Exception as e:
        print(" ### e = ",e)
        pass
    return complete_company_name

##################################################################
#   breif   :   读取csv文件
#   input   :   keywords    :   [str]   要搜索的关键词
#   returns :   response    ：  [str}   网页数据
#   note    :
##################################################################
def read_csv():
    df = pd.read_csv('customer_info_origan.csv',encoding = 'gbk')
    # print(" df = ",df)
    # print(" df['单位名称'] = ",df['单位名称'])
    full_names = []
    for origan_name in  df['单位名称']:
        print("origan_name = ",origan_name) 
        full_name = get_complete_compnay_name(origan_name)
        print("full_name = ",full_name) 
        full_names.append(full_name)
        time.sleep(4)
    df['full_name'] = full_names


if __name__ == '__main__':
    fullname = get_complete_compnay_name("中国人寿保险股份有限公司河南省分公司")
    print("fullname = ",fullname)
#    read_csv()