#!/usr/bin/env python3

'''
usage:
    python 
 
mod:
'''

import sys
import os
import re
import json
import math
import time
import datetime
import argparse
from pathlib import Path
import subprocess
import pysam


def calc_quantile(numlist,method='nearest'):
    '''
    input : numlist 
    method
    ['linear', 'lower', 'higher', 'midpoint', 'nearest']
    https://numpy.org/doc/stable/reference/generated/numpy.quantile.html
    '''
    lower_q = np.quantile(numlist,0.25,method=method)
    median = np.quantile(numlist,0.5,method=method)
    higher_q = np.quantile(numlist,0.75,method=method)
    
    return lower_q,median,higher_q



###################小工具     BEGIN#################
##
#

def reverse_complement(seq):
    '''get reverse complement  seq'''
    rule = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G', 'N': 'N'}
    return ''.join([rule[each] for each in seq.upper()][::-1])

def split_list(raw_list,split_num):
    '''
    将一个大列表分割为包含多个小列表的大列表
    用于后面多进程分析
    '''
    list_len=len(raw_list)
    split_len=(list_len//split_num)+1
    sub_len=list_len
    result_list=[]
    sub_list=[]
    start_idx=0
    for index in range(0,list_len):
        if index !=0:
            if index==list_len-1:
                sub_list=raw_list[start_idx:index+1]
                result_list.append(sub_list)
                return result_list
            if index%split_len==0:
                sub_list=raw_list[start_idx:index]
                result_list.append(sub_list)
                start_idx=index
        elif index ==0 and list_len==1:
            result_list.append(raw_list)
    return result_list


def dicMeg(dic1,dic2):
    """
    嵌套字典合并，参数1旧字典，参数2新字典，结果是将新字典合并到旧字典中
    利用函数调用自己无限循环直到keys 被遍历完，保证dic1 中存入了左右dic2的keys 与values
    https://www.jianshu.com/p/c6768fe13727
    a={'a':{'x':1}}
    b={'a':{'y':2}}
    dicMeg(a,b)
    {'a':{'x':1,'y':2}}
    #a.update(b) 只更新一层，key a 的值就被替换了
    #{'a':{'y':2}}
    """
    for i in dic2:
        #print(i)
        if i in dic1:
            if type(dic1[i]) is dict and type(dic2[i]) is dict:
                dicMeg(dic1[i],dic2[i])
        else:
            dic1[i] = dic2[i]
    return dic1

#
##
###################小工具     END#################




###################用于bam  方法  BEGIN#################
##
#
#以下4个函数 在这个脚本里只用了judge_softclip
def change_reads_pos(length, start, end):
    '''
    对于reads 方向反的情况获得reads反向互补的相对坐标
    '''
    #1-base
    #s = 1 + length - end
    #e = 1 + length - start
    #0-base
    s = length - end
    e = length - start
    return s, e


def get_ref_pos(read):
    '''
    pysam
    return reads obj attribute
    rstart, rend 是相对测序reads 方向的坐标
    #特殊修改，遇到负链，将其转换为正链的坐标;用于后期检查谁是最近断点
    '''
    length = read.query_length
    rstart = read.query_alignment_start
    rend = read.query_alignment_end
    stand = "+"
    if read.is_reverse:
        rstart, rend = change_reads_pos(length, rstart, rend)
        stand = "-"
    chro = read.reference_name
    #1-base
    #return [chro, read.reference_start+1, read.reference_end+1,  rstart+1, rend+1, stand]
    #0-base
    return [chro, read.reference_start, read.reference_end,  rstart, rend, stand]


def get_ref_pos_mp(hit,q_len):
    '''
    mappy
    return hit obj attribute
    rstart, rend 是相对测序reads 方向的坐标
    #特殊修改，遇到负链，将其转换为正链的坐标;用于后期检查谁是最近断点
    '''
    length = q_len
    rstart = hit.q_st
    rend = hit.q_en
    stand = "+"
    if hit.strand == -1:
        rstart, rend = change_reads_pos(length, rstart, rend)
        stand = "-"
    chro = hit.ctg
    #1-base
    #return [chro, read.reference_start+1, read.reference_end+1,  rstart+1, rend+1, stand]
    #0-base
    return [chro, hit.r_st, hit.r_en,  rstart, rend, stand]

def pos_overlap(start, end, rstart, rend):
    hasOverLap = False
    if (int(rstart) < int(end) <= int(rend)) or (int(rstart) <= int(start) < int(rend)):
        hasOverLap = True
    elif (int(start) <= int(rstart) < int(end)) or (int(start) < int(rstart) <= int(end)):
        hasOverLap = True
    return hasOverLap


def judge_softclip(read, clip_min_len=10):
    '''
    ***discard function***
    reads 两侧 有大于5bp 的soft-clipping base 就算 softclip reads
    #[read_dict[read][0].cigartuples]
    #[(4, 58), (4, 8515)]  45.6
    #[(4, 30), (4, 20287)]  43  大于30 就算
 
    #read.cigartuples
    # return [(0, 151)]
    alignment   meaning operation
    M   BAM_CMATCH  0
    I   BAM_CINS    1
    D   BAM_CDEL    2
    N   BAM_CREF_SKIP   3
    S   BAM_CSOFT_CLIP  4
    H   BAM_CHARD_CLIP  5
    P   BAM_CPAD    6
    =   BAM_CEQUAL  7
    X   BAM_CDIFF   8
    B   BAM_CBACK   9
 
    '''
    #print(get_ref_pos(read))
    #print(read.query_name)
    #print(read.is_unmapped)
    if read.is_unmapped:
        return False
    softclip_list = [x[1] for x in read.cigartuples if x[0] == 4]
    if len(softclip_list) > 1:
        left = softclip_list[0]
        right = softclip_list[1]
        if left >= clip_min_len or right >= clip_min_len:
            return True
        else:
            return False
    elif len(softclip_list) == 1:
        if softclip_list[0] >= clip_min_len:
            return True
        else:
            return False
    else:
        return False

def get_supplementary_Alignment(read):
    '''
    #使用:
    # 一般分析 带上 -M 参数
    # 有些软件不会去处理supplemenary(split alignments),比如Picard's markDuplicates,所以可能需要用-M把supplemenary 转换为secondary。
    # 对于插入检测分析,不要使用 -M 参数;可以获得更多的 supplemenary alignments信息 ,用于检测插入序列

    # bwa mem parameter -M -Y
    # -M:mark shorter split hits as secondary; 把supplemenary alignment(flag值2048) 变为no primary(flag值256)
    # -Y:use soft clipping for supplementary alignments; 仅仅是 58H34M变为58S34M 表示, 依然是 supplementary alignments
    # 参考:
    # Secondary ,Supplementary alignment 和bwa mem的-M -Y参数
    # https://www.cnblogs.com/timeisbiggestboss/p/8856888.html
    # bwa -M 参数解读
    # https://blog.csdn.net/tanzuozhev/article/details/79037340

    SA:Z:(rname ,pos ,strand ,CIGAR ,mapQ ,NM ;)
    只能找到标记的 supplementary_Alignment , 有些split_reads 没有判断那为 supplementary_Alignment
    1.rname: sa_chr：补充比对的参考序列名称（染色体名称）。
    2.pos: sa_pos：补充比对的起始位置。
    3.strand: sa_strand：补充比对的方向（正向或反向）。
    4.CIGAR: sa_cigar：补充比对的CIGAR字符串，描述了比对中的匹配、插入、删除等操作。
    5.mapQ: sa_mapq：补充比对的映射质量。
    6.NM;: sa_match：补充比对的匹配长度。
    在之前的示例代码中，sa_tag.split(',')返回的是一个包含上述信息的列表。每个元素分别对应上述的一列。

    SA:Z:seq2,361,+,62M46S,60,0; -> seq2,361,+,62M46S,60,0
    '''
    try :
        sa_tag_str = read.get_tag('SA')
    except KeyError:
        return None
    '''
    A_chrom,310,+,105S45M,60,0;
    B_chrom,6971,-,103S47M,0,0;C_chrom,36224645,-,77S11M2D32M30S,0,2;
    '''
    sa_tag_lst = re.split(";",sa_tag_str)
    all_tag_values = []
    for sa_tag in sa_tag_lst:
        sa_chr, sa_pos, sa_strand, sa_cigar, sa_mapq, sa_match = sa_tag.split(',')
        all_tag_values.append([sa_chr,sa_pos,sa_strand,sa_cigar,sa_mapq,sa_match])
    #print(f"Read {read.query_name} has a supplementary alignment at {sa_chr}:{sa_pos} on strand {sa_strand}")
    return all_tag_values

def Mismatch_counter(read):
    '''
    96C53
    20^TGC4T77
    17A2A20A6A28G72
    https://lh3.github.io/2018/03/27/the-history-the-cigar-x-operator-and-the-md-tag
    R: AAAAAAAAAAATTTTT--GTTTTT
    Q: AAAAAAAAAAGTTTTTACATTTTT
    since this would be "10A5^ACG5".

    150
    总结：数字表示匹配，碱基表示错配，^碱基表示del。
    https://www.zxzyl.com/archives/1484/
    但需要注意的MD不包含insertion，含有insertion的字符串表示更复杂，需要与CIGAR联合看。
    '''
    deletion_base_count = 0
    insertion_base_count = 0
    # 获取CIGAR字符串并分析插入和删除
    cigar_tuples = read.cigartuples
    for operation, length in cigar_tuples:
        if operation == 1:  # 插入
            insertion_base_count += length
        elif operation == 2:  # 删除
            deletion_base_count += length
    mismatch_count = 0
    # 获取MD标签
    md_tag = read.get_tag("MD")
    pattern = re.compile(r"[ATGC]")
    if "^" in md_tag:
        match_list = pattern.findall(md_tag)
        mismatch_count = len(match_list) - deletion_base_count
    else:
        match_list = pattern.findall(md_tag)
        mismatch_count = len(match_list)
        
    return mismatch_count

def cigar_detect(read,cigar_idex,min_len=0):
    '''
    cigar_dic = {'M':0,'I':1,'D':2,'N':3,'S':4,'H':5,'P':6,'=':7,'X':8,'B':9}
    cigar_idex = cigar_dic['M']
    read_name ,info_list= cigar_detect(read,cigar_idex,min_len)
    
    # read_obj 对象
    # min_len指定cigar之值的最小数量
    # cigar_dic = {'M':0,'I':1,'D':2,'N':3,'S':4,'H':5,'P':6,'=':7,'X':8,'B':9}
    # cigar_idex = cigar_dic['M']
    基于比对, 根据 cigar_idex  获取 reads名，坐标信息，reads 数据来源坐标，变异长度以及 正负链信息 的列表;
    NOTE: reads 的相对坐标调整为了测序reads 的想对坐标，而不是比对的，如果需要比对的信息，请用cigar2tab，或者修改或者去掉此函数中change_reads_pos函数的调用
    [chrom,ref_pos_start_tmp,ref_pos_end_tmp,read_pos_start_tmp,read_pos_end,var_len,stand]
    主要用于 INS DEL INV 数据后续合并可用于稀有TRA的检测
    alignment   meaning operation
    M   BAM_CMATCH  0
    I   BAM_CINS    1
    D   BAM_CDEL    2
    N   BAM_CREF_SKIP   3   #CIGAR: skip on the reference (e.g. spliced alignment)
    S   BAM_CSOFT_CLIP  4
    H   BAM_CHARD_CLIP  5
    P   BAM_CPAD    6   # padding # P 6 padding (silent deletion from padded reference)
    =   BAM_CEQUAL  7
    X   BAM_CDIFF   8
    B   BAM_CBACK   9   # It was never really used.
    '''
    
    read_name = read.query_name
    chrom = read.reference_name
    ref_pos_start = read.reference_start # 0-base
    ref_pos_end = read.reference_end # 0-base
    read_pos_start = read.query_alignment_start # 0-base
    read_pos_end = read.query_alignment_end # 0-base
    query_length = read.query_length
    #print(read_name,chrom,ref_pos_start,ref_pos_end,read_pos_start,read_pos_end,query_length)
    stand = '-' if  read.is_reverse else '+' #  is negative 相对与参考基因组方向
    #stand = '+'
    
    #循环cigarstring 或者 cigartuples
    #cigarstring = read.cigarstring
    cigartuples = read.cigartuples
    #print(cigartuples[0:10])
    type_info_list = []
    target_info_lst = []
    if cigar_idex == 4 or cigar_idex == 5: #单独统计 soft/hard softclip
        flag,var_len = cigartuples[0]
        if flag == 4 and var_len >= min_len: #softclip
            read_pos_end_tmp = read_pos_start
            read_pos_start_tmp = 0
            ref_pos_end_tmp = ref_pos_start
            ref_pos_start_tmp = None
            if stand == '-':
                read_pos_start_tmp, read_pos_end_tmp = change_reads_pos(query_length, read_pos_start_tmp, read_pos_end_tmp)
            type_info_list = [chrom,ref_pos_start_tmp,ref_pos_end_tmp,read_pos_start_tmp,read_pos_end_tmp,var_len,stand]
            target_info_lst.append(type_info_list)
        
        flag,var_len = cigartuples[-1]
        if flag == 4 and var_len >= min_len: #softclip
            read_pos_start_tmp = read_pos_end 
            read_pos_end_tmp = query_length 
            ref_pos_start_tmp = ref_pos_end
            ref_pos_end_tmp = None
            if stand == '-':
                read_pos_start_tmp, read_pos_end_tmp = change_reads_pos(query_length, read_pos_start_tmp, read_pos_end_tmp)
                # s = query_length - read_pos_end_tmp
                # e = query_length - read_pos_start_tmp
            type_info_list = [chrom,ref_pos_start_tmp,ref_pos_end_tmp,read_pos_start_tmp,read_pos_end,var_len,stand]
            target_info_lst.append(type_info_list)
        #target_info_lst = sorted(target_info_lst,key=lambda x:(x[1],x[2]))#根据参考基因组 start 与end 升序排序
        return read_name, target_info_lst
        #change_reads_pos(length, start, end)
    tuple_len = len(cigartuples)
    #for flag,var_len in cigartuples: # 不统计 softclip
    for idx in range(tuple_len):
        flag,var_len = cigartuples[idx]
        # reads 长度统计 S5,H4,M0{7，8}，I1 
        # ref 统计 M0{7,8}, D2，N3,P6，
        read_flag_list = [0,1,4,5,7,8]
        ref_flag_list = [0,2,3,6,7,8]

        if idx == 0 :  #从左侧第一个碱基开始，包括 mismatch match ;
            read_pos_start = 0  # 顺序是从左到右，第一个softclip,右侧的第二个softclip 不会遇到
            read_pos_end = 0    # 第一个softclip 记录 start == end ,后面 计算时根据var_len 累加
            ref_pos_end = ref_pos_start
        #reads
        if flag == 4 or cigar_idex == 5 : #  BAM_CSOFT_CLIP soft/hard clipping base ref 不统计，位于两侧
            if idx == tuple_len: #最右侧
                read_pos_start = read_pos_end
                read_pos_end = read_pos_end + var_len # 左开右闭区间
            else:
                read_pos_start = var_len  # 顺序是从左到右，第一个softclip,右侧的第二个softclip 不会遇到
                read_pos_end = var_len    # 第一个softclip 记录 start == end 
            continue # reads 累加 ; ref 不统计 softclip/hardclip
        

        if stand == '-':
            if flag in read_flag_list : # reads 长度累加有关的flag
                read_pos_start = read_pos_end
                read_pos_end = read_pos_start + var_len # 左开右闭区间
            else:
                read_pos_start = read_pos_end
                read_pos_end = read_pos_start
        else:
            if flag in read_flag_list : # reads 长度累加有关的flag
                #print(read_pos_start,read_pos_end)
                read_pos_start = read_pos_end
                read_pos_end = read_pos_start + var_len # 左开右闭区间
            else:
                #print(read_pos_start,read_pos_end)
                read_pos_start = read_pos_end
                read_pos_end = read_pos_start

        #ref
        if flag in ref_flag_list :  # ref 坐标 长度累加有关的flag
            #print(ref_pos_start,ref_pos_end)
            ref_pos_start = ref_pos_end
            ref_pos_end =  ref_pos_start + var_len # 左开右闭闭区间
        else:
            ref_pos_start = ref_pos_end 
            ref_pos_end =  ref_pos_start
        
        
        if var_len >= min_len and cigar_idex == flag :
            #print(var_len,min_len)
            if stand == '-':
                read_pos_start_tmp, read_pos_end_tmp = change_reads_pos(query_length, read_pos_start, read_pos_end)
                #read_pos_start_tmp, read_pos_end_tmp = read_pos_start, read_pos_end
                #print(read_name,read_pos_start, read_pos_end,read_pos_start_tmp, read_pos_end_tmp,cigarstring)
                #print(read.query_alignment_start,read.query_alignment_end,read_pos_start, read_pos_end,query_length,read_pos_start_tmp, read_pos_end_tmp)
                type_info_list = [chrom,ref_pos_start,ref_pos_end,read_pos_start_tmp,read_pos_end_tmp,var_len,stand]
            else:
                type_info_list = [chrom,ref_pos_start,ref_pos_end,read_pos_start,read_pos_end,var_len,stand]
                #print(type_info_list)
            target_info_lst.append(type_info_list)
    #target_info_lst = sorted(target_info_lst,key=lambda x:(x[1],x[2]))#根据参考基因组 start 与end 升序排序
    return read_name, target_info_lst

def cigar2tab(read):
    '''
    解析为列表;由于可能遇到较高的深度，使用yield 返回结果；避免内存爆炸
    alignment   meaning operation
    M   BAM_CMATCH  0
    I   BAM_CINS    1
    D   BAM_CDEL    2
    N   BAM_CREF_SKIP   3   #CIGAR: skip on the reference (e.g. spliced alignment)
    S   BAM_CSOFT_CLIP  4
    H   BAM_CHARD_CLIP  5
    P   BAM_CPAD    6   # padding # P 6 padding (silent deletion from padded reference)
    =   BAM_CEQUAL  7
    X   BAM_CDIFF   8
    B   BAM_CBACK   9   # It was never really used.

    * BAM_CIGAR_TYPE  QUERY  REFERENCE
    * --------------------------------
    * BAM_CMATCH      1      1
    * BAM_CINS        1      0
    * BAM_CDEL        0      1
    * BAM_CREF_SKIP   0      1
    * BAM_CSOFT_CLIP  1      0
    * BAM_CHARD_CLIP  0      0
    * BAM_CPAD        0      0
    * BAM_CEQUAL      1      1
    * BAM_CDIFF       1      1
    * BAM_CBACK       0      0
    * --------------------------------
    '''
    
    read_name = read.query_name
    chrom = read.reference_name
    ref_pos_start = read.reference_start # 0-base
    #ref_pos_end = read.reference_end # 0-base
    ref_pos_end = 0 #
    read_pos_start = read.query_alignment_start # 0-base
    read_pos_end = read.query_alignment_end # 0-base
    query_length = read.query_length
    #print(read_name,chrom,ref_pos_start,ref_pos_end,read_pos_start,read_pos_end,query_length)
    stand = '-' if  read.is_reverse else '+' #  is negative 相对与参考基因组方向
    #stand = '+'
    target_info_lst = []
    cigar_lst = ['M','I','D','N','S','H','P','=','X','B']
    '''
     * BAM_CIGAR_TYPE  QUERY  REFERENCE
    0* BAM_CMATCH      1      1
    1* BAM_CINS        1      0
    2* BAM_CDEL        0      1
    3* BAM_CREF_SKIP   0      1         #填N的区域
    4* BAM_CSOFT_CLIP  1      0
    5* BAM_CHARD_CLIP  0      0
    6* BAM_CPAD        0      0         #假设https://www.jianshu.com/p/ff6187c97155
    7* BAM_CEQUAL      1      1
    8* BAM_CDIFF       1      1
    9* BAM_CBACK       0      0
    '''
    stand = '-' if  read.is_reverse else '+' #  is negative 相对与参考基因组方向
    cigartuples = read.cigartuples
    for idx,var_len in cigartuples:
        # reads 长度统计 S5,H4,M0{7，8}，I1 
        # ref 统计 M0{7,8}, D2，N3,P6，
        read_idx_list = [0,1,4,5,7,8] # [M，I,S,H,=,X]
        ref_idx_list = [0,2,3,6,7,8] # [M,D,N,P,=,X]

        if idx == 0: # BAM_CMATCH
            read_pos_start = read_pos_end
            read_pos_end = read_pos_start + var_len # 左开右闭区间
            if ref_pos_end == 0:
                ref_pos_start = ref_pos_start
            else:
                ref_pos_start = ref_pos_end
            ref_pos_end = ref_pos_start + var_len # 左开右闭区间

        elif idx == 1: # BAM_CINS  # ref pos 相等
            read_pos_start = read_pos_end
            read_pos_end = read_pos_start + var_len
            ref_pos_start = ref_pos_end
            ref_pos_end = ref_pos_end # 左开右闭区间

        elif idx == 2: # BAM_CDEL # read pos 相等
            read_pos_start = read_pos_end
            read_pos_end = read_pos_end
            ref_pos_start = ref_pos_end
            ref_pos_end = ref_pos_start + var_len   # 左开右闭区间

        elif idx == 3: # BAM_CREF_SKIP  # 长度如果连续，则不是S/D[4/5],read ref pos 都累加
            read_pos_start = read_pos_end
            read_pos_end = read_pos_start + var_len
            ref_pos_start = ref_pos_end
            ref_pos_end = ref_pos_start + var_len   # 左开右闭区间

        elif idx == 4: # BAM_CSOFT_CLIP # ref pos 相等
            read_pos_start = read_pos_end
            read_pos_end = read_pos_start + var_len
            if ref_pos_end == 0:
                ref_pos_start = ref_pos_start
            else:
                ref_pos_start = ref_pos_end
            ref_pos_end = ref_pos_start  # 左开右闭区间

        elif idx == 7: # BAM_CEQUAL #
            read_pos_start = read_pos_end
            read_pos_end = read_pos_start + var_len
            if ref_pos_end == 0:
                ref_pos_start = ref_pos_start
            else:
                ref_pos_start = ref_pos_end
            ref_pos_end = ref_pos_start + var_len  # 左开右闭区间

        elif idx == 8: # BAM_CDIFF #
            read_pos_start = read_pos_end
            read_pos_end = read_pos_start + var_len
            if ref_pos_end == 0:
                ref_pos_start = ref_pos_start
            else:
                ref_pos_start = ref_pos_end
            ref_pos_end = ref_pos_start + var_len  # 左开右闭区间

        else: #5,BAM_CHARD_CLIP  6,BAM_CPAD  9,BAM_CBACK
            continue

        var_type = cigar_lst[idx]
        tmp_lst = [read_name,chrom,ref_pos_start,ref_pos_end,read_pos_start,read_pos_end,var_len,query_length,var_type,stand]
        #target_info_lst.append(tmp_lst)
        yield tmp_lst
    #return target_info_lst

def parse_cigar4count(read):
    '''
    # minimap2 -eqx
    # pbmm2

    samfile = pysam.AlignmentFile(bam_file, "rb")
    allreads=samfile.fetch(contig='chrX', start=1234567, stop=1234568)
    for read in allreads:
        reference_start = read.reference_start
        query_alignment_start = read.query_alignment_start
        query_alignment_end = read.query_alignment_end
        query_length = read.query_length
    '''
    cigar_str = read.cigarstring
    #print(cigarstring)
    ins_len_list = list(map(int,re.findall('(\d+)I', cigar_str)))
    #print(ins_len_list)
    del_len_list = list(map(int,re.findall('(\d+)D', cigar_str)))
    mis_len_list = list(map(int,re.findall('(\d+)X', cigar_str)))
    mat_len_list = list(map(int,re.findall('(\d+)=', cigar_str)))
    softclip_len_list = list(map(int,re.findall('(\d+)S', cigar_str)))
    ins_count=len(ins_len_list)
    del_count=len(del_len_list)
    mis_count=len(mis_len_list)
    mat_count=len(mat_len_list)
    softclip_count=len(softclip_len_list)
    return ins_count,del_count,mis_count,mat_count,softclip_count

def max_depth_region(bam,reference_name,chr_len):
    '''
    import pysam
    检测单个染色体中平均深度最大的区间，也可以修改为目标区域内深度最大的比对区域
    '''
    all_depth = []
    pos_flag=0
    start_pos=0
    ref_pos = 0 # 
    last_ref_pos = 0 #
    
    base_depth=0 # 全局变量
    temp_pos =[] # 存储平均深度最大所有坐标
    temp_cov =[] # 存储平均深度最大所有碱基深度

    region_mean_depth_max = 0
    temp_pos_max = []
    temp_cov_max = []
    samfile = pysam.AlignmentFile(bam, "rb" )
    #pileupcolumn,直接到有比对的位置,第一个位置就是有覆盖深度的地方
    #for pileupcolumn in samfile.pileup( reference_name, 0, chr_len,max_depth=8000,truncate=True,stepper="nofilter"):
    for pileupcolumn in samfile.pileup( reference_name, 0, chr_len):
        #reference_name = pileupcolumn.reference_name
        base_coverage = pileupcolumn.nsegments
        ref_pos = pileupcolumn.reference_pos
        all_depth.append([ref_pos,base_coverage])
        #print(ref_pos,base_coverage)
        #一次性 flag
        if pos_flag == 0:
            pos_flag = 1
            start_pos = ref_pos
            temp_pos.append(ref_pos)
            temp_cov.append(base_coverage)
            continue
        #获取上一个位置
        last_ref_pos = temp_pos[-1]
        if ref_pos - last_ref_pos > 2000: # 大于2k,则作为新的片段,但是实际中不应出现大于2k的del;完全连续贯穿
            region_len=last_ref_pos-start_pos+1
            base_depth=sum(temp_cov)
            region_mean_depth = float("{:.2f}".format(base_depth/region_len))
            if region_mean_depth > region_mean_depth_max:
                region_mean_depth_max = region_mean_depth
                temp_pos_max = temp_pos
                temp_cov_max = temp_cov
            
            start_pos = ref_pos # 新的起始坐标
            # 区域起始坐标,从起始开始计算
            # 清零从新记录,节省内存
            temp_pos = []
            temp_cov = []
            # 添加
            temp_pos.append(ref_pos)
            temp_cov.append(base_coverage)
            
        else:#正常连贯区域
            last_ref_pos = ref_pos
            temp_pos.append(ref_pos)
            temp_cov.append(base_coverage)

    # 最后一个区间,补充上最后一个终止
    if ref_pos == last_ref_pos:
        region_len = ref_pos-start_pos+1
        base_depth=sum(temp_cov)
        region_mean_depth = float("{:.2f}".format(base_depth/region_len))
        if region_mean_depth > region_mean_depth_max:
            region_mean_depth_max = region_mean_depth
            temp_pos_max = temp_pos
            temp_cov_max = temp_cov

    samfile.close()
    #由于两侧深度低,中间深度高, 取Q1-1.5iqr(Q3-Q1) 作为异常值边界
    if len(temp_cov_max) >1:
        lower_q,median,higher_q= calc_quantile(temp_cov_max)
        iqr = higher_q - lower_q
        t1 = lower_q - 1.5*iqr
        start_idx = 0
        for x in temp_cov_max:
            if x > t1:
                start_idx=temp_cov_max.index(x)
                break
        end_idx = -1
        for x in temp_cov_max[::-1]:
            if x > t1:
                end_idx=len(temp_cov_max) - temp_cov_max[::-1].index(x) 
                break
    else:
        return ["",0,0,0,0]
    #print(temp_cov_max[start_idx-1],temp_cov_max[end_idx-1])
    #print(temp_cov_max[start_idx],temp_cov_max[end_idx])
    #print(temp_cov_max[start_idx+1],temp_cov_max[end_idx+1])
    temp_pos_max = temp_pos_max[start_idx:end_idx+1]
    #print(start_idx,end_idx+1)
    #print(temp_pos_max)
    #start,end = temp_pos_max[0],temp_pos_max[-1]
    temp_cov_max = temp_cov_max[start_idx:end_idx+1]

    #上一个 50% 以下的排除
    if not  temp_cov_max:
        return ["",0,0,0,0]
    s_idx,e_idx = get_break_point_idx(temp_cov_max,0.5)
    temp_pos_max = temp_pos_max[s_idx:e_idx+1]
    start,end = temp_pos_max[0],temp_pos_max[-1]
    temp_cov_max = temp_cov_max[s_idx:e_idx+1]
    region_len = (end-start)
    region_mean_depth_max = float("{:.2f}".format(sum(temp_cov_max)/region_len))
    target_region = [reference_name,start,end,region_mean_depth_max,region_len]
    #return target_region,all_depth
    return target_region


def get_taget_region_mean_depth(bam,reference_name,start,end):
    '''
    coordinate: 0-base
    import pysam
    计算目标区域内的平均深度
    '''
    #all_depth = []
    temp_pos =[] # 存储平均深度最大所有坐标
    temp_cov =[] # 存储平均深度最大所有碱基深度
    samfile = pysam.AlignmentFile(bam, "rb" )
    #pileupcolumn,直接到有比对的位置,第一个位置就是有覆盖深度的地方
    #for pileupcolumn in samfile.pileup( reference_name, 0, chr_len,max_depth=8000,truncate=True,stepper="nofilter"):
    for pileupcolumn in samfile.pileup( reference_name, start,end+1):
        #reference_name = pileupcolumn.reference_name
        base_coverage = pileupcolumn.nsegments
        ref_pos = pileupcolumn.reference_pos
        #if ref_pos <start or ref_pos>end:
        #    continue
        if ref_pos >end:
            break
        if ref_pos <start:
            continue
        # 一个单碱基坐标，一个该位置的深度
        #all_depth.append([ref_pos,base_coverage])
        #print(ref_pos,base_coverage)
        temp_pos.append(ref_pos)
        temp_cov.append(base_coverage)
    region_len = end +1 - start 
    base_depth=sum(temp_cov)
    #print(region_len,base_depth)
    region_mean_depth = float("{:.2f}".format(base_depth/region_len))
    #print(region_mean_depth)
    samfile.close()
    return region_mean_depth

#
##
###################用于bam  方法  END#################




######################      obs         #####################


def ObsPathJoin(*args):
    '''
    param: [*str]
    #https://www.cnblogs.com/bincoding/p/7944860.html
    '''
    tmp_list=[]
    for x in args:
        tmp_list.append(x.strip('/'))
    obs_path = "/".join(tmp_list)
    return obs_path


def run_obs_ls_cmd(obsutil_bin, completed_obs_path):
    '''
        param:obs_path
        param:check_dir_list
        #https://www.cnblogs.com/lgj8/p/12132829.html
    '''
    cmd = " ".join([obsutil_bin ,'ls', completed_obs_path])
    ret = subprocess.run(args=cmd, encoding='utf8',
                             stdout=subprocess.PIPE, shell=True, check=True)
    return ret.stdout


def obs_ls_out_pase(standout):
    '''
    #读取 standout 内容按照行读取获得 key 与 LastModified Size 存储
    '''
    obs_files_dic = {}
    flag_table = False
    line_num = 0
    file_obs_path = ''
    for line in re.split('\n', standout):
        if line.startswith("key"):
            flag_table = True
            continue  # 跳过表头 #key LastModified Size StorageClass ETag
        if flag_table:
            line_num += 1
            if line_num % 3 == 1:
                file_obs_path = line.strip()
                #print("*", file_obs_path)
            elif line_num % 3 == 2:
                records = re.split("\s+", line.strip())
                modifiedTime = records[0]
                size_info = records[1]
                #print("#", "#"+modifiedTime+"#")
                #print("*", "#"+size_info+"#")
                obs_files_dic[file_obs_path] = [modifiedTime, size_info]
            else:
                continue
    return obs_files_dic

######################      obs         #####################




def get_args():
    parser = argparse.ArgumentParser(
        description=" step 2 ", usage="python3 %(prog)s [options]")
    parser.add_argument(
        "--input", help="input", metavar="FILE")
    parser.add_argument(
        "--ebv_fasta", help="ebv_fasta path:[default: %(default)s]", type=str,  default='NC_007605.1.fa', metavar="FILE")
    parser.add_argument(
        "--sample_lst", help="sample_list", metavar="FILE")
    parser.add_argument(
        '--offset', help='max offset,[default: %(default)s]', type=int, default=1, metavar="INT")
    parser.add_argument(
        '--clip_min_len', help='min softclip base length,[default: %(default)s]', type=int, default=10, metavar="INT")
    parser.add_argument(
        '--process_num', help='process_num,[default: %(default)s]', type=int, default=10, metavar="INT")
    parser.add_argument('--prefix', help='prefix', type=str,
                        required=True, metavar="PREFIX")
    parser.add_argument("--outdir", help="output directory", metavar="DIR")

    if len(sys.argv) <= 1:
        parser.print_help()
        sys.exit()
    else:
        args = parser.parse_args()

    return args

def main():
    
    bam_file='check.reads.sorted.bam'
    samfile = pysam.AlignmentFile(bam_file, "rb")
    # rb,wb
    out_bam = 'check.reads.tag.sorted.bam'
    result_bam = pysam.AlignmentFile(out_bam, "wb",template=samfile)
    # template=samfile 指定bam header 来源
    # https://pysam.readthedocs.io/en/latest/api.html?highlight=pysam.AlignmentFile#pysam.AlignmentFile
    allreads=samfile.fetch(contig='chrX', start=1234567, stop=1234567)
    all_lst=[]
    cigar_dic = {'M':0,'I':1,'D':2,'N':3,'S':4,'H':5,'P':6,'=':7,'X':8,'B':9}
    for read in allreads:
        reference_start = read.reference_start
        query_alignment_start = read.query_alignment_start
        query_alignment_end = read.query_alignment_end
        query_length = read.query_length

        cigar_idex = cigar_dic['M']
        min_len=0
        if read.mapping_quality >20 and not read.is_secondary:
                    read_name ,info_list= cigar_detect(read,cigar_idex,min_len)
                    if len(info_list)>0:
                        print([read_name]+info_list)
                    result_bam.write(read)
    
    # set_tag
    # https://pysam.readthedocs.io/en/latest/api.html?highlight=set_tag#pysam.AlignedSegment.set_tag
    # type
    # https://samtools.github.io/hts-specs/SAMtags.pdf
    # multiple_iterators=True
    # https://pysam.readthedocs.io/en/latest/api.html?highlight=multiple_iterators%3DTrue#pysam.AlignmentFile.fetch
    # AlignmentFile.fetch does not show unmapped reads
    # https://pysam.readthedocs.io/en/latest/faq.html?highlight=included%20in%20the%20iteration%20by%20adding%20the%20until_eof%3DTrue%20flag#alignmentfile-fetch-does-not-show-unmapped-reads

if __name__ == "__main__":
    if sys.version[0] == "3":
        start_time = time.perf_counter()
    else:
        start_time = time.clock()
    main()
    if sys.version[0] == "3":
        end_time = time.perf_counter()
    else:
        end_time = time.clock()
    print("%s %s %s\n" % ("main()", "use", str(
        datetime.timedelta(seconds=end_time - start_time))))
