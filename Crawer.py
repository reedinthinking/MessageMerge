# coding=utf-8

import traceback
import urllib2, re, urllib
from bs4 import BeautifulSoup
import json, time
import csv
import sys
import codecs
import datetime
import pymysql
import re

reload(sys)
sys.setdefaultencoding("utf-8")


class Crawer:
    def __init__(self, baseurl):
        self.baseurl = baseurl
        self.url = self.baseurl + '/cgxq/'

    def connect(self, host, port, user, passwd, db, charset):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.db = db
        self.charset = charset
        try:
            self.condb = pymysql.connect(host=self.host, port=self.port, user=self.user,
                                         passwd=self.passwd, db=self.db, charset=self.charset)
        except Exception as abnormal:
            print("the database connect error:%s " % abnormal)
        # 创建一个游标对象
        self.cursor = self.condb.cursor()
        #self.sql = "insert into qjwqzhb('name','url','pub_time','con_finish_time','click_num','dock_enter_num','func_use','main_indice','tp') values (%s, %s,%s, %s, %s,%s, %s, %s,%s);"
        self.sql = "insert into qjwqzhb2(name,url,pub_time,con_finish_time,click_num,dock_enter_num,func_use,main_indice,tp) values (%s, %s,%s, %s, %s,%s, %s, %s,%s);"

    def get_ip_list(self, obj):
        ip_text = obj.findAll('tr', {'class': 'odd'})
        ip_list = []
        for i in range(len(ip_text)):
            ip_tag = ip_text[i].findAll('td')
            ip_port = ip_tag[1].get_text() + ':' + ip_tag[2].get_text()
            ip_list.append(ip_port)
        # print("共收集到了{}个代理IP".format(len(ip_list)))
        # print(ip_list)
        return ip_list


    def get_random_ip(self, ip_list):
        # ip_list = spider.get_ip_list(bsObj)
        import random
        random_ip = 'http://' + random.choice(ip_list)
        proxy_ip = {'http:': random_ip}
        return proxy_ip

    # get the html page
    def getHtml(self, url):
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
        headers = {'User-Agent': user_agent, 'Referer': url}
        try:
            random_ip = spider.get_random_ip(ip_list)
            #print 'random_ip:',random_ip
            httpproxy_handler = urllib2.ProxyHandler(random_ip)
            opener = urllib2.build_opener(httpproxy_handler)
            request = urllib2.Request(url, headers=headers)
            reponse = opener.open(request)
            html = reponse.read()
            return html
        except urllib2.URLError, e:
            print traceback.print_exc()
            if hasattr(e, "code"):
                print e.code
            if hasattr(e, "reason"):
                print e.reason

    # get the detail data
    def getItemList(self, url,writer,tp):
        #datenow = datetime.datetime.now()#获取当前系统时间
        #datenow = datetime.datetime.strftime(datenow, "%Y-%m-%d")#将datetime格式的时间转换成str
        #datenow = datetime.datetime.strptime(datenow, "%Y-%m-%d")#将str格式的时间转换成datetime格式
        # 今后的n天的日期
        #n_days = 4
        #now = datetime.datetime.now()#2018-12-31 16:17:05.627000
        #my_date = datetime.timedelta(days=n_days)# 4 days, 0:00:00
        #n_day = now + my_date#2019-01-04 16:17:05.627000
        urllist = ''
        itemdate = ''

        datenow = datetime.datetime.now()  # 获取当前系统时间
        n_days = 365

        my_date = datetime.timedelta(days=n_days)
        n_date = datenow - my_date
        t_date = n_date - my_date
        for i in range(100):
            if i==0:
                urllist = url
            else:
                suffix = '/index_' + str(i+1) + '.html'
                urllist = url + suffix
            print 'start srawer the url:',urllist
            html = spider.getHtml(urllist)
            if html == None:
                html = spider.getHtml(url)
            try:
                soup = BeautifulSoup(html, "html.parser")
                # -----------------get the attributes : borrowing_rates and debt_term-----------------
                items = soup.find(attrs={'class': 'text_list clearself retext_list'}).find_all('li')
                for item in items:
                    itemurl = spider.baseurl + item.a['href']
                    itemdate = item.i.string.strip()
                    itemdate_date = datetime.datetime.strptime(itemdate,"%Y-%m-%d")
                    if itemdate_date >= n_date:
                        print itemurl,'---date:---',itemdate
                        temp = spider.getDataList(itemurl,tp)
                        print temp
                        writer.writerow(temp)
                    else:
                        print itemurl

            except Exception, e:
                print traceback.print_exc()
                print e.message
                if hasattr(e, "code"):
                    print e.code
                if hasattr(e, "reason"):
                    print e.reason



        id = 2


    #get the detail data
    def getDataList(self, url,type):
        error = 0
        html = spider.getHtml(url)
        if html == None:
            html = spider.getHtml(url)
        name = ''
        pub_time = ''
        con_finish_time = ''
        click_num = ''
        dock_enter_num = ''
        func_use = ''
        main_indice = ''


        try:
            soup = BeautifulSoup(html, "html.parser")
            # -----------------get the attributes : borrowing_rates and debt_term-----------------
            items = soup.find('div', attrs={'class': 'view'})
            name = items.h1.string.strip()

            items2 = items.find('div', attrs={'id': 'fl'}).find_all('span')
            pub_time = items2[0].string
            print pub_time
            if pub_time.index('：'):
                pub_time = pub_time.split('：')[1].strip()
            con_finish_time = items2[1].string
            if con_finish_time.index('：'):
                con_finish_time = con_finish_time.split('：')[1].strip()
            link = items2[2].script.string.split('"')[1]
            linkstr = spider.getHtml(link)
            s = linkstr.index('=')
            n = linkstr.index(';')
            #print linkstr[s+1: n].strip()
            #click_num = linkstr[s+1:n].strip()
            if s != 0 and n!=0 :
                click_num = linkstr[s+1:n].strip()
            else:
                click_num = items2[3].string.strip()
            dock_enter_num = items2[4].span.string.strip()

            # for it in items2:
            #     print 'span:', it

            #for item in items3[1].stripped_strings:
            #    sex += item
            items3 = items.find('div',attrs={'class': 'view_box'}).find('div',attrs={'class': 'box'})
            print 'items3:-------------',items3
            for item in items3.stripped_strings:
                func_use += item

            print '---', pub_time, '---', con_finish_time, '---', click_num, '---', dock_enter_num, '---',func_use
           #marital_status = marital_status[5:]

        except Exception, e:
            print traceback.print_exc()
            if hasattr(e, "code"):
                print e.code
            if hasattr(e, "reason"):
                print e.reason
        self.cursor.execute(self.sql,[name,url,pub_time,con_finish_time,click_num,dock_enter_num,func_use,main_indice,type])  # 执行SQL
        self.condb.commit()  # 提交到数据库执行
        return [name,url,pub_time,con_finish_time,click_num,dock_enter_num,func_use,main_indice,type]


