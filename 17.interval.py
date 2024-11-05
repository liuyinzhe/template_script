import re
from natsort import natsorted

def get_other_intervals(all_regions,intervals):
    '''
    给于0-base 区间,从all_regions中移除intervals区间,获得剩余区间
    返回的列表区间，可用于直接截取字符串
    all_regions = [0,83]
    intervals -> match [[3, 51], [53, 81]]
    [(0, 2), (51, 52), (81, 83)]
    '''
    # all_regions = (0,31)
    # intervals = [(2, 4), (7, 25)]
    #get_other_intervals(all_regions,intervals)
    result = [] # 不在区间内的数字
    start_idx , end_idx = all_regions
    for num  in range(start_idx,end_idx+1):
        in_interval = False
        for interval in intervals:
            if interval[0] < num < interval[1]:
                in_interval = True
                break
        if not in_interval:
            result.append(num)
    # 将结果转换为区间形式
    result_intervals = []
    start = None
    for num in result:
        if start is None:
            start = num
        if num + 1 not in result: # 移位+1,作为end  # 到了末尾
            end = num
            result_intervals.append((start, end))
            start = None
    return result_intervals


def determine_contain(position,regions):
    '''
    :param position: int
    :param regions: List[List[int]]
    :return: bool
    '''
    flag_determine = False
    for interval in regions:
        x,y = interval
        if x < position < y:
            flag_determine = True
            break
    return flag_determine
    
    
def merge_intervals(regions):
    """
    :param regions: List[List[int]]
    :return: List[List[int]]
    """

    regions.sort(key=lambda x: x[0])
    merged = []
    for interval in regions:
        if not merged or merged[-1][-1] < interval[0]:
            merged.append(interval)
        else:
            merged[-1][-1] = max(merged[-1][-1], interval[-1])
    return merged

def is_overlap(region_a, region_b):
    """
    :param region_a: List[int,int]
    :param region_b: List[int,int]
    :return: Bool
    """
    return max(region_a[0], region_b[0]) <= min(region_a[1], region_b[1])
