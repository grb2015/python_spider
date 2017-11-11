"""A simple script to import the daily picture of bing"""  
# http://blog.csdn.net/wbb1075421270/article/details/51810282?locationNum=4&fps=1
import urllib.request  
import re  
import time  


def main():  
    """We use the xml api provided by bing to get the pic url"""  
    hostname = "http://cn.bing.com/HPImageArchive.aspx?idx=0&n=1"  
    req = urllib.request.Request(hostname)              ### 1.这里得到的是一个req对象


    #print(req)
    #print('------------------------------\n\n')
    webpage = urllib.request.urlopen(req)  
    #print(webpage)
    content = str(webpage.read())                       ### 2.这里真正得到了上面host中的内容，并且是以字节表示的字符串。
    #f= open('webpage.html','w')
    #f.write(content)
    #print(content)


    url_tail = re.search(r'<url>[^\s]*</url>', content) ### 3.在上面的网页内容中需要url相对地址
    #print(url_tail.group())   # <url>/az/hprichbg/rb/HawaiiWave_ZH-CN13164844408_1366x768.jpg</url>


    
                                                        ### 4.得到绝对的url地址 
    url = 'http://cn.bing.com' + str(url_tail.group())[5:-6]    # str(url_tail.group())[5:-6] = /az/hprichbg/rb/HawaiiWave_ZH-CN13164844408_1366x768.jpg
    print(url)               

                                                        ### 构建保存的文件名，并调用urlretrieve进行下载
    pic_file_name = time.strftime('%Y_%m_%d', time.localtime(time.time()))  
    urllib.request.urlretrieve(url, pic_file_name+url[-4:])   #  url[-4:] =.jpg  
  
if __name__ == '__main__':  
    main()
