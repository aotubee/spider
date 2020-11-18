#!/usr/bin/env python3
# coding=utf-8

import requests, sys
from bs4 import BeautifulSoup

'''
小说下载

Create:2020-11-18
'''

class downloader(object):

    def __init__(self):
        self.server = 'https://www.biqukan.com'   #小说网站主页
        self.target = 'https://www.biqukan.com/1_1094/'    #一念天堂主页
        self.names = []    #章节名
        self.urls = []    #章节链接
        self.nums=0    #章节数

#获取下载链接:
    def get_download_url(self):
        req = requests.get(url = self.target)
        html = req.text.encode('iso-8859-1').decode('gbk')   #encode('iso-8859-1').decode('gbk')指定字符集为gbk
        div_bf = BeautifulSoup(html)
        div = div_bf.find_all('div',class_ = 'listmain')
        a_bf = BeautifulSoup(str(div[0]))
        a = a_bf.find_all('a')
        self.nums = len(a[15:])
        for i in a[15:]:
            self.names.append(i.string)
            self.urls.append(self.server + i.get('href'))

#下载小说内容：
    def get_contents(self, target):
        req = requests.get(url=target)
        html = req.text
        bf = BeautifulSoup(html)
        texts = bf.find_all('div', class_= 'showtxt')
        texts = texts[0].text.replace('\xa0'*8, '\n\n')
        return texts

#写入本地文件：
    def writer(self, name, path, text):
        writer_flag = True
        with open(path,'a',encoding='utf-8') as f:
            f.write(name + '\n')
            f.writelines(text)
            f.write('\n\n')

if __name__=='__main__':
    dl = downloader()
    dl.get_download_url()
    print('《一念永恒》开始下载：')
    for i in range(dl.nums):
        dl.writer(dl.names[i],'ynyh.txt',dl.get_contents(dl.urls[i]))
        sys.stdout.write("已下载：%.3f%%" % float(i/dl.nums) + '\r')
        sys.stdout.flush()
    print ('《一念永恒》下载完成')
