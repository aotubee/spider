#!/usr/bin/env python3
# coding=utf-8

import requests
from bs4 import BeautifulSoup

def main():
    target='https://www.biqukan.com/1_1094/5403177.html'
    req = requests.get(url=target)
    html=req.text
    bf=BeautifulSoup(html)
    texts=bf.find_all('div',class_='showtxt')
    print(texts[0].text.replace('\xa0'*8,'\n\n'))

if __name__=='__main__':
    main()
