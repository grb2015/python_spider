import numpy as np    
import matplotlib.mlab as mlab    
import matplotlib.pyplot as plt  
import codecs

###  从表格中获取Index列的不同的值，返回一个set
def get_unique_item_set(list_lines,index):
    unique_items_set = set([])
    for list_line in list_lines:
        print(list_line)
        item = list_line[index]   ### 
        if item:
            unique_items_set.add(item)
        else:
            unique_items_set.add('未知地区')
    return unique_items_set
####  从list_lines表格中获取第index列的数据透视表
####  index = 2 则获取的是一个市所有的县的上市公司透视表{'滨江区':22,'上河区'：12...}
#     index = 3  获取的是一个市所有行业的数据透视表 {‘互联网’：9,'制药':8}
def get_unique_item_amount_dict(list_lines,index):  
    dict_colurmn_index = {}
    unique_items = get_unique_item_set(list_lines,index)
    for item in unique_items:     
        dict_colurmn_index[item]=0 ####  初始化为0
    for list_line in list_lines:
        item = list_line[index]
        if item:
            dict_colurmn_index[item] = dict_colurmn_index[item] +1
        else:
            dict_colurmn_index['未知地区'] = dict_colurmn_index['未知地区'] +1

    #print(dict_colurmn_index)
    return dict_colurmn_index   

####从csv读取数据,存放在list_lines里面
def get_list_lines_from_csv(csvfile):
    with codecs.open(csvfile,'r+',encoding='utf-8') as f:  
        lines = f.readlines()
    list_lines = []
    for line in lines[1:]:
        print('line = ' , line)
        line = line.strip()
        list_line = line.split(',')
        list_lines.append(list_line)
    return list_lines
#def barh_plot2(): 
def barh_plot2(labels,data): 
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    ### a = 1 
    #b =2 
    #c = 3
    #d = 4
    
    #labels= ['a','b','c','d']
    #data=[1,2,3,4]
    idx = np.arange(len(data))
    fig = plt.figure(figsize=(12,12))  ### 画框大小
    plt.barh(idx, data, color='b',alpha=0.6)
    plt.yticks(idx+0.4,labels)
    plt.grid(axis='x')
    plt.xlabel('人数')
    plt.ylabel('地区')
    plt.title('微信好友地点分布')
    plt.show()
list_lines = get_list_lines_from_csv('friends_info_format.csv')
print(list_lines)
addr_dict = get_unique_item_amount_dict(list_lines,3)
X = []
Y = []
print('#### addr_dict = ',addr_dict)
for key in addr_dict.keys():
    print(key)
    print(addr_dict[key])
    X.append(key)
    Y.append(addr_dict[key])
print(X)
print(Y)

barh_plot2(X,Y)