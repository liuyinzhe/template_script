# coding=utf-8
from openpyxl import Workbook
from openpyxl.styles import Font, Border, Side, Alignment, PatternFill
wb = Workbook()
ws = wb.active
"""设置全局样式"""
border = Border(bottom=Side(style='thin', color='000000'),
                right=Side(style='thin', color='000000'),
                left=Side(style='thin', color='000000'),
                top=Side(style='thin', color='000000'))
alignment = Alignment(horizontal='center', vertical='center')
row_index = 1 # 写入的行索引,每写入一行后+1
"""写入标题"""
title = ['姓名', '学号', '分数']
for index,item in enumerate(title):
    cell = ws.cell(row_index,index+1,item) # 行索引,列索引,value
    cell.border = border # 指定边框样式
    cell.alignment = alignment # 指定对齐方式
    cell.font = Font(bold=True) # 指定字体加粗
row_index += 1 # 第二行
data = [['张三', "1101", 17],['李四', "3412", 18],['王五', "1103", 16]]
"""写入正文"""
for row in data:
    for index,item in enumerate(row):
        cell = ws.cell(row_index, index + 1, item)
        cell.border = border
        cell.alignment = alignment
    row_index += 1
"""写入结果"""
result = ["", "合计", 17+18+16]
for index,item in enumerate(result):
    cell = ws.cell(row_index,index+1,item)
    cell.border = border
    cell.alignment = alignment
    cell.fill = PatternFill(fill_type='solid', start_color="FFFF00") # 填充样式
    '''
    cell.fill 是指单元格的填充属性。
    PatternFill 是一个类,用于定义填充的样式。
    fill_type='solid' 表示填充类型是实心的。
    start_color="FFFF00" 设置了填充的起始颜色,这里的颜色代码 "FFFF00" 对应于黄色。
    '''
wb.save(r"学生信息表.xlsx")
