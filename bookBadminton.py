# 羽毛球馆关门了.v1.4   py3.7
# coding:utf-8
import requests
from bs4 import BeautifulSoup
import datetime
import schedule
import time
import yagmail
import types
import threading


class BBKing:
    def __init__(self, u_name, u_pwd, u_playtime0, u_playtime1, u_cd, u_cd1, up_days=2, receiver_email='biubiubiu@yunmail.com'):
        self.receiver = receiver_email
        self.username = u_name
        self.user_pwd = u_pwd
        self.playtime0 = u_playtime0
        self.playtime1 = u_playtime1
        self.up_days = up_days
        self.cd = u_cd
        self.cd1 = u_cd1
        self.login_url = 'http://biubiubiu.xxx.edu.cn:8080/index.php/Book/Login/authCheck.html'
        self.post_url = 'http://biubiubiu.xxx.edu.cn:8080/index.php/Book/Book/order.html'
        self.book_index3_url = 'http://biubiubiu.xxx.edu.cn:8080/index.php/Book/Book/index3.html?day='
        self.order_index4_url = 'http://biubiu.xxx.edu.cn:8080/index.php/Book/Book/index4?'

    def login(self):
        try:
            # 随机分配header
            header = {'User-Agent': 'Mozilla/5.0'}
            data = {'name': self.username, 'pwd': self.user_pwd}
            book_session = requests.Session()
            book_post = book_session.post(self.login_url, headers=header, data=data)
            if book_post.text == 'SUCCESS':
                print(self.username + 'Login Done')
            elif book_post.text == 'ERROR':
                print(self.username + 'Login Error')
            cookies = book_post.cookies.get_dict()
            return book_session, cookies
        except:
            print('登录异常')

    def assemble_cds_url(self):
        # 提前两天预定
        day_now = datetime.datetime.now()
        delta = datetime.timedelta(days=self.up_days)
        day_goal = day_now + delta
        day_goal = day_goal.strftime("%Y-%m-%d")
        # 哪个时间段预定
        # 如果选择两个时间段 ，没选默认-1，默认playtime1=-1
        is_double = True if int(self.playtime0) and int(self.playtime1) > 0 else False
        if not is_double:
            play_times0 = self.playtime0  # 00002代表9~10点 转换？
            playtime0 = int(self.playtime0) + 7
            cds_url = self.book_index3_url + day_goal + '&time=' + play_times0 + '&cg=01&cp=02'
            latter_cut = 'day=' + day_goal + '&time=' + play_times0 + '&cg=01&cp=02'
            s0 = f'预定日期: {day_goal} 预定时间: {str(playtime0)}~{str(playtime0 + 1)}'
            return [is_double, cds_url, latter_cut, s0]
        else:

            play_times0 = self.playtime0  # 00002代表9~10点 转换？
            playtime0 = int(self.playtime0) + 7
            cds_url0 = self.book_index3_url + day_goal + '&time=' + play_times0 + '&cg=01&cp=02'
            latter_cut0 = 'day=' + day_goal + '&time=' + play_times0 + '&cg=01&cp=02'
            s0 = f'预定日期: {day_goal} 预定时间: {str(playtime0)}~{str(playtime0 + 1)}'

            play_times1 = self.playtime1  # 00002代表9~10点 转换？
            playtime1 = int(self.playtime1) + 7
            cds_url1 = self.book_index3_url + day_goal + '&time=' + play_times1 + '&cg=01&cp=02'
            latter_cut1 = 'day=' + day_goal + '&time=' + play_times1 + '&cg=01&cp=02'
            s1 = f'预定日期: {day_goal} 预定时间: {str(playtime1)}~{str(playtime1 + 1)}'
            return [is_double, cds_url0, latter_cut0, s0, cds_url1, latter_cut1, s1]

    def refresh(self, refresh_session, cds_url, cookies):
        cnt = 0
        # 巡回刷新
        while 1:

            r = refresh_session.get(cds_url, cookies=cookies)
            probe_soup = BeautifulSoup(r.content, "html.parser")
            probe_title = probe_soup.select('body > div.navigate.box.bottom_border > div > h2')
            ponce = BeautifulSoup(str(probe_title), "html.parser")
            msg = ponce.text[1:-1]  # 场馆预定->预定场地
            # 刷新，还未开放或者已被预订,持续10分钟最多
            if msg == 'ERROR':
                if cnt % 60 == 0:
                    if self.receiver != 'biubiubiu@yunmail.com':
                        print('羽毛球场还没开门')
                        sent_mail('羽毛球场还没开门', 'BBKing Info', self.receiver)
                time.sleep(3)
                cnt += 3
                if cnt == 600:
                    break
                continue

            elif msg == '场馆预定->预定场地':

                if self.receiver != 'biubiubiu@yunmail.com':
                    sent_mail('羽毛球场开门了，开始预定', 'BBKing Info', self.receiver)
                print('羽毛球场开门了，开始预定', 'BBKing Info')

                break
        return refresh_session

    def order(self, book_session, cds_url, cookies, latter_cut, s1, cd):
        # 默认 cd1=-1
        if cd == -1:
            return
        r = book_session.get(cds_url, cookies=cookies)
        try:
            book_soup = BeautifulSoup(r.content, "html.parser")
            orientation = book_soup.find(id='spaceList')  # 当前可预定场地如下
            orientation1 = BeautifulSoup(str(orientation), "html.parser")
            cdinfo_divs_plus = orientation1.find_all('div')
            cdinfo_divs = cdinfo_divs_plus[1:]

            cd_list = [x['name'] for x in cdinfo_divs]
            u_cd_info = '22' + str(cd) if cd > 9 else '220' + str(cd)
            # 目标场地存在
            cdinfoid = cdinfo_divs[0]['name'] if u_cd_info not in cd_list else u_cd_info
            s21 = f' 目标场地：{u_cd_info[2:]}号 '
            s22 = f' 预定场地：{cdinfoid[2:]}号 '

            # 目标场地链接
            order_urls_1 = self.order_index4_url + latter_cut + '&cdinfoid=' + cdinfoid
            order_html = book_session.get(order_urls_1)
            try:
                order_soup = BeautifulSoup(order_html.content, "html.parser")
                # 获取 formdata
                form_data_input = order_soup.find_all('input')[:-2]
                form_data_value = [x['value'] for x in form_data_input]
                form_data = {
                    '__hash__': form_data_value[0],
                    'CELL_PHONE': form_data_value[1],
                    # 'NAME': form_data_value[2], # 姓名，此项不用
                    'CGINFO_ID': form_data_value[3],
                    'CDINFO_ID': form_data_value[4],
                    'CAMPUS_ID': form_data_value[5],
                    'SEQ_NO': form_data_value[6],
                    'PRICE': form_data_value[7],
                    'DISCOUNT': form_data_value[8],
                    'PRICE_FINAL': form_data_value[9],
                }
            except Exception as e:
                print(e)
                print('预定次数已满')
                self.failure(order_html)
            else:
                # 预定场地
                post_html = book_session.post(self.post_url, data=form_data)
                # 预定成功，邮件发送
                sent_text = '学号：' + self.username + s1 + s21 + s22
                # 不用这个判断
                if post_html.text == 'SUCCESS':
                    if self.receiver != 'biubiubiu@yunmail.com':
                        print('BBKing Info 预定成功')
                        sent_mail(sent_text, 'BBKing Info 预定成功', self.receiver)
                    print('DONE!')
                    print(sent_text)

        except Exception as e:
            print(e)
            self.failure(r)

    def failure(self, r):
        print('预定失败')
        biu_soup = BeautifulSoup(r.content, "html.parser")
        bsoup = biu_soup.select('tr > td')
        bbsoup = BeautifulSoup(str(bsoup), "html.parser")
        msg = bbsoup.text[-25:-1]
        if self.receiver != 'biubiubiu@yunmail.com':
            print('羽毛球场关门了', 'BBKing Info 预定失败')
            sent_mail(msg + '羽毛球场关门了', 'BBKing Info 预定失败', self.receiver)

    def booking(self):
        book_session, cookies = self.login()
        cookies = book_session.cookies.get_dict()
        playtime_list = self.assemble_cds_url()
        cd, cd1 = self.cd, self.cd1
        # 选择两个时间段
        if not playtime_list[0]:
            # 选择两个场地
            cds_url, latter_cut, s1 = playtime_list[1], playtime_list[2], playtime_list[3]
            refresh_session = self.refresh(book_session, cds_url, cookies)
            # 预定开始
            try:
                # todo 改并行
                self.order(refresh_session, cds_url, cookies, latter_cut, s1, cd)
                self.order(refresh_session, cds_url, cookies, latter_cut, s1, cd1)
            except Exception as e:
                print(e)
            finally:
                book_session.close()
        else:
            cds_url0, latter_cut0, s0 = playtime_list[1], playtime_list[2], playtime_list[3]
            cds_url1, latter_cut1, s1 = playtime_list[4], playtime_list[5], playtime_list[6]
            refresh_session = self.refresh(book_session, cds_url0, cookies)
            # 预定开始
            try:
                self.order(refresh_session, cds_url0, cookies, latter_cut0, s0, cd)
                self.order(refresh_session, cds_url1, cookies, latter_cut1, s1, cd1)
            except Exception as e:
                print(e)
            finally:
                book_session.close()


