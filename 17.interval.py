import re
from natsort import natsorted

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
