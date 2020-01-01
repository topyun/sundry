import requests
from bs4 import BeautifulSoup as bs
import os
from conf.bangongwang_url import BanGongWang_Site_education
from conf.filepath import load_file_path
from conf.create_file import download_file
from conf.logmodule import LogModule

# ---------------- 进入学生页面 -------------------- #
logger = LogModule()

def download_work(sd_url,sd_name,headers,cookie):
    html = requests.get(sd_url,headers=headers,cookies=cookie).text
    soup1 = bs(html,'lxml')
    tables1 = soup1.find_all('fieldset',class_='fieldset')
    table_num = len(tables1)
    tables1 = str(tables1)
    tables_soup1 = bs(tables1, 'lxml')
    # 判断提交是否为空
    admit_flag = True
    flag = 1
    if table_num == 5:
        flag = 2
    if not tables_soup1.find(text='作业内容附件'):
        admit_flag = False
        print("\n 该学生[" + sd_name + "]提交作业为空！\n")

    else:
        print(tables_soup1.find_all('td')[1].text) # <td>课后习题1</td>
        work_all = tables_soup1.select('tr')[flag].find_all('tr') # 所有行的作业、】
        work_num = len(work_all[1:])
        print("提交作业数量： " + str(work_num))
        url_size_dict = {}
        for work_one in work_all[1:]:
            work_download_url = work_one.find_all('td')[0].a['href'] # 作业下载链接
            work_name = work_one.find_all('td')[0].text.strip()
            print('work_download_url: ' + work_download_url)
            print('work_explation: ' + work_one.find_all('td')[1].text.strip())
            work_size = work_one.find_all('td')[2].text
            print('work_size: ' + work_size)
            # 判断提交作业是否重复，按照文件大小判断，大小相同判为一致
            if not url_size_dict.__contains__(work_size):
                url_size_dict[work_size] = (work_download_url,work_name)

        if work_num > len(url_size_dict):
            print("有重复文件")

        # 下载文件
        work_download_url_set = [x for x in url_size_dict.values()]
        if len(work_download_url_set) > 1: # 多个文件

            print("建立文件夹")
            file_name_path = load_file_path + '\\' + sd_name
            if not os.path.exists(file_name_path):
                os.makedirs(file_name_path)

            for i in range(len(work_download_url_set)):
                work_download_url = work_download_url_set[i][0]
                work_download_url = BanGongWang_Site_education + work_download_url
                # 加后缀
                extend_name = '.' + work_download_url_set[i][1].split('.')[1]
                # 文件名
                full_file_path = file_name_path + '\\' + sd_name + '_' + str(i) + extend_name
                r = requests.get(work_download_url,headers=headers,cookies=cookie)

                download_file(full_file_path, r)

            print(sd_name + " 作业已下好")
            logger.info(sd_name + " 作业已下好")

        else: # 单个文件直接下载建立
            print(work_download_url_set)
            work_download_url = work_download_url_set[0][0]
            work_download_url = BanGongWang_Site_education + work_download_url
            extend_name = '.' + work_download_url_set[0][1].split('.')[1] # 加后缀
            full_file_path = load_file_path + '\\' + sd_name + extend_name # 文件名
            r = requests.get(work_download_url,headers=headers,cookies=cookie)

            download_file(full_file_path, r)

            print(sd_name + " 作业已下好")
            logger.info(sd_name + " 作业已下好")

    return admit_flag
