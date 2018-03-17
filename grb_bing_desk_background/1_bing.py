"""A simple script to import the daily picture of bing"""  
# http://blog.csdn.net/wbb1075421270/article/details/51810282?locationNum=4&fps=1
# 
# 将本文件打包成一个exe可执行程序 1_bing.exe :
#   pyinstaller --onefile 1_bing.py
import urllib.request  
import re  
import time  
import os


## rbguo added  2018-03-10 begin
import ctypes
def set_img_as_wallpaper(filepath):  ## 貌似要绝对地址
    ctypes.windll.user32.SystemParametersInfoW(20, 0, filepath, 0)
#set_img_as_wallpaper("G:\\study\\python_spider\\grb_bing_desk_background\\2018_03_10.jpg") ## 貌似要绝对地址
## rbguo added  2018-03-10 end


###直接下载到当前路径 返回文件名(按时间命名)
def downloader_picture():  
	pic_file_name = time.strftime('%Y_%m_%d', time.localtime(time.time()))+'.jpg'
	if os.path.exists(pic_file_name):
		print(pic_file_name+' already exits,need not to download')
	else:
		"""We use the xml api provided by bing to get the pic url"""
		hostname = "http://cn.bing.com/HPImageArchive.aspx?idx=0&n=1"
		req = urllib.request.Request(hostname)              ### 1.这里得到的是一个req对象
		#print(req)
		##print('------------------------------\n\n')
		webpage = urllib.request.urlopen(req)
		##print(webpage) 
		content = str(webpage.read())                       ### 2.这里真正得到了上面host中的内容，并且是以字节表示的字符串。
		#f= open('webpage.html','w')
		#f.write(content)
		#print(content)
		url_tail = re.search(r'<url>[^\s]*</url>', content) ### 3.在上面的网页内容中需要url相对地址
		#print(url_tail.group())   # <url>/az/hprichbg/rb/HawaiiWave_ZH-CN13164844408_1366x768.jpg</url>
		url = 'http://cn.bing.com' + str(url_tail.group())[5:-6]# str(url_tail.group())[5:-6] = /az/hprichbg/rb/HawaiiWave_ZH-CN13164844408_1366x768.jpg
		print(url)    ### 构建保存的文件名，并调用urlretrieve进行下载
		urllib.request.urlretrieve(url, pic_file_name)  
	return pic_file_name

def main():
	pic_file_name = downloader_picture()  
	pwd = os.getcwd()
	set_img_as_wallpaper(pwd+"\\"+pic_file_name)
if __name__ == '__main__':  
    main()
#   pyinstaller --onefile 1_bing.py  to package 1_bing.py to exe