import psutil
import os
from influxdb import InfluxDBClient
import time,math,random

###  renbin.guo added    2017-11-10
###  需要先安装influxdb数据库(概念类似mysql)。centos可用yum安装。安装完后需要先启动数据库服务进程 service influxd start 
###  然后需要安装python-influxdb 用于连接influxdb . pip3 install  influxdb
'''
influxdb的一点用法：
参考： https://my.oschina.net/u/213000/blog/865884

'''


#获取当前运行的pid
p1=psutil.Process(os.getpid()) 


from influxdb import InfluxDBClient
import time,math,random

client = InfluxDBClient('localhost', 8086, 'root', 'root', 'xxyyxx4')  ### 链接数据库，使用xxyyxx4数据库(这里会创建.)  root  root 为用户名和密码(默认的)'
client.create_database('xxyyxx4')
while True:
    a = psutil.virtual_memory().percent  #内存占用率
    print('a = %s'%a)


    b = psutil.cpu_percent(interval=1.0) #cpu占用率
    print('b = %s'%b)

    json_body = [
        {
            "measurement": "cpu_load_short",
            "tags": {
                "host": "server01",
                "region": "us-west"
            },
            #"time": "2009-11-10T23:00:00Z",  ### 
            "fields": {
                "cpu": b,
                "mem": a
            }
        }
    ]
    client.write_points(json_body)
    result = client.query('select cpu,mem from cpu_load_short;')  ### cpu_load_short类似于表名，host ,region cpu mem 类似于列
    print("Result: {0}".format(result))
    time.sleep(2)
