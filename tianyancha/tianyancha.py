import requests
from lxml import etree


class TianYanCha():

    def __init__(self, url):

        self.url = url

        # 请求头
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
            "Cookie": "jsid=SEM-BAIDU-PZ-SY-20201109-BIAOTI; TYCID=3c59f8c03c7d11eb9def2f8baf70ca36; sajssdk_2015_cross_new_user=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22176571f0d65102-00ec6e84389a29-59442e11-921600-176571f0d66381%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E8%87%AA%E7%84%B6%E6%90%9C%E7%B4%A2%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E5%A4%A9%E7%9C%BC%E6%9F%A5%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fwww.baidu.com%2Fother.php%22%7D%2C%22%24device_id%22%3A%22176571f0d65102-00ec6e84389a29-59442e11-921600-176571f0d66381%22%7D; ssuid=5785470860; _ga=GA1.2.712634124.1607779424; _gid=GA1.2.284145277.1607779424; csrfToken=4MUN0aJbhfoTfv0pGPDCjxUL; bannerFlag=true; refresh_page=0; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1607784044; _gat_gtag_UA_123487620_1=1; relatedHumanSearchGraphId=23718623; relatedHumanSearchGraphId.sig=qzugegiZm0JJHXrAT_NmRMEXCaT3npwYnT8Pxodg06c; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1607784056",
            "Content-Type": "application/json; charset=UTF-8",
            "Accept-Encoding": "gzip, deflate, br",
        }

        self.item_list = {} # 存储队列

    def zhixing(self):

        self.response = requests.get(url=self.url, headers=self.headers).text  # 起始URL
        print("######### self.response = ")
        print(self.response)
        # html = self.response .text
        html = self.response
        print('### html = ',html)
        with open('tianyancha.html','w',encoding='utf-8') as f:
            f.write(html)


    def xiang_qing(self):

        import time
        time.sleep(1)
        self.response_content = requests.get(url=self.urls, headers=self.headers).text

        self.datalist = etree.HTML(self.response_content)

        self.datas = self.datalist.xpath('//div[@class="box -company-box "]')

        # 公司数据
        for self.data in self.datas:
            self.item_list["公司名称"] = self.data.xpath('./div[@class="content"]/div[@class="header"]/h1/text()')
            self.item_list['注册资本'] = self.data.xpath(
                '//*[@id="_container_baseInfo"]/table[2]/tbody/tr[1]/td[2]/div/text()')
            self.item_list['成立日期'] = self.data.xpath(
                '//*[@id="_container_baseInfo"]/table[2]/tbody/tr[2]/td[2]/div/text()')
            self.item_list['行业'] = self.data.xpath('//*[@id="_container_baseInfo"]/table[2]/tbody/tr[5]/td[4]/text()')
            self.item_list['注册地址    '] = self.data.xpath(
                '//*[@id="_container_baseInfo"]/table[2]/tbody/tr[10]/td[2]/text()')
            self.item_list['经营范围'] = self.data.xpath(
                '//*[@id="_container_baseInfo"]/table[2]/tbody/tr[11]/td[2]/span/text()')
            self.item_list['法定代表人'] = self.data.xpath(
                '//*[@id="_container_baseInfo"]/table[1]/tbody/tr[1]/td[1]/div/div[1]/div[2]/div[1]/a/@title')

        print(self.item_list)


if __name__ == '__main__':
        url = "https://www.tianyancha.com/search?key=三一重工" # 分页
        tianyancha = TianYanCha(url)
        tianyancha.zhixing()
