'''
如何根据输入内容计算其在excel的列宽是多少?
利用GBK编码方式,非汉字字符占1个长度,汉字字符占2个长度
'''

from openpyxl import Workbook
from openpyxl.utils import get_column_letter,column_index_from_string
wb = Workbook()
ws = wb.active
column = ws.column_dimensions[get_column_letter(1)]    # 根据数字列标获取第一列列对象
value = "我爱中国ILoveChain"	# 4*2+10*1+1=19
column.width = len(str(value).encode("GBK"))+1  # 根据内容设置列宽,+1既可以补充误差又可以让两边留有一定的空白,美观
print("列宽",column.width)	# 输出:19
ws.cell(1,1,value)
wb.save(r'测试6.xlsx')


'''
插入和删除行、列均使用数字指定

ws.insert_rows(row_index,amount=1):在第row_index行上方插入amount列,默认插入1行
ws.insert_cols(col_index,amount=1):在第col_index列左侧插入amount列,默认插入1列
ws.delete_rows(row_index,amount=1):从row_index行开始向下删除amount行,默认删除1行
ws.delete_cols(col_index,amount=1):从col_index列开始向右删除amount行,默认删除1列
'''

from openpyxl import Workbook,load_workbook
wb = load_workbook("测试1.xlsx")
ws = wb.active
ws.insert_rows(1,2)     # 在第一行前插入两空行

delete_col_index = [1,3]    # 删除1、3两列
"""为避免删除多列时前面列对后面列产生影响,采取从后面列往前面列删的策略,行同理"""
delete_col_index.sort(reverse=True)     # 从大到小排序
for col_index in delete_col_index:
    ws.delete_cols(col_index)
wb.save(r'测试7.xlsx')


'''
插入和获取图片

ws.add_img(img,"坐标"):添加图片到指定单元格位置
'''

from openpyxl import Workbook
from openpyxl.drawing.image import Image
wb = Workbook()
ws = wb.active
img = Image('logo.png')     # 打开图片
img.width,img.height = 80,80    # 设置图片宽、高
ws.add_image(img, 'A1')
wb.save('logo.xlsx')

'''
插入和获取图片

ws._images:获取当前工作表的图片列表
'''
from openpyxl import load_workbook
from PIL import Image as PILImage
wb = load_workbook(r'logo.xlsx')
ws = wb.active
for img in ws._images:     
    img = PILImage.open(img.ref)   # 获取图片对象
    img.save(r'logo.{}'.format(img.format))     # 保存图片到指定位置
"""获取多张图片"""
for index,img in enumerate(ws._images):
    img = PILImage.open(img.ref)   # 获取图片对象
    img.save(r'图片{}.{}'.format(index+1,img.format))     # 保存图片到指定位置
