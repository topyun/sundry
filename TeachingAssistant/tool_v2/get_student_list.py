import requests
from bs4 import BeautifulSoup as bs
import time
import random
from tool_v2.download_work import download_work
from conf.bangongwang_url import BanGongWang_Site
from conf.logmodule import LogModule
from concurrent.futures import ThreadPoolExecutor,wait,ALL_COMPLETED



# -------------- 进入办公网学生列表页面 --------------- #
logger = LogModule()

def work_down(bangongwang_url,headers,cookie):

    html = requests.get(bangongwang_url,headers=headers,cookies=cookie)
    if html.status_code == 200:
        logger.info('已联通。。。')
    html = html.text
    soup = bs(html,'lxml')
    # print(soup.title)
    title = str(soup.title)
    if '校园统一认证系统' in title:
        logger.info('但是需要登陆(换cookie吧)')
    else:
        tables = soup.find('table',class_='tableborder100')
        tables = str(tables)
        tables_soup = bs(tables,'lxml')
        tr_all = tables_soup.select('tr') # 获取所有行
        # tr_one = tr_all[1].find_all('td') # 获取单行
        check_url_list = []

        # print("提交人数： " + str(len(tr_all[1:])))
        logger.info("提交人数： " + str(len(tr_all[1:])))
        for tr_one in tr_all[1:]: # 滤去第一行, every_student
            tr_one_td = tr_one.find_all('td')
            name = tr_one_td[0].text
            check_url = tr_one_td[4].a['href']
            check_url = BanGongWang_Site + check_url
            check_urlAnd_name = (check_url,name)
            check_url_list.append(check_urlAnd_name)
            # 调用下载函数，返回是否交有作业
            # time.sleep(random.randint(2, 10))
        executor = ThreadPoolExecutor(max_workers=10)
        future_tasks = [executor.submit(download_work, check_urlAnd_name[0], check_urlAnd_name[1],headers,cookie) for check_urlAnd_name
                        in check_url_list]
        wait(future_tasks, return_when=ALL_COMPLETED)
        # print("over！")
        logger.info('下载完成')
