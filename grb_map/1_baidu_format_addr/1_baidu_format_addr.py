#encoding=utf-8
'''

使用Place API把从文本中提取出的地址转换为对应的经纬度坐标，再使用Geocoding API把经纬度坐标转换为结构化地址。

//renbin.guo aded 

input :  拱北
output:  广东省珠海市香洲区侨光路3号


来源  http://blog.csdn.net/lianghq6/article/details/77776649
'''

from xml.etree import ElementTree  
import json  
import urllib.request
import re

search=urllib.parse.quote(u'拱北'.encode('utf-8'))              
region=urllib.parse.quote(u'珠海市'.encode('utf-8'))                 
ak = 'QPBpKbOkCqkkToYT5VaFixoz3hkykVBi'      ### 这里需要替换为你的ak 
url="http://api.map.baidu.com/place/v2/search?query=%s&region=%s&city_limit=true&output=json&ak=%s"%(search,region,ak)
print('\n#### url1 = \n',url)
req = urllib.request.urlopen(url)#JSON格式的返回数据
#print('#### req = ',req)
respan_json = req.read().decode("utf-8") #将其他编码的字符串解码成unicode
print('### respan_json = ',respan_json)  ###　json格式的字符串
respan_python = json.loads(respan_json)  ####  将json格式转为python数据结构
#print ('###temp = ',temp)
address = respan_python['results'][0]['address']#地址 在珠海地图中搜索'拱北',会但会多个地点，这里人工取了第一个。(实际上搜索会有很多也，这里的temp只是第一页)
location = respan_python['results'][0]['location'] #经纬度坐标
#print ('### address and location = ',address,location)
lat = str(location['lat'])#纬度坐标 
lng = str(location['lng'])#经度坐标 
#url2 = "http://api.map.baidu.com/geocoder/v2/?callback=renderReverse&location='+lat+','+lng+'&output=xml&pois=1&ak=%s"%(ak)  ## 也可以用xml
url2 = "http://api.map.baidu.com/geocoder/v2/?callback=renderReverse&location=%s,%s&output=json&pois=1&ak=%s"%(lat , lng,ak)
print('\n### url2 = \n',url2)



respan_str = urllib.request.urlopen(url2) #JSON格式的返回数据 这次返回的不是json，而是一个字符串了
#print('#### req = ',req)
respan_str = respan_str.read().decode("utf-8") #将其他编码的字符串解码成unicode
print('### respan_str = ',respan_str)  


pattern = re.compile(r'"formatted_address":"(.+?)"',re.S)
format_addr  = re.findall(pattern , str(respan_str))
#print('### form_addr = ',form_addr)
#print(type(form_addr))
print('format_addr = ',format_addr[0])


### ## 也可以用xml

#root = ElementTree.fromstring(res2)#解析XML时直接将字符串转换为一个#Element，解析树的根节点
#node_find = root.find('result/formatted_address')#find()用于查找属于某个tag的第一个element，这里查找结构化地址
#print(node_find.text)#输出结构化的地址
