#!/usr/bin/python
# -*- coding:utf-8 -*-
# author:joel
# time:2018/8/8 17:36

import datetime
import random
import time
import requests
import re
import pymysql

# pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pymysql 清华源

# https://tech.sina.com.cn/apple/if/2018-08-10/doc-ihhnunsq9039061.shtml

headers = {
    'User-Agent':''
}

def getHtml(page):
    """
    获取60条的新闻列表,包含新闻类别、标题、url、发布时间等
    :return: data_list
    """
    r = requests.get('http://roll.news.sina.com.cn/interface/rollnews_ch_out_interface.php?col=89&spec=&type=&ch=01&k=&offset_page=0&offset_num=0&num=60&asc=&page={}&r=0.9447795955534601'.format(page),headers=headers)
    r.encoding = 'gb2312'
    pattern1 = re.compile('\n|\t|\r')
    text = re.sub(pattern1, "", r.text)
    pattern2 = re.compile('{channel.*?{title\s:\s"(.*?)",id.*?,cTyp.*?,url.*?},title\s:\s"(.*?)",url\s:\s"(.*?)",type.*?,pic.*?,time\s:\s(\d+)}', re.S)
    data_list = re.findall(pattern2, text)
    return data_list

def getNews(m):
    """
    通过url获取新闻的内容正文，与之前的类别、标题、url、发布时间一起存入一个列表中
    :return:none
    """
    # 爬取5页
    for k in range(1,6):
        print(u'开始爬取第'+str(k)+u'页...')
        data_list = getHtml(k)
        n = 0
        for i in data_list:
            # 对包含四个参数的每个元组
            news = []
            for j in i:
                news.append(j)
            try:
                r = requests.get(i[2],headers=headers,timeout=3)
                r.encoding = 'utf-8'
            except:
                print(u'网络错误无法访问...')
                continue
            # 分析多篇新闻总结得网页源码中一般都含有<label>关键字，但也存着没有关键字的，这种网页源码中却也一般都包含<!--关键词begin-->的注释
            try:
                pattern3 = re.compile('.*?<!-- 引文 end -->.*?<!-- 正文.*? -->(.*?)我要反馈|<!--.*?关键词.*?begin -->.*?', re.S)
                content = re.findall(pattern3, r.text)
                # 匹配花括号{[^}]+}
                pattern4 = re.compile('\n|\s|\t|\r|<.*?>|<!--.*?-->|\(.*?\)|{[^}]+}|\)|\;|-->|&nbsp|打印网页', re.S)
                new_content = re.sub(pattern4, "", content[0])
            except:
                print(u'页面没有内容...')
                continue
            news.append(new_content)
            # 这里一个news列表中已经有类别、标题、url、发布时间、内容正文
            n += 1
            print(u'已获取第' + str(n) + u'条新闻...')
            print(news)
            stop_tag = insert_mysql(news[0], news[1], news[2], news[3], news[4])
            if stop_tag == 1 and m > 1:
                print(u'上次更新的位置...')
                return
            else:
                pass

def insert_mysql(type, title, url, time, content):
    stop_tag = 0
    dbname = 'sina'
    database = pymysql.connect(host='localhost', port=3306, user='user', passwd='passwd', db=dbname)
    cursor = database.cursor()
    try:
        select_sql = "select url from sinaroll2 where url= '%s'" % (url)
        response = cursor.execute(select_sql)
        if response == 1:
            print(u'该条新闻已存在...')
            stop_tag = 1
        else:
            try:
                insert_sql = "INSERT INTO SINAROLL2(`type`,title,url,`time`,content)VALUES ('%s','%s','%s','%s','%s')"%(type,title,url,time,content)
                cursor.execute(insert_sql)
                database.commit()
                print(u'提交成功')
            except:
                print(u'插入未成功！')
                database.rollback()
    except:
        print(u'查询错误！')
        database.rollback()
    finally:
        cursor.close()
        database.close()
        return stop_tag

if __name__ == '__main__':
    tag = 0
    m = 0
    # 获取当前时间
    now = datetime.datetime.now()
    #格式化开始时间
    start_time = datetime.datetime(now.year, now.month, now.day, now.hour, now.minute, now.second)
    print(start_time)
    while True:
        time.sleep(10)
        now = datetime.datetime.now()
        if tag == 0 and start_time < now:
            m += 1
            print(u'第'+str(m)+'次')
            time.sleep(3)
            print(now)
            getNews(m)
            tag = 1
        elif tag == 1:
            start_time = start_time + datetime.timedelta(minutes=40)
            # 下次开始执行的时间
            print(start_time)
            tag = 0
        else:
            pass
