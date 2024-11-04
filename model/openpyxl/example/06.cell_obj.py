# coding=utf-8
from openpyxl import Workbook
from openpyxl.styles import Font

wb = Workbook()  # 新建工作簿
ws = wb.active
"""获取与设置单元格值的两种方式"""
cell1 = ws.cell(1, 1)  # 先获取第一行第一列的单元格对象
cell1.value = 18  # 再设置单元格对象的值
print("值", cell1.value)
print("数字列标", cell1.column)
print("字母列标", cell1.column_letter)
print("行号", cell1.row)
print("坐标", cell1.coordinate)
cell2 = ws.cell(2, 1, 17)  # 直接在获取单元格的时候设置值
"""使用公式和不适用公式"""
cell3 = ws.cell(3, 1, "=A1+A2")  # 直接输入公式具有计算功能
cell4 = ws.cell(4, 1, "=A1+A2")
cell4.data_type = 's'  # 指定单元格数据类型为文本可以避免公式被计算 ************
"""设置格式和不设置格式"""
cell5 = ws.cell(5, 1, 3.1415)  # 默认常规格式
cell6 = ws.cell(6, 1, 3.1415)
cell6.number_format = "0.00"  # 设置格式为保留两位小数
"""超链接"""
cell7 = ws.cell(7, 1, "百度翻译")
cell7.hyperlink = "https://fanyi.baidu.com/"  # 设置超链接
# cell7.hyperlink = r"C:\Users\admin\Desktop\测试.xlsx" # 打开本地文件
# print(cell7.hyperlink.target) # 获取超链接地址
cell7.font = Font(color="0000FF", underline='single')  # 字体颜色为蓝色+下划线
wb.save(r'测试4.xlsx')  # 保存到指定路径


'''
cell.value :获取或设置值
cell.column : 数字列标
cell.column_letter : 字母列标
cell.row : 行号
cell.coordinate : 坐标,例如'A1'
cell.data_type : 数据类型, 's' = string字符串,'n' = number数值,会根据单元格值自动判断
cell.number_format :单元格格式,默认”General“常规,详见excel自定义数据类型
cell.hyperlink:获取或设置单元格超链接（可以是网址或者本地文件路径）
'''



'''
单元格样式
cell.font :获取或设置单元格Font对象
cell.border : 获取或设置单元格边框
cell.alignment : 获取或设置单元格水平、垂直对齐方式、自动换行等
cell.fill:获取或设置单元格填充颜色
'''

from openpyxl import Workbook
from openpyxl.styles import Font, Border, Side, Alignment,PatternFill
from copy import copy
wb = Workbook()
ws = wb.active
"""获取单元格并设置单元格值为 姓名 """
cell = ws.cell(1,1,"姓名")
"""设置单元格文字样式"""
cell.font = Font(bold=True, # 加粗
                         italic=True, # 倾斜
                         name="楷体", # 字体
                         size=13, # 文字大小
                         color="FF0000", # 字体颜色为红色
                         underline='single' # 下划线
                         )
"""复制单元格样式"""
cell2 = ws.cell(1,2,"学号")
cell2.font = copy(cell.font)
"""设置单元格边框为黑色边框"""
cell.border = Border(bottom=Side(style='thin', color='000000'),
                             right=Side(style='thin', color='000000'),
                             left=Side(style='thin', color='000000'),
                             top=Side(style='thin', color='000000'))
"""设置单元格对齐方式为水平居中和垂直居中，单元格内容超出范围自动换行"""
cell.alignment = Alignment(horizontal='center',vertical='center',wrap_text=True)
"""设置单元格底纹颜色为黄色"""
cell.fill = PatternFill(fill_type='solid', start_color='FFFF00')
"""
	白色：FFFFFF，黑色：000000，红色：FF0000，黄色：FFFF00
	绿色：00FF00，蓝色：0000FF，橙色：FF9900，灰色：C0C0C0
	常见颜色代码表：https://www.osgeo.cn/openpyxl/styles.html#indexed-colours
"""
wb.save(r"测试5.xlsx")



'''
列宽与行高
ws.row_dimensions[行号]：获取行对象（非行数据，包括行的相关属性、行高等）
ws.column_dimensions[字母列标]：获取列对象（非行数据，包括行的相关属性、列宽等）
get_column_letter(index)：根据列的索引返回字母
column_index_from_string(string)：根据字母返回列的索引
row.height:获取或设置行高
column.width:获取或设置列宽
'''

from openpyxl import Workbook
from openpyxl.utils import get_column_letter,column_index_from_string
wb = Workbook()
ws = wb.active
"""行"""
row = ws.row_dimensions[1]  # 获取第一行行对象
print("行号",row.index)
row.height = 20     # 设置行高 ****************
print("行高",row.height)
"""列"""
column = ws.column_dimensions["A"]     # 根据字母列标获取第一列列对象
column = ws.column_dimensions[get_column_letter(1)]    # 根据数字列标获取第一列列对象
print("字母列标",column.index)
print("数字列标",column_index_from_string(column.index))
column.width = 15  # 设置列宽 ****************
print("列宽",column.width)
wb.save(r'测试6.xlsx')
