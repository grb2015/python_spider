'''
  breif :         从江森自控的微信公众号(江森自控贤才堂)分享出来的连接，获取所有招聘数据
  create time:    rbg created  2020/03/20
  note  :
                  做的经过：
                    1.进入公众号 点击社会招聘  然后右上角分享链接 https://jci.tupu360.com/position/list?enter=menu&type=SOCIALRECRUITMENT&lang=zh_CN 
                    2.在谷歌浏览器对上面的连接进行网络调试分析,发现职位只能一次获取15个，url为
                      0-15号职位：  https://jci.tupu360.com/positionData/listInfo?type=SOCIALRECRUITMENT&offset=0
                      15-30号职位：  https://jci.tupu360.com/positionData/listInfo?type=SOCIALRECRUITMENT&offset=15
                      ...
                      这步可以得到职位的基本信息：['职位id', '职位名', '发布日期', '地点', '所属事业部', '职位类别', '月薪', ‘内推金'], 
                    3.获取职位的描述  https://jci.tupu360.com/positionData/detailDesc/职位id
                      需要注意的是：调试发现,浏览器直接访问该url需要登录后才能查看,所以需要提前注册，然后再打开该url，输入用户名和密码，登录后会得到一个loginWxInfo

                  遇到的问题：
                    1.如上述,获取详情页需要登录
                    2.即便是登录后，附上LoginwxInfo等cookie了，发现SSL错误。
                      解决方法: 还需要加上一个verify=False,requests.get(url,headers=header,verify=False) 不进行SSL验证
                    3.utf-8的csv文件excel无法打开。
                      解决方法1：with codecs.open('jsonControlJOb_allinfo.csv', 'w+', encoding='utf_8_sig')  设置为utf_8_sig utf-8 with BOM
                      解决方法2：在notepad++中更改编码方式为utf-8 with BOM


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



############################################################################################### 
'''
brief   :   获取职位总数
input   :   无
returns :   [int] 职位总数
'''
############################################################################################### 
def get_total_job_count():
  url= 'https://jci.tupu360.com/positionData/listInfo?type=SOCIALRECRUITMENT&offset=15'   
  header={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.3 Safari/537.36'}
  req = requests.get(url,headers=header)
  respan_json = req.content.decode('utf-8')  ### 注意这里如果要自己编码，必须content，而不能req.text
  respan_python = json.loads(respan_json)  ####  将json格式转为python数据结构
  return respan_python['result']['total']



############################################################################################### 
'''
brief   :   获取职位的基本信息
input   :   无
returns :   [list]  职位的基本信息
[ 
                ['职位id', '职位名', '发布日期', '地点', '所属事业部', '职位类别', '月薪', ‘内推金'], 
                ['职位id', '职位名', '发布日期', '地点', '所属事业部', '职位类别', '月薪', ‘内推金'],
                ...
            ]
note    :
          # 这个接口也可以获取职位的基本信息 这里的t=1584692369899是Utc时间，不带这个参数也可以。
          # # respan_python = get_job_baseinfo_single('https://jci.tupu360.com/positionData/detailInfo?curLang=zh_CN&t=1584692369899&id=5e1420fe744a262f3bf2a182&lang=zh_CN')
          # respan_python = get_job_baseinfo_single('https://jci.tupu360.com/positionData/detailInfo?curLang=zh_CN&id=5e1420fe744a262f3bf2a182&lang=zh_CN')
          这个接口是通过详情页的Url发现的
         
'''
############################################################################################### 
def get_job_baseinfo():
  base_info = [ ]
  header={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.3 Safari/537.36'}
  total_job = get_total_job_count()
  n = total_job//15 + 2 #循环次数
  for i in range(n):
    url= 'https://jci.tupu360.com/positionData/listInfo?type=SOCIALRECRUITMENT&offset=%s'%(i*15)   
      ##　获取所有的编号，存放在一个list里
    req = requests.get(url,headers=header)
    respan_json = req.content.decode('utf-8')  ### 注意这里如果要自己编码，必须content，而不能req.text
    respan_python = json.loads(respan_json)  ####  将json格式转为python数据结构
    for info in respan_python['result']['positions']:
      info_list = []
      info_list.append(info['pid'])
      info_list.append(info['pName'])
      info_list.append(info['pDate'])
      info_list.append(info['pCity'])
      info_list.append(info['pDepartment'])
      info_list.append(info['pFunction'])
      info_list.append(info['offeredSalary'])
      info_list.append(info['innerRecommendBonus'])
      base_info.append(info_list)
  print("base_info = ",file=log_file)
  print(base_info,file=log_file)
  print("--------------------------------------------",file=log_file)
  print("base_info = ")
  print(base_info)
  print("--------------------------------------------")
  return base_info
    


###############################################################################################   
'''
breif   : 获取职位的描述
input   : [str] 职位描述的url
returns : [str] 职位的描述
note:   ：需要登录才能访问该url ,在网站登录后，登录信息放在header的cookie里面即可
'''
############################################################################################### 
def get_job_desc(url):
  # header={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.3 Safari/537.36'}
  header={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.3 Safari/537.36',
   'Cookie':\
                'SESSION=c36978e7-ba34-49f1-a113-67f98a7d9d48; \
                 _sm_au_c=kkb4cAKIwKbGoIOXGjoEK7ZcgjFABRAccqa3uTWYng1UgAAAAVLg3WmKLB4w3kuYWX1bv29347z8wbRzi1k1qEkOObr8=; \
                loginWxInfo=70ef28ef9395ffe83d7232a50ba9a8ba2fbe9459d948c8653c58b3c4fb4362526fe39ffd9a706547367e63c9d5343e105f9d2cf2a92bf6ef;\
                 pgv_pvi=697453568; \
                 pgv_si=s4706393088'
                     }
  req = requests.get(url,headers=header,verify=False)
  # html = req.text
  html = req.content.decode('utf-8')  ### 注意这里如果要自己编码，必须content，而不能req.text
  with codecs.open('jsonControl.html','w',encoding = 'utf-8') as f:
    f.write(html) 
  soup = BeautifulSoup(html,'html5lib')
  ps = soup.find_all('p')
  job_desc = ''
  for p in ps:
    text =  p.get_text('\n','<br/>')
    job_desc += text
    print("\n\n",file=log_file)
    print("\n\n")
    print(job_desc,file=log_file)
    print(job_desc)
  return job_desc



# def get_job_baseinfo_single(url):
#   header={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.3 Safari/537.36',
#    'Cookie':\
#                 'SESSION=c36978e7-ba34-49f1-a113-67f98a7d9d48; \
#                  _sm_au_c=kkb4cAKIwKbGoIOXGjoEK7ZcgjFABRAccqa3uTWYng1UgAAAAVLg3WmKLB4w3kuYWX1bv29347z8wbRzi1k1qEkOObr8=; \
#                 loginWxInfo=70ef28ef9395ffe83d7232a50ba9a8ba2fbe9459d948c8653c58b3c4fb4362526fe39ffd9a706547367e63c9d5343e105f9d2cf2a92bf6ef;\
#                  pgv_pvi=697453568; \
#                  pgv_si=s4706393088'
#                      }
#   req = requests.get(url,headers=header,verify=False)
#   respan_json = req.content.decode('utf-8')   
#   respan_python = json.loads(respan_json)  
#   return respan_python





###############################################################################################   
'''
breif   : 获取职位的完整信息(["职位id","职位名","发布日期","地点","所属事业部","职位类别","月薪","内推金","职位描述"])
          保存到jsonControlJOb_allinfo.csv
input   : 无
returns : 无  结果保存到jsonControlJOb_allinfo.csv
note:   ：1.需要登录才能访问该url ,在网站登录后，登录信息放在header的cookie里面即可
          2.从get_job_baseinfo获取到每个职位的id,然后访问详情页
'''
############################################################################################### 
def get_job_all_info():
  base_info = get_job_baseinfo()
  all_info = base_info
  print(base_info,file=log_file)
  print(len(base_info),file=log_file)
  print(base_info)
  print(len(base_info))
  for i in range(len(all_info)):
    job_desc = get_job_desc('https://jci.tupu360.com/positionData/detailDesc/%s'%(base_info[i][0]))
    all_info[i].append(job_desc)
  with codecs.open('jsonControlJOb_allinfo.csv', 'w+', encoding='utf_8_sig') as market_file:   ### UTf-8 BOM编码 ,这样生成的csv excel才能直接打开。utf-8 excel会乱码
    writer = csv.writer(market_file)
    writer.writerow(["职位id","职位名","发布日期","地点","所属事业部","职位类别","月薪","内推金","职位描述"])
    for info_list in base_info:    
        writer.writerow(info_list)


if(__name__ == '__main__'):
    # log_file = open("./jsonControlJob.txt", 'w+') 
    log_file = codecs.open('jsonControlJOb_allinfo.csv', 'w+', encoding='utf_8')
    get_job_all_info()
    log_file.close()
