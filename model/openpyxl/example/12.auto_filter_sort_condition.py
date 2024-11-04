from openpyxl import load_workbook,Workbook


wb = Workbook()
ws = wb.active

rows = [
    ['月份','桃子','西瓜','龙眼'],
    [1, 38, 28, 29],
    [2, 52, 21, 35],
    [3, 39, 20, 69],
    [4, 51, 29, 41],
    [5, 39, 39, 31],
    [6, 30, 41, 39],
]

for row in rows:
    ws.append(row)

ws.auto_filter.ref = 'A1:D7'
#ws.auto_filter.add_filter_column(1, ['39', '51', '30']) # 第二列
ws.auto_filter.add_filter_column(0,[]) #全选
ws.auto_filter.add_filter_column(1,[])
ws.auto_filter.add_filter_column(2,[])
ws.auto_filter.add_filter_column(3,[])

ws.auto_filter.add_sort_condition('C2:C7',descending=True) # 排序条件,降序
wb.save(r'filter_sort.xlsx')


###############  pandas ####################


import pandas as pd 

df = pd.read_excel("filter_sort.xlsx",sheet_name='Sheet')
df_value = df.sort_values(by=["桃子","西瓜"],ascending=False)#,inplace=True) # 倒序

with pd.ExcelWriter("filter_sort2.xlsx",engine='openpyxl') as writer:
    df_value.to_excel(writer,sheet_name='Sheet',index=False)


