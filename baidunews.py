#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:joel
# time:2018/8/14 15:36

import re
from readability.readability import Document
import requests
import pymysql


class Extract(object):
    def __init__(self):
        self.headers = {
            'User-Agent': 'ua'
        }

    @staticmethod
    def getnewslist(pn, keyword):
        """
        获取20条json类型的新闻信息（标题，url，来源，时间戳）
        """
        # %3A%28{}%29之间为关键字，pn为页偏移量
        r = requests.get('http://news.baidu.com/ns?word=title%3A%28{}%29&pn={}&cl=2&ct=1&tn=json&rn=20'
                         '&ie=utf-8&bt=0&et=0'.format(keyword, str(pn*20)))
        # 获取json类型的news基本信息
        pattern = re.compile('{.*?"title": "(.*?)",.*?"url": "(.*?)",.*?"source": "(.*?)",.*?"time": (\d+).*?}', re.S)
        info_list = re.findall(pattern, r.text)
        # pattern2 = re.compile('<em>|</em>|[\n\t\r\s]|&nbsp;|<.*?>|&#8226;',re.S)
        all_info = []
        for info in info_list:
            info = list(info)
            info[1] = re.sub('\\\\', "", info[1])
            # 将\uxxxx转换成中文
            info[0] = info[0].encode('utf-8').decode('unicode_escape')
            info[2] = info[2].encode('utf-8').decode('unicode_escape')
            all_info.append(info)
        return all_info

    @staticmethod
    def tool(text):
        """
        清洗readability抓取后的数据，清洗过程加入了 &#13; 和 \n
        """
        pattern1 = re.compile(r'<!--.*?-->|<script.*?>(.*?)<\/script>|<style.*?>(.*?)<\/style>|<.*?>'
                              r'|[ \t\r\f\v]|&#13;|\n', re.S)
        text = re.sub(pattern1, "", text)
        return text

    def getcontent(self):
        """
        调用readability库的方法，readable_article是带参数的HTML文本
        Given a html document, it pulls out the main body text and cleans it up
        """
        global readable_article
        keyword = input(u'请输入关键字：')
        for i in range(0, 5):
            all_info = self.getnewslist(i, keyword)
            for info in all_info:
                print(info[1])
                try:
                    # 对于某些网站需要添加请求头，如news.10jqka.com.cn ， 开源中国等
                    r = requests.get(info[1], headers=self.headers)
                except Exception as e:
                    print(u'无法访问...', e)
                    continue
                try:
                    charset = re.search('[meta|META].*?charset="*(.*?)".*?>', r.text).group(1)
                    r.encoding = charset
                except Exception as e:
                    print(u'可能为视频...', e)
                try:
                    readable_article = Document(r.text).summary()
                except Exception as e:
                    print(u'抱歉，readability无法获取...', e)
                # readable_title = Document(r.text).short_title()
                readable_article = self.tool(readable_article)
                print(readable_article)
                self.insert(info[0], info[1], info[2], info[3], readable_article)

    def insert(self, title, url, source, time, content):
        """
        mysql数据插入
        """
        database = pymysql.connect(host='localhost', port=3306, user='', passwd='', db='gzh')
        cursor = database.cursor()
        try:
            select_sql = "select url from baidunews where url='%s'" % url
            response = cursor.execute(select_sql)
            if response == 1:
                print(u'该条新闻已存在...')
            else:
                try:
                    insert_sql = "insert into baidunews (title,url,source,`time`,content)values" \
                                 "('%s','%s','%s','%s','%s')"%(title, url, source, time, content)
                    cursor.execute(insert_sql)
                    database.commit()
                    print(u'提交成功...')
                except Exception as e:
                    print(u'插入错误...', e)
                    database.rollback()
        except Exception as e:
            print(u'查询错误...', e)
            database.rollback()
        finally:
            cursor.close()
            database.close()


if __name__ == '__main__':
    extract = Extract()
    extract.getcontent()


