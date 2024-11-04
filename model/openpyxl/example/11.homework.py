# encoding: utf-8
import os
from openpyxl import Workbook, load_workbook
excel_path = r"学生名单/高一1班.xlsx"    # excel文件路径
job_path = r"作业"     # 作业文件夹路径

"""获取姓名列表"""
wb = load_workbook(excel_path)
ws = wb.active
names = []
for cell in ws["C"][1:]:	# 获取第C列第2行开始的数据
    names.append(cell.value)

"""获取作业列表"""
os.chdir(job_path)  # 切换到作业目录
files = []    # 获取文件列表
for file in os.listdir():
    files.append(os.path.splitext(file)[0])

"""作业检测"""
yes,no = [],[]
for name in names:     # 逐个姓名判断
    if name in files:   # 判断姓名是否在文件列表中
        yes.append(name)    # 如果在，添加到已完成名单
    else:
        no.append(name)     # 否则，添加到未完成名单
print("已完成人数：{}，已完成名单：{}".format(len(yes),yes))
print("未完成人数：{}，未完成名单：{}".format(len(no),no))
