
# coding=utf-8
from openpyxl import load_workbook
wb = load_workbook(r'测试1.xlsx') # 获取已存在的工作簿
ws = wb.active
print("工作表名",ws.title)
ws.title = "学生信息表"
print("修改后工作表名",ws.title)
print("最大行数",ws.max_row)
print("最大列数",ws.max_column)
ws.append(["王五","1103",17])
print("最大行数",ws.max_row)
wb.save(r"测试3.xlsx")

'''
ws.title:获取或设置工作表名
ws.max_row:工作表最大行数
ws.max_column:工作表最大列数
ws.append(list):表格末尾追加数据
ws.merged_cells:获取所有合并单元格
ws.merge_cells('A2:D2'):合并单元格
ws.unmerge_cells('A2:D2'):解除合并单元格。

'''