import requests
from bs4 import BeautifulSoup as bs
import time
import random
import os


load_file_path = r''
headers = {
    'User-Agent':'Mozilla/5.0 '
}
# 保密
cookie_oral = ''
cookie_oral_0 = ''


# ---------------- 转换cookie --------------------- #
def cookie_to_dict(cookie):
    cookie_dict = {}
    items = cookie.split(';')
    for item in items:
        key = item.split('=')[0].replace(' ', '')
        value = item.split('=')[1]
        cookie_dict[key] = value
    return cookie_dict

cookie = cookie_to_dict(cookie_oral_0)


# ---------------- 进入学生页面 -------------------- #
def download_work(sd_url,sd_name):

    admit_list = []
    html = requests.get(sd_url,headers=headers,cookies=cookie).text
    soup1 = bs(html,'lxml')
    tables1 = soup1.find_all('fieldset',class_='fieldset')
    table_num = len(tables1)
    tables1 = str(tables1)
    tables_soup1 = bs(tables1, 'lxml')

    # 判断提交是否为空
    flag = 1
    if table_num == 5:
        flag = 2
    if not tables_soup1.find(text='作业内容附件'):
        print("\n 该学生[" + sd_name + "]提交作业为空！\n")

    else:

        print(tables_soup1.find_all('td')[1].text) # <td>课后习题1</td>
        # work_num = len(tables_soup1.select('tr')[flag]) - 1
        work_all = tables_soup1.select('tr')[flag].find_all('tr') # 所有行的作业、】
        work_num = len(work_all[1:])
        print("提交作业数量： " + str(work_num))

        url_size_dict = {}
        for work_one in work_all[1:]:
            # work_one = work_all[2] #单行作业
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
                with open(full_file_path, 'wb') as f:
                    f.write(r.content)
                f.close()
            print(sd_name + " 作业已下好")

        else: # 单个文件直接下载建立
            print(work_download_url_set)
            work_download_url = work_download_url_set[0][0]
            work_download_url = BanGongWang_Site_education + work_download_url
            # 加后缀
            extend_name = '.' + work_download_url_set[0][1].split('.')[1]
            # 文件名
            full_file_path = load_file_path + '\\' + sd_name + extend_name
            r = requests.get(work_download_url,headers=headers,cookies=cookie)
            with open(full_file_path,'wb') as f:
                f.write(r.content)
            f.close()
            print(sd_name + " 作业已下好")


# -------------- 进入办公网学生列表页面 --------------- #
def work_down(bangongwang_url):

    html = requests.get(bangongwang_url,headers=headers,cookies=cookie)
    if html.status_code == 200:
        print("已联通。。。")
    html = html.text
    soup = bs(html,'lxml')
    print(soup.title)
    title = str(soup.title)
    if '校园统一认证系统' in title:
        print('但是需要登陆')

    tables = soup.find('table',class_='tableborder100')
    tables = str(tables)
    tables_soup = bs(tables,'lxml')
    tr_all = tables_soup.select('tr') # 获取所有行
    tr_one = tr_all[1].find_all('td') # 获取单行

    print("提交人数： " + str(len(tr_all[1:])))
    for tr_one in tr_all[1:]: # 滤去第一行
        tr_one_td = tr_one.find_all('td')
        name = tr_one_td[0].text
        check_url = tr_one_td[4].a['href']
        check_url = BanGongWang_Site + check_url
        print('===============================')
        print("name: " + name)
        print("class: " + tr_one_td[1].text)
        print("smit_time: " + tr_one_td[2].text)
        print("check_state: " + tr_one_td[3].text.strip())
        print("check: " + tr_one_td[4].text.strip())
        print("check_url: " + check_url)
        print('-------------------------------')
        download_work(check_url, name)
        print('===============================')
        time.sleep(random.randint(2,10))

    print("over！")


# ----------------- run ---------------------- #
if __name__ == '__main__':
    start_time = time.time()
    url = ''
    work_down(url)
    end_time = time.time()
    cost_min = (end_time - start_time) / 60
    print('total time: ' + str(cost_min) + 'mins')
