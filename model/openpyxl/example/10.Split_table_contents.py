# coding=utf-8
from openpyxl import Workbook,load_workbook
import os
file_path = "高一学生汇总.xlsx" # 要拆分的文件地址
split_dir = "拆分结果"  # 拆分文件后保存的文件夹
group_item = "班级"	 # 拆分的依据字段


"""打开拆分的excel文件并读取标题"""
wb = load_workbook(file_path)
ws = wb.active
title = []  # list
for cell in ws[1]: # sheet 第二行
    title.append(cell.value)


"""开始分组，分组结果保存到字典，键为班级名，值为班级学生列表"""
group_result = {}  # 存储分组结果
group_index = title.index(group_item) 	# 获取拆分依据字段的索引
for row in list(ws.values)[1:]:
    class_name = row[group_index] # 获取分组依据数据，即班级名
    if class_name in group_result:    # 如果分组存在就追加，不存在就新建
        group_result[class_name].append(row)
    else:
        group_result[class_name] = [row]


"""创建输出文件夹"""
if not os.path.exists(split_dir):   # 如果不存在文件夹就新建
    os.mkdir(split_dir)
os.chdir(split_dir)     # 进入拆分文件夹


"""打印并输出分组后的数据"""
for class_name,students in group_result.items():
    new_wb = Workbook()     # 新建excel
    new_ws = new_wb.active
    new_ws.append(title)    # 追加标题
    for student in students:
        new_ws.append(student)  # 讲分组数组追加到新excel中
    new_wb.save("{}.xlsx".format(class_name))
