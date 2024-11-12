from pysam import VariantFile
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

def convert2table(args):
    chrom,file =args
    # print(bcf_in.header)
    # bcf_out = VariantFile('-', 'w', header=bcf_in.header)
    # for rec in bcf_in.fetch('chr1', 100000, 200000):
    #     bcf_out.write(rec)
    bcf_in = VariantFile(file)  # auto-detect input format

    with gzip.open(chrom+".hg38.txt.gz",mode="wt",compresslevel=6) as out:
        header = "chrom\tstart\tstop\tref\talt\tallele_type\tAF\tAF_eas\tnhomalt\n"
        out.write(header)
        for rec in bcf_in.fetch():
            
            # print(rec.pos) # 使用vcf 本身的1-base
            # print(type(rec.alts)) # <class 'tuple'>
            for idx in range(len(rec.alts)):
                #print(rec.chrom, rec.pos, rec.start, rec.stop, rec.ref, rec.alts[idx], rec.info["allele_type"],rec.info["nhomalt"][idx])
                if "AF" not in rec.info:
                    # print(rec.chrom, rec.pos, rec.start, rec.stop, rec.ref, rec.alts[idx], rec.info["allele_type"],rec.info["nhomalt"][idx])
                    # AF = '-'
                    # 无记录的位点
                    continue
                else:
                    AF = rec.info["AF"]
                if "AF_eas" not in rec.info:
                    #print(rec.chrom, rec.pos, rec.start, rec.stop, rec.ref, rec.alts[idx], rec.info["allele_type"],rec.info["nhomalt"][idx])
                    AF_eas = '-'
                else:
                    AF_eas = rec.info["AF_eas"]
                # int(rec.start)+1 调整为1-base
                info_lst = list(map(str,[rec.chrom, int(rec.start)+1, rec.stop, rec.ref, rec.alts[idx], rec.info["allele_type"],AF[idx],AF_eas[idx],rec.info["nhomalt"][idx]]))
                info_str = "\t".join(info_lst)+"\n"
                out.write(info_str)
            #print(rec.chrom, rec.pos, rec.start, rec.stop, rec.ref, rec.alts, rec.info["allele_type"],rec.info["nhomalt"])
            # rec.alts # 元组
            # print(rec.start, rec.stop) # 使用0-base
            # print (rec.info)# object
            # print (rec.info.keys())
            # print(rec.info["nhomalt"]) #元组
    '''
    .chrom: 返回字符串
    .pos: 返回数值。 这个是以0为基, 可以用.start和.stop
    .id: 如果无记录, 就是NoneType
    .ref: 返回字符串
    .alt: 返回元祖(tuple), 因为一个位点上可以有多个变异类型
    .qual: 返回数值
    .filter: 返回pysam.libcbcf.VariantRecordFilter对象, 类似于字典
    .info: 返回pysam.libcbcf.VariantRecordInfo对象，类似于字典, 存放所有样本的统计信息
    .format: 返回pysam.libcbcf.VariantRecordFormat，类似于字典, 存放后续每个样本数据存放顺序和数据类型
    .samples: 返回pysam.libcbcf.VariantRecordSamples, 类似于字典, 存放每一个样本的具体信息
    '''

    # print(list((bcf_in.header.contigs))) # 染色体
    # # ['M', '17', '20']
    # print(list((bcf_in.header.filters)))
    # # ['PASS', 'q10', 's50']
    # print(list((bcf_in.header.info)))
    # # ['NS', 'DP', 'AF', 'AA', 'DB', 'H2']
    # print(list((bcf_in.header.samples)))
    # # ['NA00001', 'NA00002', 'NA00003']

    bcf_in.close()  # close file

def main():

    # script_path =Path(__file__)
    # script_dir = Path(script_path).parent
    # print(script_dir)
    current_dir = Path.cwd()
    files_lst = GetAllFilePaths(current_dir,wildcard="gnomad.genomes.v4.1.sites.*.vcf.bgz")
    arg_list = []
    for file in files_lst:
        file_name = file.name
        chrom = re.search(r'gnomad.genomes.v4.1.sites.(.*).vcf.bgz',file_name).group(1)
        arg_list.append((chrom,str(file)))

    # verison 3
    with multiprocessing.Pool(10) as pool:
        # prime 返回值
        primes = [n + 1 for 
                  n, prime in enumerate(pool.map(func=convert2table,iterable=arg_list)) # 函数，可迭代每个参数的迭代
                  if prime]

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
    
