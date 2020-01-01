# 微信点名  导入名单用
from bs4 import BeautifulSoup as bs

def getStuName(html_path,file_name):
    f = open(html_path,'r',encoding='utf=8')
    soup = bs(f.read(),'lxml')
    print(soup.title)
    tables = soup.find_all('div',class_='member ng-scope')
    num = len(tables)
    print('加上 [' + str(num) + ']人')
    member_list = []
    for div in tables:
        name = div.text.strip()
        member_list.append(name)
    print(member_list)
    with open(file_name,'w',encoding='utf-8') as f:
        for i in member_list:
            f.write(i + '\n')

if __name__ == '__main__':
    html_path_1 = r'.html'
    html_path_2 = r'.html'
    file_name_1 = '.txt'
    file_name_2 = '.txt'
    file_name_list = [(html_path_1,file_name_1), (html_path_2,file_name_2)]
    for html_pathAndfile_name in file_name_list:
        getStuName(html_pathAndfile_name[0],html_pathAndfile_name[1])
