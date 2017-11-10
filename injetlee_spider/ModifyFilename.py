##批量修改文件名    对当前超过50字节的文件(文件夹)只截取50字节来重命名  只递归2层  (这个例子没什么意义)
import os
dir = os.getcwd()   ## pwd
subdir = os.listdir(dir)  ## 得到当前路径下所有文件(文件夹)
for i in subdir:
    path = os.path.join(dir, i)		### 获取改文件的完整路径
    if os.path.isdir(path):		### 如果当前是文件夹
        end_dir = os.listdir(path)
        for i in range(len(end_dir)):
            newname = end_dir[i][0:50] ### 只得到当前文件(文件夹的前50个字节)  end_dir[i]就是当前文件的名称的字符串
            os.rename(os.path.join(path, end_dir[		### 对当前文件重命名
                      i]), os.path.join(path, newname))
