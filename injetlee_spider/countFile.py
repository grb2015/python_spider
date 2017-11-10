### 对目录下所有文件计数(文件夹不认为是文件，会递归下去找文件)
import os
result = []
def get_all(cwd):
    get_dir = os.listdir(cwd)  #遍历当前目录，获取文件列表
    for i in get_dir:  
      #  print('i =%s'%i)        
        sub_dir = os.path.join(cwd,i)  # 把第一步获取的文件加入路径
        #print('sub_dir = %s'%sub_dir)
        if os.path.isdir(sub_dir):     #如果当前仍然是文件夹，递归调用
            get_all(sub_dir)
        else:
            ax = os.path.basename(sub_dir)  #如果当前路径不是文件夹，则把文件名放入列表
           # print('ax = %s'%ax)
            result.append(ax)  ### result 存放到底是哪些文件
            


            
if __name__ == "__main__": 
    cur_path = os.getcwd()   #当前目录
   # print('cur_path = %s'%cur_path)
    get_all(cur_path)

    print('\n\ntotal files : %s\n\n'%len(result))   #对列表计数
    print("they are : %s"%result)