# 添加邮箱账号密码
def sent_mail(content, subject, to_email, user_email='biubiubiu@yunmail.com', psw='biubiubiu'):
    try:
        yag = yagmail.SMTP(user=user_email, password=psw, host='smtp.yunmail.com')
        contents = [content]
        yag.send(to_email, subject, contents)
        yag.close()
        print('done sent email')
    except Exception as e:
        print(e)
        print('sent failure')


BBKing.sent_mail = types.MethodType(sent_mail, BBKing)


def run_threaded(job):
    job_thread = threading.Thread(target=job)
    job_thread.start()


if __name__ == '__main__':
    # todo 日志，插件。。。
    # 当前同一个号同一天定最多订两个场地，最多提前两天预定
    # 输入为 账号, 密码,预定场地日期1，预定场地日期2=-1, 场地号1, 场地号2=-1,提前几天预定=2,接收邮箱='xxxx'
    # 00009 00010 分别代表16-17，17-18时段
    # 1.单号
    args0 = [' ', ' ', '00009',  '00010', 1, 2]
    s0 = BBKing(*args0)
    schedule.every().saturday.at('12:00').do(s0.booking)
    # 2. 多号
    # # 开线程情况（不建议）
    # args1 = ['', '', '00010', -1, 1, -1, 2, 'biubiubiu@yunmail.com']
    # s1 = BBKing(*args1)
    # schedule.every().saturday.at('12:00').do(run_threaded, s0.booking)
    # schedule.every().saturday.at('12:00').do(run_threaded, s1.booking)
    while True:
        schedule.run_pending()
