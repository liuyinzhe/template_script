import pysam
import time
import datetime
import logging
import sys
from pathlib import Path
import re
import pickle
from Bio import SeqIO
import pandas as pd

from tqdm import tqdm

def read_fasta(fasta_path):
    # 读取 FASTA 文件并存储到字典
    fasta_dict = {
        record.id: str(record.seq)  # 将 Seq 对象转为字符串
        for record in SeqIO.parse(fasta_path, "fasta")
    }
    return fasta_dict

def stat_base(bam_path,reference_seq,ref_name,start,end,pos_str_lst):
    samfile = pysam.AlignmentFile(bam_path, mode="rb", threads=6)
    position_dic = {}
    for pileupcolumn in samfile.pileup(contig=ref_name,start=start,end=end,max_depth=80000,stepper="all",ignore_overlaps=True):#flag_filter=1796,
        chrom = pileupcolumn.reference_name
        position = pileupcolumn.pos #pileupcolumn.reference_pos
        if str(position) not in pos_str_lst:
            continue
        depth = pileupcolumn.n #pileupcolumn.nsegments
        reference_base = reference_seq[position]
        if position not in position_dic:
            position_dic[position] = {'A':0,
                                      'T':0,
                                      'G':0,
                                      'C':0,
                                      'ref':reference_base, # 碱基
                                      #'depth':depth,# 深度
                                      }
        # 更新位置碱基
        for pileupread in pileupcolumn.pileups:
            if not pileupread.is_del and not pileupread.is_refskip:
                # query position is None if is_del or is_refskip is set.
                position_base = pileupread.alignment.query_sequence[pileupread.query_position]
                position_dic[position][position_base] += 1
        # read 遍历完毕
    samfile.close()
    return position_dic

