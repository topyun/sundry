import re

def filter_rawName(name):
    pattern =re.compile(u"[\u4e00-\u9fa5]+")
    result=re.findall(pattern,name)
    return result[0]

def write_name(allNamePath,memberPath):
    f = open(memberPath, 'r', encoding='utf-8')
    with open(allNamePath,'a',encoding='utf-8') as f_all:
        for nameline in f:
            if nameline != ' ':
                new_name = filter_rawName(nameline)
                print(new_name)
                f_all.write(new_name + '\n')

if __name__ == '__main__':
    allNamePath = '.txt'
    memberPath1 = '.txt'
    memberPath2 = '.txt'
    memberPath_list = [memberPath1, memberPath2]
    for path in memberPath_list:
        write_name(allNamePath,path)
