# -*- coding:utf-8 -*-  
"""
--------------------------------
    @Author: Dyson
    @Contact: Weaver1990@163.com
    @file: crawler全国青少年科技竞赛获奖名单公示.py
    @time: 2017/10/13 8:55
--------------------------------
"""
import sys
import os
import bs4
import json
import requests

sys.path.append(sys.prefix + "\\Lib\\MyWheels")
reload(sys)
sys.setdefaultencoding('utf8')
import html_table_reader
import PhantomJS_driver
import requests_manager
requests_manager = requests_manager.requests_manager()

PhantomJS_driver = PhantomJS_driver.PhantomJS_driver()
html_table_reader = html_table_reader.html_table_reader()

import set_log  # log_obj.debug(文本)  "\x1B[1;32;41m (文本)\x1B[0m"

log_obj = set_log.Logger(u'crawler全国青少年科技竞赛获奖名单公示.log', set_log.logging.WARNING,
                         set_log.logging.DEBUG)
log_obj.cleanup(u'crawler全国青少年科技竞赛获奖名单公示.log', if_cleanup=True)  # 是否需要在每次运行程序前清空Log文件


class crawler0(object):
    def __init__(self):
        pass

    def get_list(self):

        resp = requests.get('http://gs.cyscc.org.cn/')
        bs_obj = bs4.BeautifulSoup(resp.text, 'html.parser')
        e_table = bs_obj.find('table', class_='styledTable')

        e_trs = e_table.find_all('tr')[1:]
        d = {}
        for e_tr in e_trs:
            e_as = e_tr.find_all('a')
            #func = lambda e:True if e.tag == 'td' and not e.has_attr('rowspan') else False
            title = e_tr.find('td', align='left').get_text(strip=True)

            d0 = {title + e.get_text(strip=True):'http://gs.cyscc.org.cn/' + e.get('href') for e in e_as}
            d.update(d0)
        #with open('test.json','wb') as f:
        #    json.dump(d, f, ensure_ascii=False)
        return d

    def get_detail(self):
        urls = self.get_list()

        for title in urls:
            try:
                print "Crawling =>",title , urls[title]
                targetfile = os.path.join('C:\\Users\\Administrator\\Desktop\\Projects\\Uniqueness\\files\\' + title + '.csv')
                if os.path.exists(targetfile):
                    print 'pass'
                    continue
                #driver = PhantomJS_driver.initialization()
                #driver.get(urls[title])
                #bs_obj = bs4.BeautifulSoup(driver.page_source, 'html.parser')
                #driver.quit()
                bs_obj = bs4.BeautifulSoup(requests_manager.get_html(urls[title]), 'html.parser')
                if bs_obj.find('ul',class_='areaList'):
                    bs_obj = self.area_parser(bs_obj)

                self.list_parser(bs_obj, title, targetfile)
            except:
                log_obj.error(title , urls[title])

    def area_parser(self, bs_obj):
        e_li = bs_obj.find('ul',class_='areaList').li
        resp = requests.get('http://gs.cyscc.org.cn/' + e_li.a.get('href'))
        return bs4.BeautifulSoup(resp.text, 'html.parser')

    def list_parser(self, bs_obj, title, targetfile):
        e_table = bs_obj.find('table', class_='styledTable')
        df = html_table_reader.table_tr_td(e_table)
        df.to_csv(targetfile,encoding='utf_8_sig')

if __name__ == '__main__':
    crawler0 = crawler0()
    crawler0.get_detail()