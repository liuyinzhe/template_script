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
