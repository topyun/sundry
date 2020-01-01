# 分组作业
import shutil
import os
import re
import random
from classification.id2name import get_id2name_dict

#获取指定文件中文件名
def get_filename(filetype):
    name =[]
    final_name_list = []
    source_dir=os.getcwd()#读取当前路径
    for root,dirs,files in os.walk(source_dir):
        for i in files:
            if filetype in i:
                name.append(i.replace(filetype,''))
    final_name_list = [item +filetype for item in name]
    print(final_name_list)
    return final_name_list #返回由文件名组成的列表

#筛选文件，利用正则表达式
def select_file(str_cond,file_name_list):
    select_name_list =[]
    part1 = re.compile(str_cond)#正则表达式筛选条件
    for file_name in file_name_list:
        if len(part1.findall(file_name)):#判断其中一个文件名是否满足正则表达式的筛选条件
            select_name_list.append(file_name)#满足，则加入列表
    return select_name_list#返回由满足条件的文件名组成的列表

#复制指定文件到另一个文件夹里，并删除原文件夹中的文件
def cope_file(select_file_name_list,old_path,new_path):
    for file_name in select_file_name_list:
        shutil.copyfile(os.path.join(old_path,file_name),os.path.join(new_path,file_name))#路径拼接要用os.path.join，复制指定文件到另一个文件夹里
        os.remove(os.path.join(old_path,file_name))#删除原文件夹中的指定文件文件
    return select_file_name_list

#主函数
def main_function(filetype,str_cond,old_path,new_path):
    final_name_list = get_filename(filetype)
    select_file_name_list = select_file(str_cond,final_name_list)
    cope_file(select_file_name_list,old_path,new_path)
    return select_file_name_list

# 获取文件名并返回奇偶文件
def get_filename_1(src_path,sd_dict,oddeven):
    final_name_list = []
    for names in os.listdir(src_path):
        # print(names)
        name,ext = os.path.splitext(names)
        # print(name)
        # pass  # 奇偶分类
        if int(sd_dict[name]) % 2 == oddeven:
            final_name_list.append(names)
    print(final_name_list)
    return final_name_list

# 获取文件名(不含后缀)
def get_filename_2(src_path):
    final_name_list = []
    for names in os.listdir(src_path):
        # print(names)
        name,ext = os.path.splitext(names)
        print(name)

def isdir(path):
    if os.path.isdir(path):
        print ("it's a directory")
        return True
    elif os.path.isfile(path):
        print ("it's a normal file")
        return False

# 随机分配作业
def random_copyfile(srcPath,dstPath,numfiles):
    name_list=list(os.path.join(srcPath,name) for name in os.listdir(srcPath))
    random_name_list=list(random.sample(name_list,numfiles))
    if not os.path.exists(dstPath):
        os.mkdir(dstPath)
    for oldname in random_name_list:
        shutil.copyfile(oldname,oldname.replace(srcPath, dstPath))

# 复制指定文件到另一个文件夹里，并删除原文件夹中的文件
def cope_FileOrDir(select_file_name_list,old_path,new_path):
    for file_name in select_file_name_list:
        if not isdir(os.path.join(old_path,file_name)):
            shutil.copyfile(os.path.join(old_path,file_name),os.path.join(new_path,file_name))#路径拼接要用os.path.join，复制指定文件到另一个文件夹里
        else:
            shutil.move(os.path.join(old_path,file_name),os.path.join(new_path,file_name))
        # os.remove(os.path.join(old_path,file_name))#删除原文件夹中的指定文件文件
    return select_file_name_list
# get_filename_1(r'H:\编译原理助教\已批改作业\作业一\第一次作业后半部分\后半部分')

if __name__ == '__main__':

    # copy oral_path -> old_path file
    # oral_path = ''
    # old_path = r''
    # new_path = r''
    # oddeven = 0  # 按奇数改 0为偶数
    #
    # # 复制原文件 oral_path -> old_path
    # shutil.copytree(oral_path,old_path)
    # # 创建新文件 new_path
    # os.makedirs(new_path, exist_ok=True)
    # select_file_name_list = get_filename_1(oral_path,get_id2name_dict(),oddeven)
    # cope_FileOrDir(select_file_name_list, old_path, new_path)
    #
    # # 删除test文件 remove old_path file
    # shutil.rmtree(old_path)
    # # get_filename_2(r'D:\编译原理助教\作业\作业三\学生作业')
    # print('批改作业已分好')

    # srcPath = r''
    # dstPath = r''
    # random_copyfile(srcPath, dstPath, 20)

    get_filename_2('')
    