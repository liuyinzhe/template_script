from pysam import VariantFile
import re
import gzip

myvcf = 'gnomad.genomes.v4.1.sites.chrY.vcf.bgz'  # vcf.gz
bcf_in = VariantFile(myvcf)  # auto-detect input format

# print(bcf_in.header)
# bcf_out = VariantFile('-', 'w', header=bcf_in.header)
# for rec in bcf_in.fetch('chr1', 100000, 200000):
#     bcf_out.write(rec)

with gzip.open("out.txt.gz",mode="wt",compresslevel=6) as out:
    header = "chrom\tstart\tstop\tref\talt\tallele_type\tAF\tAF_eas\tnhomalt\n"
    out.write(header)
    for rec in bcf_in.fetch():
        # print(rec.pos) # 使用vcf 本身的1-base
        for idx in range(len(rec.alts)):
            #print(rec.chrom, rec.pos, rec.start, rec.stop, rec.ref, rec.alts[idx], rec.info["allele_type"],rec.info["nhomalt"][idx])
            AF= rec.info["AF"]
            AF_eas = rec.info["AF_eas"]
            # int(rec.start)+1 调整为1-base
            info_lst = list(map(str,[rec.chrom, int(rec.start)+1, rec.stop, rec.ref, rec.alts[idx], rec.info["allele_type"],AF,AF_eas,rec.info["nhomalt"][idx]]))
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
