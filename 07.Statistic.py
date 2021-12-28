import math
import scipy
import numpy as np

def cut_bin(lst,bin_len):
    '''
    1维 列表拆分bin [1, 3, 4, 5, 6, 7, 11, 33, 45, 21]
    # bin 的最大值限制表
    [5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
    # 最终分bin 结果
    [[1, 3, 4], [5, 6, 7], [11], [], [21], [], [33], [], [], [45]]
    '''
    lst_sorted = sorted(lst)
    min_limit = min(lst)
    upper_limit = max(lst) +1 + bin_len
    #list_arr0=list(filter( lambda x :x < upper_limit, range(bin_len,upper_limit,bin_len)))
    # 整除
    coefficient = min_limit//bin_len
    if coefficient == 0:
        upper_limit = max(lst) +1
    bin_limit=list(range(bin_len*(coefficient+1),upper_limit,bin_len))
    #bin_limit=list(range(bin_len,upper_limit,bin_len))
    #print(bin_limit)
    all_bin_lst = []
    for idx in range(len(bin_limit)):
        if idx != 0:
            min_limit = bin_limit[idx - 1 ]
        max_limit = bin_limit[idx]
        bin_lst=list(filter(lambda x :min_limit <= x < max_limit,lst_sorted))
        all_bin_lst.append(bin_lst)
    return all_bin_lst,bin_limit

def cut_cols_bin(lst,bin_len):
    '''
     二维列表，根据第一列分bin,根据index 拆分第二列也成为对应bin
    '''
    #print(lst)
    col1_lst =  [x[0] for x in lst]
    col2_lst =  [x[1] for x in lst]
    min_limit = int(min(col1_lst))
    upper_limit = int(max(col1_lst)) +1 + bin_len
    #list_arr0=list(filter( lambda x :x < upper_limit, range(bin_len,upper_limit,bin_len)))
    # 整除
    coefficient = min_limit//bin_len
    bin_limit=list(range(bin_len*(coefficient+1),upper_limit,bin_len))
    #print(bin_limit)
    all_bin_col1_lst = []
    all_bin_col2_lst = []
    for idx in range(len(bin_limit)):
        if idx != 0:
            min_limit = bin_limit[idx - 1 ]
        max_limit = bin_limit[idx]
        col1_bin_lst=list(filter(lambda x :min_limit <= x < max_limit,col1_lst))
        all_bin_col1_lst.append(col1_bin_lst)
        length = len(col1_bin_lst)
        col2_bin_lst = [col2_lst.pop(0) for x in range(length)]
        all_bin_col2_lst.append(col2_bin_lst)
    return all_bin_col1_lst,all_bin_col2_lst,bin_limit
