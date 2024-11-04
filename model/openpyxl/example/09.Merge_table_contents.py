# coding=utf-8
from openpyxl import Workbook,load_workbook
import os
dir_path = "学生名单"  # 要合并文件的文件夹地址
"""读取文件夹下的所有excel文件"""
files = []
for file in os.listdir(dir_path): # 获取当前目录下的所有文件
    files.append(os.path.join(dir_path,file)) # 获取文件夹+文件名的完整路径


"""以第一个文件为基本表"""
merge_excel = load_workbook(files[0])
merge_sheet = merge_excel.active


"""遍历剩余文件，追加到基本表"""
for file in files[1:]:
    wb = load_workbook(file)
    ws = wb.active
    for row in list(ws.values)[1:]:  # 从第二行开始读取每一行并追加到基本表
        merge_sheet.append(row)
merge_excel.save("高一学生汇总.xlsx")
