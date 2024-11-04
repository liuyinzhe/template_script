# coding=utf-8
from openpyxl import load_workbook
wb = load_workbook(r'测试1.xlsx')
ws = wb.active
A1 = ws["A1"]     # 根据坐标获取单个单元格
print("第一行第一列",ws.cell(1,1))    # 根据行列获取单个单元格
print("第一行",ws[1])
print("第A列",ws["A"])
print("A到B列",ws["A":"B"])
print("1到2行",ws["1":"2"])
print("A1到B2范围",ws["A1":"B2"])


'''
ws['A1']'根据坐标获取单个单元格对象
ws.cell(row, column, value=None)'根据行列获取单个单元格对象,其中cell(1,1)代表A1
ws[1]'获取第一行所有单元格对象,ws[“1”]也可
ws[“A”]'获取第A列所有单元格对象
ws[“A”:“B”]'获取A到B列所有单元格对象,ws[“A:B”]也可
ws[1:2]'获取1到2行所有单元格对象,ws[“1:2”]也可
ws[“A1”:“B2”]'获取A1到B2范围所有单元格对象,ws[“A1:B2”]也可。
'''

# ws.values:获取所有单元格数据的可迭代对象，可以通过for循环迭代或通过list(ws.values)转换为数据列表
# coding=utf-8
from openpyxl import load_workbook
wb = load_workbook(r'测试1.xlsx')     # 获取已存在的工作簿
ws = wb.active  # 获取工作表
for row in ws.values:       # for循环迭代
    print(row)
print(list(ws.values))	    # 转换为数据列表
'''
('姓名', '学号', '年龄')
('张三', '1101', 17)
('李四', '1102', 18)
[('姓名', '学号', '年龄'), ('张三', '1101', 17), ('李四', '1102', 18)]
'''


'''
ws.rows:获取所有数据以行的格式组成的可迭代对象
ws.columns:获取所有数据以列的格式组成的可迭代对象
'''

# coding=utf-8
from openpyxl import load_workbook
wb = load_workbook(r'测试1.xlsx')
ws = wb.active
for row in ws.rows:  # 以行的形式迭代
    print(row)
    #print(row[0].value)
print("-"*55)
for col in ws.columns:  # 以列的形式迭代
    print(col)


'''
ws.iter_rows(min_row=None, max_row=None, min_col=None, max_col=None):获取指定边界范围并以行的格式组成的可迭代对象，默认所有行
ws.iter_cols(min_col=None, max_col=None, min_row=None, max_row=None):获取指定边界范围并以列的格式组成的可迭代对象，默认所有列

原文链接：https://blog.csdn.net/qq_40910781/article/details/127270735
'''

# coding=utf-8
from openpyxl import load_workbook
wb = load_workbook(r'测试1.xlsx')
ws = wb.active
print("-"*35)
for row in ws.iter_rows(max_row=2,max_col=2):  # 指定边界范围并以行的形式可迭代
    print(row)
print("-"*35)
for column in ws.iter_cols(max_row=2,max_col=2):  # 指定边界范围并以行的形式可迭代
    print(column)


