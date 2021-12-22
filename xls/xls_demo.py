#!/usr/bin/env python3
# coding=utf-8

import xlsxwriter

host_ip = (
    ["server1",'192.168.1.101','2018-06-11'],
    ["server2",'192.168.1.102','2018-06-11'],
    ["server3",'192.168.1.103','2018-06-11'],
    ["server4",'192.168.1.104','2018-06-11']
)

# 创建一个新的文件
with xlsxwriter.Workbook('ip.xlsx') as  workbook:

    # 添加一个工作表
    worksheet = workbook.add_worksheet('ip地址统计')

    # 设置一个加粗的格式
    bold = workbook.add_format({"bold": True})

    # 设置一个日期的格式
    date_format = workbook.add_format(
        {'num_format': 'yyyy-mm-dd'})

    # 分别设置一下 A 和 B 列的宽度
    worksheet.set_column('A:A', 10)
    worksheet.set_column('B:B', 15)
    worksheet.set_column('C:C', 18)

    # 先把表格的抬头写上，并设置字体加粗
    worksheet.write('A1', '主机名',  bold)
    worksheet.write('B1', 'IP 地址', bold)
    worksheet.write(0,2, '统计日期', bold)    # 利用行和列的索引号方式，写入数字，索引号从0开始

    # 设置数据写入文件的初始行和列的索引位置
    row = 1
    col = 0

    # 迭代数据并逐行写入文件
    for name, ip,date in (host_ip):
        worksheet.write(row, col,                    name)
        worksheet.write(row, col + 1,                  ip)
        worksheet.write(row, col + 2,   date, date_format)
        row += 1
