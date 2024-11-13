import pandas as pd
import gzip
import re
import sys
import time
from datetime import timedelta
from pathlib import Path


import multiprocessing

def GetAllFilePaths(pwd,wildcard='*'):
    '''
    获取目录下文件全路径，通配符检索特定文件名，返回列表
    param: str  "pwd"
    return:dirname pathlab_obj
    return:list [ str ]
    #https://zhuanlan.zhihu.com/p/36711862
    #https://www.cnblogs.com/sigai/p/8074329.html
    '''
    files_lst = []
    target_path=Path(pwd)
    for child in target_path.rglob(wildcard):
        if child.is_symlink():
            pass
        elif child.is_dir():
            pass
        elif child.is_file():
            files_lst.append(child)
    return files_lst

def read_gzip(args):
    target_file,chrom,last_pos,var_type,key_str_list = args
    var_dic={}
    var_dic[chrom] ={}
    count = 0
    with gzip.open(target_file,mode="rt") as fh:
        for line in fh:
            '''
            chrom   start   stop    ref     alt     allele_type     AF      AF_eas  nhomalt
            '''
            record = re.split("\t",line.strip())
            chrom,start,stop,ref,alt,allele_type,af,af_eas,nhomalt = record
            if allele_type != var_type:
                continue
            # 起始坐标大于start则停止读取
            if last_pos <int(start):
                #print(last_pos,"<",start)
                break
            key_str='_'.join([chrom,start,stop,ref,alt])
            
            #存入
            if  key_str in key_str_list:
                #print(af,af_eas,nhomalt)
                var_dic[chrom][key_str]=[af,af_eas,nhomalt]
            count +=1
            if count%1000000 ==0:
                print(chrom,"reading",count)
    return var_dic

def main():
    # script_path =Path(__file__)
    # script_dir = Path(script_path).parent
    # print(script_dir)
    current_dir = Path.cwd()
    files_lst = GetAllFilePaths(current_dir,wildcard="*.snp.xls")
    var_type = 'snv'
    #file_df_lst = []
    var_dic = {} # chrom:{chrom_start_end_ref_alt:[AF,AF_eas,nhomalt]}
    last_chrom_pos_dic = {} #最后一个位点信息
    for file in files_lst:
        file_name = file.name
        dataframe_df = pd.read_csv(file,encoding="utf-8",sep='\t',index_col=None,dtype=str)
        #file_df_lst.append(dataframe_df)
        for index, row in dataframe_df.iterrows():
            '''
            Chr	Start	End	Ref	Alt  gnomAD_genome_ALL	gnomAD_genome_EAS # Number_of_homozygotes
            '''
            chrom = row['Chr']
            start = row['Start']
            end = row['End']
            ref = row['Ref']
            alt = row['Alt']
            # chrM 染色体没有注释
            if chrom =="chrM":
                continue
            key_str='_'.join([chrom,start,end,ref,alt])
            if chrom not in var_dic:
                var_dic[chrom] = {}
            elif key_str not in var_dic[chrom]:
                var_dic[chrom][key_str] = []
            # 更新存储最后一个start 1-base
            last_chrom_pos_dic[chrom] = start 
    # 需要读取的染色体
    chrom_list = list(var_dic.keys())
    print(chrom_list)

    # 第2部分

    #生成 args_list = [[target_file,chrom,last_pos,var_type,key_str_list],]
    #
    args_list = []
    database_path = Path("/data/database/gnomAD/Genomes_table")
    for chrom in chrom_list:
        target_file = database_path.joinpath(chrom+".hg38.txt.gz")
        last_pos = int(last_chrom_pos_dic[chrom])
        key_str_list = list(var_dic[chrom].keys())
        args_list.append([target_file,chrom,last_pos,var_type,key_str_list])
    
    # # verison 3
    processes = 10
    with multiprocessing.Pool(processes) as pool:
        # 返回值
        return_dic_lst = [dic for n, dic in enumerate(pool.map(func=read_gzip,iterable=args_list)) # 函数，可迭代每个参数的迭代
                  if len(dic) > 0]
    #
    for tmp_dic in return_dic_lst:
        var_dic.update(tmp_dic)

    # 第3部分  修改
    # 创建输出目录
    output_path = current_dir.joinpath("output")
    output_path.mkdir(parents=True,exist_ok=True)

    for file in files_lst:
        file_name = file.name
        out_file = output_path.joinpath(file_name)

        dataframe_df = pd.read_csv(file,encoding="utf-8",sep='\t',index_col=None,dtype=str)
        # 创建新的列来存储解析后的分类信息
        new_columns = ['Number_of_homozygotes',]
        for col in new_columns:
            dataframe_df[col] = ""
        
        #
        for index, row in dataframe_df.iterrows():
            chrom = row['Chr']
            start = row['Start']
            end = row['End']
            ref = row['Ref']
            alt = row['Alt']
            key_str='_'.join([chrom,start,end,ref,alt])
            # chrM 染色体没有注释
            if chrom =="chrM":
                continue
            if key_str in var_dic[chrom]:
                af,af_eas,nhomalt = var_dic[chrom][key_str]
                dataframe_df.at[index, 'gnomAD_genome_ALL'] = af
                dataframe_df.at[index, 'gnomAD_genome_EAS'] = af_eas
                dataframe_df.at[index, 'Number_of_homozygotes'] = nhomalt
        # 保存文件
        dataframe_df.to_csv(out_file,sep='\t',index=False,encoding="utf-8")


if __name__ == '__main__':
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
        timedelta(seconds=end_time - start_time))))
