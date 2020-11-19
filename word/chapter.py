#!/usr/bin/env python3
# coding=utf-8

import requests
from bs4 import BeautifulSoup

def main():
    weburl= 'https://www.biqukan.com'
    target = 'https://www.biqukan.com/1_1094/'
    req = requests.get(url = target)

    #encode('iso-8859-1').decode('gbk')指定字符集为gbk
    html = req.text.encode('iso-8859-1').decode('gbk')

    div_bf = BeautifulSoup(html)
    div = div_bf.find_all('div',class_ = 'listmain')
    a_bf = BeautifulSoup(str(div[0]))
    a = a_bf.find_all('a')
    for i in a:
        print(i.string,weburl + i.get('href'))

if __name__=='__main__':
    main()
