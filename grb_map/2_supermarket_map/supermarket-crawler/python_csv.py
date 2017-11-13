import csv
'''
	演示如何用python创建csv文件并写入
	http://blog.csdn.net/waple_0820/article/details/70049953
'''

#python2可以用file替代open
with open("test.csv","w") as csvfile: 
    writer = csv.writer(csvfile)

    #先写入columns_name
    writer.writerow(["index","a_name","b_name"])
    #写入多行用writerows
    writer.writerows([[0,1,3],[1,2,3],[2,3,4]])