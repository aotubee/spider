#!/usr/bin/env python3
# coding=utf-8

import requests
from bs4 import BeautifulSoup

def main():
    server= 'https://www.biqukan.com'
    target = 'https://www.biqukan.com/1_1094/'
    req = requests.get(url = target)
    html = req.text
    div_bf = BeautifulSoup(html)
    div = div_bf.find_all('div',class_ = 'listmain')
    a_bf = BeautifulSoup(str(div[0]))
    a = a_bf.find_all('a')
    for each in a:
        print(each.string,server + each.get('href'))

if __name__=='__main__':
    main()
