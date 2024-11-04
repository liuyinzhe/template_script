# coding=utf-8
from openpyxl import Workbook
wb = Workbook() # 新建工作簿
ws = wb.active # 获取第一张工作表
ws.append(['姓名', '学号', '年龄']) # 追加一行数据
ws.append(['张三', "1101", 17]) # 追加一行数据
ws.append(['李四', "1102", 18]) # 追加一行数据
wb.save(r'测试1.xlsx') # 保存到指定路径，保存的文件必须不能处于打开状态，因为文件打开后文件只读
