#!/usr/bin/env python3
# coding=utf-8

from bs4 import BeautifulSoup
import requests,sys


class downloader(object):

    def __init__(self):
        #主页，单独章节中的全链接需要主页的拼凑
        self.index = "https://www.bqktxt.com"
        #目录页
        self.target = "https://www.bqktxt.com/1_1094/"
        self.names = []
        self.urls = []
        self.nums = 0

    #获取目录：
    def get_list(self):
        req = requests.get(url=self.target)
        #设置中文字符为gbk，与原网站一致
        req.encoding = 'gbk'
        html = req.text
        #解析网页
        div_bf = BeautifulSoup(html,'lxml')
        div = div_bf.find_all('div', 'listmain')
        div = BeautifulSoup(str(div[0]),'lxml')
        div = div.find_all('a')
        self.nums = len(div[13:])
        #剔除前13行非必要的链接
        for i in div[13:]:
            self.names.append(i.string)
            self.urls.append(self.index + i.get('href'))
#            print (i.string, self.index + i.get('href'))

    #获取文章内容,target为动态参数，实际target为self.urls的值.
    def get_content(self, target):
        req = requests.get(url=target)
        html = req.text
        bf = BeautifulSoup(html,'lxml')
        texts = bf.find_all('div', 'showtxt')
        texts = texts[0].text.replace('\xa0'*8,'\n\n')
        return texts

if __name__=='__main__':
    down = downloader()
    down.get_list()
    print ("《一念永恒》开始下载：")
    for j in range(down.nums):
        with open('/home/debian/download/ynyh.txt', 'a+') as f:
            #先写入目录名
            f.write(down.names[j] + '\n')
            #再写入内容
            f.write(down.get_content(down.urls[j]))
        sys.stdout.write("已下载：%.2f%%" % float(j/down.nums*100) + '\r')
        sys.stdout.flush()
    print ("下载完成.")
    
































    
