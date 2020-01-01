import time
from tool_v2.get_student_list import work_down
from conf.bangongwang_url import sd_list_path_url
from conf.KeepSecret_cookies_headers import  headers,cookie
from conf.create_file import cookie_to_dict
from conf.logmodule import LogModule



if __name__ == '__main__':
    '''
    针对tool_v2
    若网站没改版
    下载作业请修改 更换页面链接： conf/bangongwang_url.py -> sd_list_path_url
                 更换cookie：conf/KeepSecret_cookies_headers.py -> cookie
                 更换下载地址：conf/filepath.py -> load_file_path
    '''
    # todo 需加上 实下人数 判断是否与提交人数相吻合（除提交空情况，可能网络问题导致下载出错）
    start_time = time.time()
    logger = LogModule()
    work_down(sd_list_path_url,headers,cookie_to_dict(cookie))
    end_time = time.time()
    cost_min = (end_time - start_time) / 60
    logger.info("下载结束，总用时为(min)： " + str(cost_min))
    # print('total time: ' + str(cost_min) + 'mins')