if __name__ == '__main__':
    #--------------------word write------------------------
    csvfile = open('demo1.csv', 'wb+')
    csvfile.write(codecs.BOM_UTF8)
    writer = csv.writer(csvfile)
    ll = ['name', 'pub_time', 'con_finish_time', 'click_num', 'dock_enter_num', 'func_use', 'main_indice', 'type']
    print "ll:-----------++++++++++", ll
    writer.writerow(ll)
    # --------------------------------------------

    baseXyb = 'http://www.weain.mil.cn'
    spider = Crawer(baseXyb)
    # ---------------------
    #get the vpn ip list
    urldaili = 'http://www.xicidaili.com/'
    headers = {
        'User-Agent': 'User-Agent:Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36'}
    request = urllib2.Request(urldaili, headers=headers)
    response = urllib2.urlopen(request)
    bsObj = BeautifulSoup(response, 'lxml')
    ip_list = spider.get_ip_list(bsObj)
    # --------------------

    spider.connect(host='127.0.0.1', port=3306, user='root',passwd='', db='MessageMerge', charset='utf8')
    urltmp = spider.url
    spider.getItemList(urltmp, writer, 'all')
    # type = ['yy','ky','gz','wx']
    # #spider.getDataList('http://www.weain.mil.cn/cgxq/ky/cpsbl/597278.html','yy')#neirongduohang
    # #spider.getDataList('http://www.weain.mil.cn/cgxq/yy/yjjsl/601900.html', 'yy')#neirongdanhang
    # for tp in type:#   range(112970, 115581)
    #     urltmp = spider.url + tp+'/'
    #     spider.getItemList(urltmp,writer,tp)
        #temp = spider.getDataList(urltmp)
        #print urltmp
        #writer.writerow(temp)

    csvfile.close()
    spider.cursor.close()
    spider.conn.close()





