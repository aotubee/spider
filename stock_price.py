#!/usr/bin/env python3
# coding=utf-8

import requests
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

        # 解析财务报表页
        cwbb_res = requests.get(cwbb_url, headers=headers)
        cwbb_html = etree.HTML(cwbb_res.text)
        cwbb_zj = cwbb_html.xpath('/html/body/div[4]/div[2]/div[2]/div[2]/div/div[2]/table//tr[31]/td[1]/text()')    #总计
        growrate = cwbb_html.xpath('/html/body/div[4]/div[2]/div[2]/div[2]/div/div[2]/table//tr[25]/td[2]/span/text()')    # 净利润增长率
        fzpers = cwbb_html.xpath('/html/body/div[4]/div[2]/div[2]/div[2]/div/div[2]/table//tr[11]/td[1]/text()')    # 资产负债率
        fzhj = cwbb_html.xpath('/html/body/div[4]/div[2]/div[2]/div[2]/div/div[2]/table//tr[34]/td[1]/text()')    # 负债合计
        zczj = cwbb_html.xpath('/html/body/div[4]/div[2]/div[2]/div[2]/div/div[2]/table//tr[36]/td[1]/text()')    # 资产权益总计

        gr = ['净利润增长率:'] + growrate
        fzper = ''.join(fzpers).strip()
        stocks = []
        stocks.append('资产负债率:')
        stocks.append("%.2f%%" % float(fzper))    # 加上%

        fz = ''.join(fzhj).strip()
        zc = ''.join(zczj).strip()
        jzc = (int(zc)-int(fz))    # 净资产
        stocks.append('净资产:')
        stocks.append('%.2f亿' % float(jzc/10000))

        if 600000 > int(code) > 300000: 
            print(' '.join(name + price + info[22:24] + info[30:32] + info[40:42] + info[32:34] + info[42:44] + gr + stocks + info[56:58]))
        else:
            print(' '.join(name + price + info[38:40] + info[46:48] + info[28:30] + info[20:22] + info[30:32] + gr + stocks + info[44:46]))
        
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