def main():
    current_dir = Path().cwd()
    fasta_path = Path("/data/project/personalization/ref/ref.fasta")#current_dir.joinpath("ref.fasta")
    ref_seq_dic = read_fasta(fasta_path) # 参考序列
    bam_path = current_dir.joinpath("fragment.sorted.bam")
    # 获取染色体坐标
    pos_lst = [
        # [0,25],#25
        [25,37],#12
        # [37,59],#
        [59,71],#12
        # [71,96],#25
        ] #0-base
        #rigth_twelve_end
        #[49,61]
    position_lst = [] # 存储不同染色体的碱基比对信息
    for ref_name,seq in tqdm(ref_seq_dic.items()):
        part_str = re.sub("XXXXX/","",ref_name)
        part_str = re.sub("/YYYY","",part_str)
        # c/a/b/d
        parts = re.split(r"/",part_str)
        # 
        offset = 400 # tmp
        fragment_dic = {} # 存储每个片段的比对信息
        for idx in range(len(parts)):
            twelve_dic = {}
            part_name = parts[idx]
            if part_name != "PT":
                left_twelve_start = 25+offset
                left_twelve_end = 37+offset

                rigth_twelve_start = 59+offset
                rigth_twelve_end = 71+offset
            else:
                left_twelve_start =25+offset
                left_twelve_end =37+offset

                rigth_twelve_start =49+offset
                rigth_twelve_end = 61+offset
            reference_seq = ref_seq_dic[ref_name]
            # 获取位置信息字典
            pos_str_lst = [str(x) for x in range(left_twelve_start,left_twelve_end)]
            pos_str_lst = pos_str_lst + [str(x) for x in range(rigth_twelve_start,rigth_twelve_end)]
            twelve_dic = stat_base(bam_path,reference_seq,ref_name,left_twelve_start,rigth_twelve_end,pos_str_lst)
            #print(ref_name,part_name)
            # 存储信息
            fragment_dic[part_name] = twelve_dic
            #
            #累加偏移坐标,用于下一个片段
            offset+=71
        #
        position_lst.append([ref_name,fragment_dic])
        #
    # 计算信息

    # 序列化
    pickle.dump(position_lst, open("data.pkl", 'wb'))
    
    # # 反序列化
    # position_lst = pickle.load(open("data.pkl", 'rb'))

    data_dic = {}
    for ref_name, fragment_dic in position_lst:
        if ref_name not in data_dic:
            data_dic[ref_name] = {
                'part_name':[],
                'position':[],
                'ref_base':[],
                'alt_base':[],
                'depth':[],
                'alt_percent':[],
                'A_count':[],
                'T_count':[],
                'G_count':[],
                'C_count':[],
                'fail_flag':[]
            }
        part_str = re.sub("XXXXX/","",ref_name)
        part_str = re.sub("/YYYY","",part_str)
        # c/a/b/d
        parts = re.split(r"/",part_str)
        for part_name in parts:
            twelve_dic = fragment_dic[part_name]
            for position,dic in sorted(twelve_dic.items(), key=lambda item:item[0]):
                A_count = dic['A']
                T_count = dic['T']
                G_count = dic['G']
                C_count = dic['C']
                max_type = ["",0] # name,count
                for key in ['A','T','G','C']:
                    if dic[key] > max_type[1]:
                        max_type = [key,dic[key]]
                alt_base_type = max_type[0]
                alt_count = max_type[1]
                reference_base = dic['ref'].upper()
                depth = sum([A_count,T_count,G_count,C_count])
                if depth == 0:
                    alt_percent="0%"
                    data_dic[ref_name]['fail_flag'].append(True)
                else:
                    alt_percent = "{:.2f}%".format((alt_count/depth)*100)
                    data_dic[ref_name]['fail_flag'].append(False)
                # 存储
                data_dic[ref_name]['part_name'].append(part_name)
                data_dic[ref_name]['ref_base'].append(reference_base)
                data_dic[ref_name]['alt_base'].append(alt_base_type)
                data_dic[ref_name]['depth'].append(depth)
                
                data_dic[ref_name]['position'].append(position)
                data_dic[ref_name]['alt_percent'].append(alt_percent)
                data_dic[ref_name]['A_count'].append(A_count)
                data_dic[ref_name]['T_count'].append(T_count)
                data_dic[ref_name]['G_count'].append(G_count)
                data_dic[ref_name]['C_count'].append(C_count)

    # 输出数据框
    with pd.ExcelWriter( 'result_success.xlsx', engine='openpyxl',mode='w') as s_writer,\
        pd.ExcelWriter( 'result_fail.xlsx', engine='openpyxl',mode='w') as f_writer:
        for  ref_name,dic in  data_dic.items():
            df = pd.DataFrame(dic)
            part_str = re.sub("XXXXX/","",ref_name)
            part_str = re.sub("/YYYY","",part_str)
            ref = re.sub(r"/","_",ref)
            if True in  df['fail_flag'].to_list():
                df.drop("fail_flag",axis=1,inplace=True)
                df.to_excel(f_writer, sheet_name=ref, index=False)
            else:
                df.drop("fail_flag",axis=1,inplace=True)
                if max(df['depth'].to_list())<5:
                    df.to_excel(f_writer, sheet_name=ref, index=False)
                df.to_excel(s_writer, sheet_name=ref, index=False)
'''
data = {
        'part_name':[],
        'position':[],
        'ref_base':[],
        'alt_base':[],
        'depth':[],
        'alt_percent':[],
        'A_count':[],
        'T_count':[],
        'G_count':[],
        'C_count':[],
        'fail_flag':[]
}

(1) 读取坐标信息
(2) 遍历获取碱基信息
(3) 解析bam指定位置的碱基构成比例 A(%) T(%) G(%) C(%)
(4) 整理多个文件的dataframe 输出多个excel shell 结果

'''
if __name__ == "__main__":
    if sys.version[0]=="3":
        start_time = time.perf_counter()
    else:
        start_time = time.clock()
    main()
    if sys.version[0]=="3":
        end_time = time.perf_counter()
    else:
        end_time = time.clock()
    logging.info("%s %s %s\n"%("main()", "use", str(datetime.timedelta(seconds = end_time - start_time))))

