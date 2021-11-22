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





###################小工具     BEGIN#################
##
#

def reverse_complement(seq):
    '''get reverse complement  seq'''
    rule = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G', 'N': 'N'}
    return ''.join([rule[each] for each in seq.upper()][::-1])


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
    解析为列表
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
            ref_pos_end = ref_pos_end  # 左开右闭区间

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
        target_info_lst.append(tmp_lst)
    return target_info_lst

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
