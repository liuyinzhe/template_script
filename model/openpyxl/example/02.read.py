# coding=utf-8
from openpyxl import load_workbook
wb = load_workbook(r'测试1.xlsx') # 获取已存在的工作簿
ws = wb.active # 获取第一张工作表
for row in ws.values: # 输出所有数据
    print(row)
print(ws[1]) # 第二行
# for cell in ws["C"][1:]:	# 获取第C列第2行开始的数据
#     print(cell.value)