"""Supermarket Crawler

Crawl the locations of supermarkets in 26 cities.


renbin.guo added:
    bug 
        1.抓到的数据不全  比如拿上海麦德龙来分析就知道了(这个貌似不是bug )
                          解释：
                          程序中发出的url为
                          http://api.map.baidu.com/place/v2/search?q=%E9%BA%A6%E5%BE%B7%E9%BE%99&region=%E4%B8%8A%E6%B5%B7&page_size=20&page_num=0&output=json&ak=QPBpKbOkCqkkToYT5VaFixoz3hkykVBi
                          得到的确实只有9条。
                          而用浏览器搜索会得到11条,其中有条是冒牌的,另外有两条地点在一起.
    TODE : 
        1.将数据导入到excel中进行分析，存为csv用excel打开发现所有内容都在一个单元格
        2.麦德龙(常熟商场店) 31.684721 120.789353 经济技术开发区通港路99号  这个就不知道是哪里了，需要对地址进行结构化 /省/市/区/路/号
        3.爬取各家超市官网，统计数据，与地图的数据做对比。
"""

import codecs
import requests
import time

def supermarket_crawler():
    """Supermarket Crawler
    """

    #cities = ['上海', '南京', '无锡', '常州', '苏州', '南通', '盐城', '扬州', '镇江', '泰州', '杭州', '宁波', '嘉兴', '湖州', '绍兴', '金华', '舟山', '台州', '合肥', '芜湖', '马鞍山', '铜陵', '安庆', '滁州', '池州', '宣城']
    #supermarkets = ['苏果', '家乐福', '世界联华', '沃尔玛', '欧尚', '大润发', '金润发', '卜蜂莲花', '华润万家', '永辉', '金鹰', '八佰伴', '华联', '好又多', '麦德龙']
    #cities = ['上海', '南京', '无锡', '常州', '苏州']
    cities = ['上海']
    supermarkets = ['家乐福','沃尔玛','大润发',  '麦德龙']
    # test_cities = ['上海', '南京']
    # test_supermarkets = ['苏果', '家乐福']
    page_size = 20
    ak = 'QPBpKbOkCqkkToYT5VaFixoz3hkykVBi' 

    # 要实现写入时编码为UTF-8，应使用codecs模块的open
    with codecs.open('supermarkets.txt', 'w', encoding='utf-8') as market_file:

        for city in cities:
            for supermarket_name in supermarkets:
                time.sleep(1)  ### renbin.guo added 必须加这个，不然我这里会发现supermarket_json = requests.get(url_total).json() 会exception
                url_total = 'http://api.map.baidu.com/place/v2/search?q={0}&region={1}&page_size={2}&output=json&ak={3}'.format(supermarket_name, city, page_size,ak)
                try:
                    
                    print('### url_total = ',url_total)
                    supermarket_json = requests.get(url_total).json()   ### 我感觉requests直接把json转为了python数据结构
                    supermarket_num =  supermarket_json['total']
                    #print('##### type  supermarket_json = ',type(supermarket_json))  ##＃这里直接得到dict 
                    print('##### supermarket_json = ',supermarket_json)
                    print('#### supermarket_total = ',supermarket_num)

                    page_total = supermarket_num // 20 + 1
                    print('#### page_total = ',page_total)
                    
                    for page_num in range(page_total):
                        url = 'http://api.map.baidu.com/place/v2/search?q={0}&region={1}&page_size={2}&page_num={3}&output=json&ak={4}'.format(supermarket_name, city, page_size, page_num,ak)
                        print('### url = ',url)
                        supermarket_json = requests.get(url).json()
                        print('##### supermarket_json2 = ',supermarket_json)

                        rest_size = page_size  ##　还剩余多少记录，默认为20
                        if(page_num == page_total - 1):
                            rest_size = supermarket_num - page_num * page_size  ## 如果是最后一页了，那么剩余的页数就不是20,而是小于20，要计算
                        for supermarket_num in range(rest_size):
                            try:
                                supermarket = supermarket_json['results'][supermarket_num]
                                print(city, supermarket_name)
                                ## windows换行需要\r\n  linux \n
                                write_buf = '{0}   {1}   {2} {3}\r\n'.format(supermarket['name'], supermarket['location']['lat'], supermarket['location']['lng'], supermarket['address'])
                                #print('write_buf = ',write_buf)
                               #print('type write_buf = ',type(write_buf))
                                #market_file.write('{0}   {1}   {2} {3}\r\n'.format(supermarket['name'], supermarket['location']['lat'], supermarket['location']['lng'], supermarket['address']))
                                market_file.write(write_buf)
                            except Exception as crawl_error:
                                print("########### except 1######################")
                                pass

                except Exception as crawl_error:
                    print("########### except 2######################")
                    pass

if(__name__ == '__main__'):
    supermarket_crawler()
