#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
本脚本基于 以下内容进行修改，用于合并目录下多个excel文件的sheet;
(1)不限制两两之间合并,可以任意数量
(2)删除结果文件最前面的空白 Sheet

#【python】带格式合并两个excel中的所有或部分sheet
# https://blog.csdn.net/sinat_32872729/article/details/125853207

#【openpyxl】操作工作表（创建、改名、移动、复制、删除）
# https://blog.csdn.net/qq_39147299/article/details/123346804
"""

from openpyxl.utils import get_column_letter
from openpyxl import load_workbook
from openpyxl import Workbook
import copy
from pathlib import Path



#【python】带格式合并两个excel中的所有或部分sheet
# https://blog.csdn.net/sinat_32872729/article/details/125853207

#【openpyxl】操作工作表（创建、改名、移动、复制、删除）
# https://blog.csdn.net/qq_39147299/article/details/123346804

def GetAllFilePaths(pwd,wildcard='*'):
    '''
    获取目录下文件全路径，通配符检索特定文件名，返回列表
    param: str  "pwd"
    return:dirname pathlab_obj
    return:list [ str ]
    #https://zhuanlan.zhihu.com/p/36711862
    #https://www.cnblogs.com/sigai/p/8074329.html
    '''
    files_lst = []
    target_path=Path(pwd)
    for child in target_path.rglob(wildcard):
        if child.is_dir():
            pass
        elif child.is_file():
            files_lst.append(child)
    return files_lst

# 不用
def copy_sheet(ws1, ws2):
    """
    ws1: source
    ws2: target
    把ws1的复制到ws2 （仅复制数值，不复制格式）
    """
    mr = ws1.max_row
    mc = ws1.max_column
  
    # copying the cell values from source 
    # excel file to destination excel file
    for i in range (1, mr + 1):
        for j in range (1, mc + 1):
            # reading cell value from source excel file
            c = ws1.cell(i, j)

            # writing the read value to destination excel file
            ws2.cell(i, j).value = c.value
    return ws2


def styles_copy(source_cell, target_cell):
    target_cell._style = copy.copy(source_cell._style)
    target_cell.font = copy.copy(source_cell.font)
    target_cell.border = copy.copy(source_cell.border)
    target_cell.fill = copy.copy(source_cell.fill)
    target_cell.number_format = copy.copy(source_cell.number_format)
    target_cell.protection = copy.copy(source_cell.protection)
    target_cell.alignment = copy.copy(source_cell.alignment)
    return target_cell


def copy_sheet_all(sheet, sheet2):
    """
    复制sheet到sheet2中，带格式复制
    """
    # tab颜色
    sheet2.sheet_properties.tabColor = sheet.sheet_properties.tabColor

    # 开始处理合并单元格形式为“(<CellRange A1：A4>,)，替换掉(<CellRange 和 >,)' 找到合并单元格
    wm = list(sheet.merged_cells)
    if len(wm) > 0:
        for i in range(0, len(wm)):
            cell2 = str(wm[i]).replace('(<CellRange ', '').replace('>,)', '')
            sheet2.merge_cells(cell2)

    for i, row in enumerate(sheet.iter_rows()):
        sheet2.row_dimensions[i+1].height = sheet.row_dimensions[i+1].height
        for j, cell in enumerate(row):
            sheet2.column_dimensions[get_column_letter(j+1)].width = sheet.column_dimensions[get_column_letter(j+1)].width
            sheet2.cell(row=i + 1, column=j + 1, value=cell.value)

            # 设置单元格格式
            source_cell = sheet.cell(i+1, j+1)
            target_cell = sheet2.cell(i+1, j+1)
            target_cell.fill = copy.copy(source_cell.fill)
            if source_cell.has_style:
                styles_copy(source_cell, target_cell)
    return sheet2


def file2list(fx):
    lst = []
    if not fx:
        return  lst
    with open(fx, 'r') as f:
        for line in f:
            lst.append(line.strip())
    return lst


def create_copy_sheets(wb, wbx, exists_names=[], allsheet=True, sub_sheetlst=[]):
    """将wbx中的所有/部分sheet写入到wb
    wb yes: sheet插入目标工作簿
    wbx yes: 源工作簿
    exists_names: 目标工作簿中已经存在的sheet名称
    allsheet: 是否将wbx中的所有sheet写入到wb
    sub_sheetlst: 需要写入的sheet名称列表
    """
    for n in wbx.sheetnames:
        if not allsheet:
            if n not in sub_sheetlst:
                continue
        if n in exists_names:
            sheetname = n+'_a'  # 同名sheet, 改为sheet_name+'_a'
        else:
            sheetname = n
        ws = wb.create_sheet(title=sheetname)
        # 不带格式赋值 sheet
        # wsc = copy_sheet(wbx[n], ws)
        # 带格式赋值 sheet
        wsc = copy_sheet_all(wbx[n], ws)
    return wb


if __name__ == '__main__':

    current_dir = Path.cwd()

    files_lst = GetAllFilePaths(current_dir,wildcard='*.xlsx')
    merged_excel = current_dir.joinpath('merged.xlsx')

    # 空的目标
    wb = Workbook()
    ex_names = []
    for  file in files_lst:
        wb_obj = load_workbook(file)
        '''
        # 修改sheetnames
        new_sheetname = 'NewSheetName'
        current_sheetname = book.sheetnames[0]  # 假设我们要修改第一个sheet的名称
        sheet = wb_obj[current_sheetname]
        # sheet = wb_obj['Sheet1'] 
        sheet.title = new_sheetname
        '''
        ex_names = wb.sheetnames
        #print(ex_names)
        if len(ex_names) == 0:
            wb = create_copy_sheets(wb, wb_obj, exists_names=[])
            # 已经有的sheet 名称
            ex_names = wb.sheetnames
        else:
            wb = create_copy_sheets(wb, wb_obj, exists_names=ex_names)  
    # 保存前删除第一个空白Sheet
    del wb["Sheet"] 
    #保存合并后内容
    wb.save(merged_excel)
    print("#Note: '%s' saved!" % merged_excel)
