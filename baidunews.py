#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:joel
# time:2018/8/14 15:36

import re
from readability.readability import Document
import requests
import pymysql

class extract():
    def getNewsList(self, pn, keyword):
        """
        获取20条json类型的新闻信息（标题，url，来源，时间戳）
        :param pn:
        :param keyword:
        :return: all_info
        """
        try:
            # %3A%28{}%29之间为关键字，pn为页偏移量
            r = requests.get('http://news.baidu.com/ns?word=title%3A%28{}%29&pn={}&cl=2&ct=1&tn=json&rn=20&ie=utf-8&bt=0&et=0'.format(keyword, str(pn*20)))
        except:
            print(u'无法访问...')
        # pattern = re.compile('.*?<h3 class="c-title">.*?<a href="(.*?)".*?data-click=".*?".*?>(.*?)</a>.*?</h3>.*?<div class="c-title-author">(.*?)&nbsp;&nbsp;(.*?)<', re.S)
        # 获取json类型的news基本信息
        pattern = re.compile('{.*?"title": "(.*?)",.*?"url": "(.*?)",.*?"source": "(.*?)",.*?"time": (\d+).*?}', re.S)
        info_list = re.findall(pattern, r.text)
        # pattern2 = re.compile('<em>|</em>|[\n\t\r\s]|&nbsp;|<.*?>|&#8226;',re.S)
        all_info = []
        for info in info_list:
            info = list(info)
            info[1] = re.sub('\\\\', "", info[1])
            # 将\\uxxxx转换成中文
            info[0] = info[0].encode('utf-8').decode('unicode_escape')
            info[2] = info[2].encode('utf-8').decode('unicode_escape')
            all_info.append(info)
        return all_info

    def tool(self, text):
        """
        清洗readability抓取后的数据，清洗过程加入了 &#13; 和 \n
        :param text:
        :return: text
        """
        pattern1 = re.compile(r'<!--.*?-->|<script.*?>(.*?)<\/script>|<style.*?>(.*?)<\/style>|<.*?>|[ \t\r\f\v]|&#13;|\n', re.S)
        text = re.sub(pattern1, "", text)
        return text

    def getContent(self):
        """
        调用readability库的方法，readable_article是带参数的HTML文本
        Given a html document, it pulls out the main body text and cleans it up
        :return: none
        """
        keyword = input(u'请输入关键字：')
        for i in range(0, 10):
            all_info = self.getNewsList(i, keyword)
            for info in all_info:
                print(info[1])
                try:
                    r = requests.get(info[1])
                except:
                    print(u'无法访问...')
                    continue
                try:
                    charset = re.search('[meta|META].*?charset="*(.*?)".*?>', r.text).group(1)
                    r.encoding = charset
                except:
                    print(u'可能为视频...')
                try:
                    readable_article = Document(r.text).summary()
                except:
                    print(u'抱歉，readability无法获取...')
                # readable_title = Document(r.text).short_title()
                readable_article = self.tool(readable_article)
                print(readable_article)
                self.insert(info[0], info[1], info[2], info[3], readable_article)

    def insert(self, title, url, source, time, content):
        """
        mysql数据插入
        :param title: 新闻标题
        :param url: 新闻url
        :param source: 新闻来源
        :param time: 新闻发布时间
        :param content: 正文内容
        :return: none
        """
        database = pymysql.connect(host='localhost', port=3306, user='user', passwd='passwd', db='baidunews')
        cursor = database.cursor()
        try:
            select_sql = "select url from baidunews where url='%s'"%(url)
            response = cursor.execute(select_sql)
            if response == 1:
                print(u'该条新闻已存在...')
            else:
                try:
                    insert_sql = "insert into baidunews (title,url,source,`time`,content)values('%s','%s','%s','%s','%s')"%(title, url, source, time, content)
                    cursor.execute(insert_sql)
                    database.commit()
                    print(u'提交成功...')
                except:
                    print(u'插入错误...')
                    database.rollback()
        except:
            print(u'查询错误...')
            database.rollback()
        finally:
            cursor.close()
            database.close()

if __name__ == '__main__':
    extract = extract()
    extract.getContent()
