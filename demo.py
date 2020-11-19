#!/usr/bin/env python3
# coding=utf-8

import requests

if __name__=='__main__':

    target='http://doubai.com'
    req = requests.get(url=target)
    print (req.text)

