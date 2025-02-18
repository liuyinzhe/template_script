#!/usr/bin/env python3

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

'''
target: 提取目标基因组上目标基因的变异信息# 
# 要求：read 对的变异 还原到基因序列上，查看所有变异形式对蛋白的影响(仅限read pair,混测)
# 
'''

from Bio.Seq import Seq
from Bio.Data import CodonTable

# 输出密码表
#standard_table = CodonTable.unambiguous_dna_by_id[1]
#mito_table = CodonTable.unambiguous_dna_by_id[2]
#print(standard_table)

def dna2port(seq,transl_table=1,cds_check=True):
    '''
    parm: seq ,can be messenger_rna or DNA_seq
    parm: transl_table 1-33
    1. The Standard Code
    2. The Vertebrate Mitochondrial Code
    3. The Yeast Mitochondrial Code
    4. The Mold, Protozoan, and Coelenterate Mitochondrial Code and the Mycoplasma/Spiroplasma Code
    5. The Invertebrate Mitochondrial Code
    6. The Ciliate, Dasycladacean and Hexamita Nuclear Code
    9. The Echinoderm and Flatworm Mitochondrial Code
    10. The Euplotid Nuclear Code
    11. The Bacterial, Archaeal and Plant Plastid Code
    12. The Alternative Yeast Nuclear Code
    13. The Ascidian Mitochondrial Code
    14. The Alternative Flatworm Mitochondrial Code
    16. Chlorophycean Mitochondrial Code
    21. Trematode Mitochondrial Code
    22. Scenedesmus obliquus Mitochondrial Code
    23. Thraustochytrium Mitochondrial Code
    24. Rhabdopleuridae Mitochondrial Code
    25. Candidate Division SR1 and Gracilibacteria Code
    26. Pachysolen tannophilus Nuclear Code
    27. Karyorelict Nuclear Code
    28. Condylostoma Nuclear Code
    29. Mesodinium Nuclear Code
    30. Peritrich Nuclear Code
    31. Blastocrithidia Nuclear Code
    33. Cephalodiscidae Mitochondrial UAA-Tyr Code
    https://www.ncbi.nlm.nih.gov/Taxonomy/Utils/wprintgc.cgi

    '''
    gene = Seq(seq)
    prot_seq = gene.translate(table=transl_table,cds=cds_check)
    #,to_stop=True 与 cds 冲突，遇到提前终止就停止翻译
    return prot_seq

def cigar2tab_r(read):
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
    query_length = read.query_length
    read_pos_start = read.query_alignment_start - query_length # 0-base
    read_pos_end = read.query_alignment_end - query_length # 0-base

    #print(read_name,chrom,ref_pos_start,ref_pos_end,read_pos_start,read_pos_end,query_length)
    stand = '-' if  read.is_reverse else '+' #  is negative 相对与参考基因组方向
    #stand = '+'
    if read.is_read1  and read.is_paired :
        read_pair = 'r1' 
    elif read.is_read2 and read.is_paired :
        read_pair = 'r2'
    else:
        read_pair = 's' 
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
        tmp_lst = [read_name,chrom,ref_pos_start,ref_pos_end,read_pos_start,read_pos_end,var_len,query_length,var_type,stand,read_pair]
        #target_info_lst.append(tmp_lst)
        yield tmp_lst
    #return target_info_lst
    

def format_str(input_str,width):
    '''
    '''
    out_str = ''
    for idx in range(0,len(input_str),width):
        if idx ==0 :
            out_str=input_str[idx:idx+width]
        else:
            out_str += '\n'+input_str[idx:idx+width]
    return out_str


def position_convert(start,end,inherent_start=968,inherent_end=2480):
    '''
    123=1X26= 提取侧翼比对，中间变异的
    输入坐标 为 ref 坐标 ,输入坐标可以控制修改，变异起始前1bp,到最后一个变异末尾后1bp
    # 目的提取变异区域，进行拆分后置换
    0-base
    inherent_end = inherent_end +1 # 主要为了index 索引 提取序列
    返回的坐标用于python list 提取序列的 index

    # 150 bp 不会完全覆盖目标区域
    # 获得的reads 坐标 覆盖的话，截取开头
    '''
    # 包含在内
    if start >= inherent_start and end<=inherent_end:
        new_start = start - inherent_start
        new_end =  new_start + (end - start)
        return new_start,new_end
    elif start < inherent_start:
        # 左侧多出来
        start = inherent_start
        # 正常处理
        new_start = start - inherent_start
        new_end =  new_start + (end - start)
        return new_start,new_end
    elif end > inherent_end:
        # 右侧多出来
        end = inherent_end
        # 正常处理
        new_start = start - inherent_start
        new_end =  new_start + (end - start)
        return new_start,new_end
    else:
        return False



