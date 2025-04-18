# -*- coding: utf-8 -*-
# @Author: Teiei
# @Date:   2025-4-18 9:00:55
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
import json

def load_divisions(json_file):
    """加载行政区划JSON文件"""
    with open(json_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_division_info(code):
    """
    根据行政编码返回省市区信息
    :param divisions_data: 加载的JSON数据
    :param code: 行政编码（如310101）
    :return: 字符串，如"上海市，黄浦区"
    """
    divisions_data = load_divisions('area.json')
    code = str(code)  # 确保是字符串类型
    
    # 处理不同长度的编码
    if len(code) == 6:  # 区县级
        province_code = code[:2] + '0000'
        city_code = code[:4] + '00'
    elif len(code) == 4:  # 市级
        province_code = code[:2] + '0000'
        city_code = code
    elif len(code) == 2:  # 省级
        province_code = code + '0000'
        city_code = None
    else:
        return "无效的行政编码"
    
    province_name = ""
    city_name = ""
    district_name = ""
    
    # 查找省份
    for province in divisions_data:
        if province['code'] == province_code[:2]:
            province_name = province['name']
            
            # 查找城市
            if 'children' in province:
                for city in province['children']:
                    if city_code and city['code'] == city_code[:4]:
                        city_name = city['name']
                        
                        # 查找区县
                        if 'children' in city:
                            for district in city['children']:
                                if len(code) == 6 and district['code'] == code:
                                    district_name = district['name']
                                    break
                        break
            break
    
    # 组装结果（避免直辖市重复显示）
    result = []
    if province_name:
        result.append(province_name)
    if city_name and city_name != province_name:  # 直辖市城市名和省份名相同
        result.append(city_name)
    if district_name:
        result.append(district_name)
    
    return "，".join(result) if result else "未找到对应的行政区域"

# 使用示例
if __name__ == "__main__":
    # 加载JSON文件
    divisions_data = load_divisions('area.json')
    
    # 测试查询
    print(get_division_info(310101))  # 上海市，市辖区，黄浦区
    print(get_division_info(510104))  # 上海市，市辖区，黄浦区
    # print(get_division_info(divisions_data, 110105))  # 北京市，朝阳区
    # print(get_division_info(divisions_data, 4403))    # 广东省，深圳市
    # print(get_division_info(divisions_data, 50))      # 重庆市