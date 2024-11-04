
# coding=utf-8
from openpyxl import load_workbook
wb = load_workbook(r"测试1.xlsx")
"""获取工作表"""
active_sheet = wb.active    # 获取第一个工作表
print(active_sheet)         # 输出工作表：<Worksheet "Sheet">
by_name_sheet = wb["Sheet"]    		  # 根据工作表名称获取工作表
by_index_sheet = wb.worksheets[0]     # 根据工作表索引获取工作表
"""获取所有工作表"""
print("获取所有",wb.sheetnames)
"""新建工作表"""
New_Sheet = wb.create_sheet("New")  # 在最后新建工作表
First_Sheet = wb.create_sheet("First",index=0)  # 在开头新建工作表
print("新建后",wb.sheetnames)
"""复制工作表"""
Copy_Sheet = wb.copy_worksheet(active_sheet)    # 复制第一个工作表
Copy_Sheet.title = "Copy"
print("复制后",wb.sheetnames)
"""删除工作表"""
wb.remove(First_Sheet)      # 根据指定的工作表对象删除工作表
wb.remove(New_Sheet)
print("删除后",wb.sheetnames)
wb.save(r"测试2.xlsx")


'''
wb.active ：获取第一张工作表对象
wb[sheet_name] ：获取指定名称的工作表对象
wb.sheetnames ：获取所有工作表名称
wb.worksheets:获取所有工作表对象,wb.worksheets[0]可以根据索引获取工作表,0代表第一个
wb.create_sheet(sheet_name,index=“end”):创建并返回一个工作表对象,默认位置最后,0代表第一个
wb.copy_worksheet(sheet)：在当前工作簿复制指定的工作表并返回复制后的工作表对象
move_sheet( sheet, offset=0):移动工作表,offset代表偏移量,正数向后移,负数向前移
wb.remove(sheet)：删除指定的工作表
ws.save(path):保存到指定路径path的Excel文件中,若文件不存在会新建,若文件存在会覆盖

原文链接：https://blog.csdn.net/qq_40910781/article/details/127270735
'''

