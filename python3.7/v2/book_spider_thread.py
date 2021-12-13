#!/usr/bin/env python3
# coding=utf-8

from bs4 import BeautifulSoup
import requests,sys
import threading
import queue
import time
 
class downLoader(threading.Thread):
 
    def __init__(self, target, q, n):
        super(downLoader, self).__init__()
        self.target = target
        self.q = q
        #主页，单独章节中的全链接需要主页的拼凑
        self.index = "https://www.bqktxt.com"
        #目录页   
        self.names = []
        self.urls = []
        self.nums = 0

    #获取目录：
    def get_list(self):
       req = requests.get(url = self.target)
       #设置中文字符为gbk，与原网站一致
       req.encoding = 'gbk'
       html = req.text
       #解析网页
       div_bf = BeautifulSoup(html,'lxml')
       div = div_bf.find_all('div', 'listmain')
       div = BeautifulSoup(str(div[0]),'lxml')
       html_list = div.find_all('a') 
       #剔除前13行非必要的链接
       for i in html_list[13:]:
           self.names.append(i.string)
           self.urls.append(self.index + i.get('href'))
 
    #获取文章内容,page为动态参数,在writer函数调用时传入值
    def get_content(self, page):
        req = requests.get(url = page)
        html = req.text
        bf = BeautifulSoup(html,'lxml')
        texts = bf.find_all('div', 'showtxt')
        texts = texts[0].text.replace('\xa0'*8,'\n\n')
        return texts

    def writer(self, n):
        self.get_list()
        with open('/home/debian/download/%s.txt' % (self.names[n]), 'a+') as f:
            f.write(self.names[n] + '\n')
            f.write(self.get_content(self.urls[n]))
        sys.stdout.write("已下载：%.2f%%" % float(n/nm*100) + '\r')
        sys.stdout.flush()
 
    def run(self):
        self.writer(n)


#通过爬取目录列表，获取要爬网页的数量
def get_list(target):
    req = requests.get(url=target)
    #设置中文字符为gbk，与原网站一致
    req.encoding = 'gbk'
    html = req.text
    #解析网页
    div_bf = BeautifulSoup(html,'lxml')
    div = div_bf.find_all('div', 'listmain')
    div = BeautifulSoup(str(div[0]),'lxml')
    div = div.find_all('a')
    nums = len(div[13:200])
    return nums

if __name__=='__main__':
    start = time.time()
    q = queue.Queue(10)
    target = "https://www.bqktxt.com/1_1094/"
    thread_list=[]

    #将要爬网页的数量赋值与nm
    nm = get_list(target)
    print ("《一念永恒》开始下载：")
    for n in range(nm):
        p = downLoader(target, q, n)
        p.start()
        thread_list.append(p)
        time.sleep(0.8)

    for syn in thread_list:
        syn.join()

    while not q.empty():
        pass
 
    print ("下载完成.")
    print ('[info]耗时：%s秒'%(time.time()-start))  
