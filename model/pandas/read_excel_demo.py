import pandas as pd
import os
from pathlib import Path
#pwd = os.path.split(os.path.realpath(__file__))[0]
pwd = os.getcwd()
pwd = Path(pwd)
os.chdir(pwd)

# https://blog.csdn.net/qq_18351157/article/details/105261636

df = pd.read_excel('example.xlsx',sheet_name='Sheet1')

# for  index,value in enumerate(df):
#     print(index,value)
#     print(df[value]) # print(df['name'])

'''
逐列检索
DataFrame.iteritems()
逐行检索
DataFrame.iterrows()
DataFrame.itertuples()
'''
# for  index,row in df.iterrows():
#     print(index,row)
#     print(row)
#     print(type(row))
#     print(row[2])
#     break
for  row in df.itertuples():
    print(row)
    print(row[0]) # index
    number = row[1]
    name = row[2]
