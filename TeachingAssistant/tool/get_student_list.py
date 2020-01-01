import requests
from bs4 import BeautifulSoup as bs
import time
import random
from tool.download_work import download_work
from conf.bangongwang_url import BanGongWang_Site
from conf.filepath import load_file_path
from conf.create_file import downtext_file
from conf.logmodule import LogModule


# -------------- 进入办公网学生列表页面 --------------- #
logger = LogModule()

def work_down(bangongwang_url,headers,cookie):

    html = requests.get(bangongwang_url,headers=headers,cookies=cookie)
    if html.status_code == 200:
        logger.info('已联通。。。')
        # print("已联通。。。")
    html = html.text
    soup = bs(html,'lxml')
    print(soup.title)
    title = str(soup.title)
    if '校园统一认证系统' in title:
        logger.info('但是需要登陆(换cookie吧)')
        # print('但是需要登陆(换cookie吧)')

    tables = soup.find('table',class_='tableborder100')
    tables = str(tables)
    tables_soup = bs(tables,'lxml')
    tr_all = tables_soup.select('tr') # 获取所有行
    # tr_one = tr_all[1].find_all('td') # 获取单行

    admit_list = []
    admitNone_list = []

    for tr_one in tr_all[1:]: # 滤去第一行, every_student
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
        # 调用下载函数，返回是否交有作业
        if download_work(check_url,name,headers,cookie):
            admit_list.append(name)
        else:
            admitNone_list.append(name)
        print('===============================')
        time.sleep(random.randint(2,10))

    print(admitNone_list)
    content = '交作业为空的同学：' + '\n' + str(admitNone_list)
    logger.info('交作业为空的同学：' + '\n' + str(admitNone_list))
    statistics_path = load_file_path + '\\' + 'statistics.txt'

    downtext_file(statistics_path, content)

    print("over！")