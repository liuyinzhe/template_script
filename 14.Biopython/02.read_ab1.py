import sys 
from Bio import SeqIO
from pathlib import Path
import numpy as np
import argparse
import shutil



def abi_to_dict(record):
    abi_data = {"conf":[],
                "channel":{"A":[],
                           "T":[],
                           "G":[],
                           "C":[],
                          },
                "_channel":{"A":[],
                            "T":[],
                            "G":[],
                            "C":[],
                          }
                }
    '''
    record.annotations['abif_raw']["PLOC1"] 所有顺序 list   [1,2,3,4]
    record.annotations['abif_raw']["PCON1"] 所有质量值 list [1,2,3,4]
    abi_data["channel"]["G"]                碱基信号强度   A [5,6,7,7]

    # https://bioinformatics.stackexchange.com/questions/19300/extracting-base-sequences-from-abi-ab1-sanger-sequencing-chromatogram
    You can access the peak positions of Sanger Sequencing chromatograms from ["PLOC1"].
    The position values in ["PLOC1"] correspond to the index values in ["DATA9"], ["DATA10"], ["DATA11"], ["DATA12"],
    so you can extract the signal values of each base at the positions.

    '''
    for i, (pos, conf) in enumerate(zip(record.annotations['abif_raw']["PLOC1"], record.annotations['abif_raw']["PCON1"])):
        if pos > 4 and pos < len(record.annotations['abif_raw']["DATA9"])-5: 
            abi_data["conf"].append(conf)
            abi_data["channel"]["G"].append(record.annotations['abif_raw']["DATA9"][pos])
            abi_data["channel"]["A"].append(record.annotations['abif_raw']["DATA10"][pos])
            abi_data["channel"]["T"].append(record.annotations['abif_raw']["DATA11"][pos])
            abi_data["channel"]["C"].append(record.annotations['abif_raw']["DATA12"][pos])

    return abi_data 


def generate_consensusseq(abidata):
    '''
    _atgc_dict = {0:"A", 1:"T", 2:"G", 3:"C"}
    index   0   1   2   3
    signal  A   T   G   C

    '''
    _atgc_dict = {0:"A", 1:"T", 2:"G", 3:"C"}
    consensus_seq = "" 
    
    for values in zip(abidata["channel"]["A"], abidata["channel"]["T"], abidata["channel"]["G"], abidata["channel"]["C"]):
        consensus_seq += _atgc_dict[values.index(max(values))]
    
    positive_strand_seq = consensus_seq
    negative_strand_seq = consensus_seq.translate(str.maketrans("ATGC","TACG"))[::-1]
    return positive_strand_seq,negative_strand_seq

def count_GC(sequence):
    seq_len = len(sequence)
    G_count = sequence.count("G")
    C_count = sequence.count("C")
    GC_count = G_count + C_count
    GC_ratio = GC_count / seq_len
    return GC_ratio


def Get_Max_noise_signal(numlist):
    '''
    获取 信号中 次大信号值，且信号值 与最大之间 次峰占比低于不能超过最高的40%
    # 重合 杂合新型号
    # 40% 以上的杂合信号
    '''
    numlist_sorted = sorted(numlist,reverse=True)
    list_len = len(numlist_sorted)
    Max_signal = numlist_sorted[0]
    Max_noise_signal = 0
    for idx in range(1,list_len):
        #print(idx)
        value = numlist_sorted[idx]
        if Max_signal == 0:
            singal_percent = 0.0
            #print(value,Max_signal)
        else:
            singal_percent = float(value/Max_signal)
        if singal_percent < 0.4:#0.4:
            Max_noise_signal = value
            break
        else:
            continue
    # 没有其它信号，用最小的
    if Max_noise_signal == 0:
        Max_noise_signal = numlist_sorted[-1]
    return Max_noise_signal



def generate_secondMax_signal(abidata):
    '''
    _atgc_dict = {0:"A", 1:"T", 2:"G", 3:"C"}
    index   0   1   2   3
    signal  A   T   G   C

    '''
    secondMax_signal_list= []
    #secondMax_percent_list = []
    double_peak_lst = []
    for values in zip(abidata["channel"]["A"], abidata["channel"]["T"], abidata["channel"]["G"], abidata["channel"]["C"]):
        secondMax_signal_list.append(Get_Max_noise_signal(values))
        #secondMax_percent_list.append(Get_Max_noise_percent(values))
        # ATGC 信号峰值
        value_sorted = sorted(values,reverse=True)
        if value_sorted[1] ==0:
            double_peak_lst.append(0)
        elif value_sorted[1]/value_sorted[0] >0.4:
            double_peak_lst.append(1)
        else:
            double_peak_lst.append(0)
    return secondMax_signal_list,double_peak_lst #,secondMax_percent_list

def main()->None:
    # 获取当前目录
    current_dir = Path.cwd()

    file_path = Path.joinpath(current_dir,'Y01DD-004.41.Reversed.ab1')
    # biopython 读取文件
    record   = SeqIO.read(file_path,'abi')
    # 转为字典
    abidata = abi_to_dict(record)
    print(list(abidata['channel'].keys()))
    '''
    # 字典内容
    abi_data = {"channel":{"G":[0,10,4,5,20],
                            "A":[23,3,1,3,4],
                            "T":[3,1,30,4,1],
                            "C":[1,1,3,34,1]
                            }
                }
    # 按照list 顺序可 对应碱基构成 
    abi_data["channel"]["G"]  [0,10,4,5,20]
    abi_data["channel"]["A"]  [23,3,1,3,4]
    abi_data["channel"]["T"]  [3,1,30,4,1]
    abi_data["channel"]["C"]  [1,1,3,34,1]
                      碱基构成  A G T  C G
    '''
    # 正向与反向互补的序列，通过信号最强的碱基确认的一致性序列（consensus seq）
    positive_strand_seq,negative_strand_seq = generate_consensusseq(abidata)
    # 计算序列的GC含量,虽然意义不大
    GC_ratio = count_GC(positive_strand_seq)
    # 定义噪音杂峰的定义是 低于最高峰信号40%峰高的峰中峰值最高的峰
    # 获得噪音峰的信号强度列表，以及非噪音的双峰位置列表（0,1表示双峰在某个位置是否存在）
    # secondMax_signal_list 用于计算 噪音信号的 均值；double_peak_lst，用于判断 InDel 变异区域
    secondMax_signal_list,double_peak_lst = generate_secondMax_signal(abidata)
if __name__ == '__main__':
    main()