def main():
    ref_seq=""
    with open('D5_ref.fa',mode='rt',encoding='utf-8') as fh:
        for line in fh:
            if line.startswith('>'):
                continue
            else:
                ref_seq += line.strip()


    target_gene_seq = ref_seq[968:2480]
    print(len(target_gene_seq))
    
    # print(target_gene_seq[0:20])
    # print(target_gene_seq[len(target_gene_seq)-20:-1])
    # 固定区域读取：
    var_info = open('var_info.xls',mode='wt',encoding='utf-8')
    var_info.write("read_name\tchrom\tref_pos_start\tref_pos_end\tgene\tg_start\tg_end\tread_pos_start\tread_pos_end\tquery_length\tvar_len\tvar_type\tstand\tread_pair\n")
    bam_file='RS23IMYJH16_D5_n.sorted.bam'
    samfile = pysam.AlignmentFile(bam_file, "rb",threads=2)
    allreads=samfile.fetch(contig='D5', start=968, stop=2480)
    read_dic={} # read_name: target_seq #
    cigar_dic={}
    for read in allreads:
        read_name = read.query_name
        reference_start = read.reference_start
        reference_end = read.reference_end
        query_length = read.query_length
        query_seq = read.query_sequence # 与参考基因组方向一致

        #if read.mapping_quality >20 and not read.is_secondary:
        # read.is_reverse
        # 没存过 则是目标序列
        #if read_name != "A00358:870:HG3H5DSX5:3:1149:23357:27821":
        #    continue

        cigar_str = str(read.cigarstring)
        start_mobj = re.search("^(\d+?)=\d+?[MIDNSHPXB]",cigar_str)
        end_mobj = re.search("[MIDNSHPXB](\d+?)=$",cigar_str)
        if start_mobj and end_mobj :

            if read_name not in read_dic:
                read_dic[read_name] = target_gene_seq
            '''
            判断，两侧为^\d+=  \d+{}$
            '''
            gene_seq = read_dic[read_name]
            start_len = int(start_mobj.group(1))
            end_len = int(end_mobj.group(1))
            start = reference_start + start_len
            end = reference_end - end_len
            # read.is_reverse
            # 变异发生在这个区域以外,并且变异长度 30bp 不在 # 必须保留30bp 变异区域在 目标区域
            if  reference_start + start_len -30 < 968 or reference_start + start_len +30 > 2480 :
                continue
            # 记录 cigar
            if read_name not in cigar_dic:
                cigar_dic[read_name] = cigar_str
            else:
                cigar_dic[read_name] += ","+cigar_str

            n_start,n_end = position_convert(start,end)
            # 拆分 两部分
            part_1_gene_seq = gene_seq[0:n_start]
            part_3_gene_seq = gene_seq[n_end:]
            # 获得 ref 坐标 对应的 reads 坐标用于提取序列
            insert_seq = query_seq[start_len:query_length-end_len] 
            read_dic[read_name] = part_1_gene_seq+insert_seq+part_3_gene_seq
            #target_gene_seq[n_start:n_end]
            for set_array in cigar2tab_r(read):
                read_name,chrom,ref_pos_start,ref_pos_end,read_pos_start,read_pos_end,var_len,query_length,var_type,stand,read_pair = set_array
                #if var_type != "=":
                #    var_info.write("\t".join([read_name,chrom,str(ref_pos_start),str(ref_pos_end),str(read_pos_start),str(read_pos_end),str(var_len),var_type,stand,read_pair])+'\n')
                if var_type != "=":
                    var_info.write("\t".join([read_name,chrom,str(ref_pos_start+1),str(ref_pos_end),'gene',str(ref_pos_start-968+1),str(ref_pos_end-968),str(read_pos_start+1),str(read_pos_end),str(query_length),str(var_len),var_type,stand,read_pair])+'\n')
                else:
                    var_info.write("\t".join([read_name,chrom,str(ref_pos_start+1),str(ref_pos_end),'gene','-','-',str(read_pos_start+1),str(read_pos_end),str(query_length),str(var_len),var_type,stand,read_pair])+'\n')
        elif cigar_str == "150=":
            read_dic[read_name] = ref_seq[968:2480]
            # 记录 cigar
            if read_name not in cigar_dic:
                cigar_dic[read_name] = cigar_str
            else:
                cigar_dic[read_name] += ","+cigar_str

            for set_array in cigar2tab_r(read):
                read_name,chrom,ref_pos_start,ref_pos_end,read_pos_start,read_pos_end,var_len,query_length,var_type,stand,read_pair = set_array
                #if var_type != "=":
                #    var_info.write("\t".join([read_name,chrom,str(ref_pos_start),str(ref_pos_end),str(read_pos_start),str(read_pos_end),str(var_len),var_type,stand,read_pair])+'\n')
                if var_type != "=":
                    var_info.write("\t".join([read_name,chrom,str(ref_pos_start+1),str(ref_pos_end),'gene',str(ref_pos_start-968+1),str(ref_pos_end-968),str(read_pos_start+1),str(read_pos_end),str(query_length),str(var_len),var_type,stand,read_pair])+'\n')
                else:
                    var_info.write("\t".join([read_name,chrom,str(ref_pos_start+1),str(ref_pos_end),'gene','-','-',str(read_pos_start+1),str(read_pos_end),str(query_length),str(var_len),var_type,stand,read_pair])+'\n')
        else:
            continue
    var_info.close()
    # 输出dna 与蛋白序列

    with open('nucl.fasta',mode='wt',encoding='utf-8') as nucl, open('prot.fasta',mode='wt',encoding='utf-8') as prot:
        for read_name in read_dic:
            nucl_seq = read_dic[read_name]
            nucl_len = len(nucl_seq)
            #supp_seq = ref_seq[2480:2580] # 100bp
            remainder = nucl_len%3
            if remainder != 0:
                #print(read_name,nucl_len)
                supp_len = 3 - remainder
                nucl_seq += ref_seq[2480:2480+supp_len]
                nucl_len = len(nucl_seq)
                if nucl_len %3 != 0:
                    print(read_name,nucl_len)
            prot_seq = str(dna2port(nucl_seq,transl_table=1,cds_check=False))
            prot_len = len(prot_seq)
            nucl.write(">"+read_name+" "+str(nucl_len)+"\n")
            prot.write(">"+read_name+" "+str(prot_len)+"\n")
            nucl.write(format_str(nucl_seq,60)+'\n')
            prot.write(format_str(prot_seq,60)+'\n')
    with open('cigar.info.xls',mode='wt',encoding='utf-8') as out:
        out.write('read_name\tcigar_str\n')
        for read_name in cigar_dic:
            cigar_str = cigar_dic[read_name]
            out.write('\t'.join([read_name,cigar_str])+'\n')


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
