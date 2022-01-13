#!/usr/bin/env python3
# coding=utf-8

import time
import requests
import pymysql
from lxml import etree

class Spider(object):

    def loadPage(self, code):
        """下载页面"""
        # 获取首页
        if int(code) < 600000:
            url = 'https://xueqiu.com/S/SZ' + code
        else:
            url = 'https://xueqiu.com/S/SH' + code

        # 财务报表页面
        cwbb_url = 'https://q.stock.sohu.com/cn/%s/cwzb.shtml' % str(code)
        headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (sKHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"}

        # 解析主页信息
        res = requests.get(url, headers=headers)
        html = etree.HTML(res.text)
        name = html.xpath('//*[@id="app"]/div[2]/div[2]/div[1]//text()')    # 用于获取股票基本信息
        price = html.xpath('//*[@id="app"]/div[2]/div[2]/div/div/div/div/strong/text()')    # 用于获取股票基本信息
        info = html.xpath('//*[@id="app"]/div[2]/div[2]/div/table//text()')    # 用于获取股票基本信息
        stime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())    # 日期

        # 解析财务报表页
        cwbb_res = requests.get(cwbb_url, headers=headers)
        cwbb_html = etree.HTML(cwbb_res.text)
        cwbb_zj = cwbb_html.xpath('/html/body/div[4]/div[2]/div[2]/div[2]/div/div[2]/table//tr[31]/td[1]/text()')    #总计
        gr = cwbb_html.xpath('/html/body/div[4]/div[2]/div[2]/div[2]/div/div[2]/table//tr[25]/td[2]/span/text()')    # 净利润增长率
        fzpers = cwbb_html.xpath('/html/body/div[4]/div[2]/div[2]/div[2]/div/div[2]/table//tr[11]/td[1]/text()')    # 资产负债率
        fzper = ''.join(fzpers).strip()
        stocks = []
        stocks.append("%.2f%%" % float(fzper))    # 加上%
        stocks.append(stime)    

        if 600000 > int(code) > 300000: 
            stock = name + price + info[23:24] + info[31:32] + info[41:42] + info[33:34] + info[43:44] + gr + stocks
        else:
            stock = name + price + info[39:40] + info[47:48] + info[29:30] + info[21:22] + info[31:32] + gr + stocks

        self.sqlWrite(stock)

    def sqlWrite(self, stock):

        # 打开数据库连接
        db = pymysql.connect(host='localhost',
                             user='spider',
                             password='sql1234',
                             database='spider')

        # 使用cursor()方法获取操作游标 
        cursor = db.cursor()

        # SQL 插入语句
        sql = "INSERT INTO stock(NAME, PRICE, MARKET, FLOW, EARND, EARNS, SJL, GROW, PER, TIME) \
            VALUES ('%s', '%s', '%s', '%s', %s, %s, %s, '%s', '%s', '%s')" % \
            (str(stock[0]), str(stock[1]), str(stock[2]), str(stock[3]), str(stock[4]), str(stock[5]), str(stock[6]), str(stock[7]), str(stock[8]), str(stock[9]))

        try:
           # 执行sql语句
           cursor.execute(sql)
           # 提交到数据库执行
           db.commit()
        except:
           # 如果发生错误则回滚
           db.rollback()

        # 关闭数据库连接
        db.close()

if __name__=="__main__":
    codes = []
    print("输入股票代码,最后输入'yes'完成：")
    while True:
        code= input("输入股票代码或yes:")
        if len(code)==6:
            codes.append(code)
        elif code == 'yes':
            break
        else:
            print("输入有误.")
    for code in codes:
        spider = Spider()
        spider.loadPage(code)
