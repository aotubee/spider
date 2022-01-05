#!/usr/bin/env python3
# coding=utf-8

import requests
from lxml import etree
from openpyxl import Workbook
from openpyxl.styles import Font
from openpyxl.styles import colors

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

        # 解析财务报表页
        cwbb_res = requests.get(cwbb_url, headers=headers)
        cwbb_html = etree.HTML(cwbb_res.text)
        cwbb_zj = cwbb_html.xpath('/html/body/div[4]/div[2]/div[2]/div[2]/div/div[2]/table//tr[31]/td[1]/text()')    #总计
        fzpers = cwbb_html.xpath('/html/body/div[4]/div[2]/div[2]/div[2]/div/div[2]/table//tr[11]/td[1]/text()')    # 资产负债率
        fzper = ''.join(fzpers).strip()
        stocks = []
        stocks.append('资产负债率:')
        stocks.append(fzper)

        if int(code) > 600000:
            print(name + price + info[38:40] + info[46:48] + info[28:30] + info[20:22] + info[30:32] + stocks)
        elif 600000 > int(code) > 300000: 
            print(name + price + info[22:24] + info[30:32] + info[40:42] + info[32:34] + info[42:44] + stocks)
        else:
            print(name + price + info[38:40] + info[46:48] + info[28:30] + info[20:22] + info[30:32] + stocks)
        
if __name__=="__main__":
    code = input("请输入股票代码：")
    spider = Spider()
    spider.loadPage(code)
