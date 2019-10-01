#!/usr/bin/env python
# -*- coding:utf-8 -*-
#@Time  : 2019/10/1 3:40
#@Author: 林先森
#@File  : Excel.py

import xlwt
def set_style(name, height, bold = False):
    style = xlwt.XFStyle() #初始化样式
    font = xlwt.Font() #为样式创建字体
    font.name = name
    font.bold = bold
    font.color_index = 4
    font.height = height
    style.font = font
    return style

# excelData : 列表格式数据
def write_excel(excelData, file_path):
    # 创建工作簿
    workbook = xlwt.Workbook(encoding='utf-8')
    # 创建sheet
    data_sheet = workbook.add_sheet('demo')

    # 定义循环下标
    index = 0
    for i in excelData:
    # 每一列的内容(i)
        for x, item in enumerate(i):
            # 下标(x)，单元元素(item)
            data_sheet.write(index, x, item, set_style('Times New Roman', 220, True))
        index += 1
    # sys.exit();
    # 保存文件
    workbook.save(file_path)
