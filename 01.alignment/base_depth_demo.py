import pysam
import  re
from collections import OrderedDict
position_dic = OrderedDict() #[Ref_base, position]
with open('input_pos.tsv',mode='rt',encoding='utf-8') as fh:
    '''Ref	623	G	A'''
    for line in fh:
        record = re.split('\t',line.strip())
        ref_chrom, position, ref_base, alt_base = record
        position_dic[position]=[ref_chrom, int(position), ref_base, alt_base]

result_lst = [] # chrom position ref_base alt_base percent depth
samfile = pysam.AlignmentFile("sample.sorted2.bam", "rb", threads=2)
# 保证pileupcolumn.nsegments 与reads 统计深度一致
# pysam pileup function seems to give wrong pileup number
#https://github.com/pysam-developers/pysam/issues/988
for pileupcolumn in samfile.pileup(ignore_overlaps=False): # "Ref", 623, 625
    chrom = pileupcolumn.reference_name
    position = pileupcolumn.pos #pileupcolumn.reference_pos
    depth = pileupcolumn.n #pileupcolumn.nsegments
    #print(depth,pileupcolumn.nsegments)
    #print(dir(pileupcolumn))
    if str(position) in position_dic:
        ref_chrom, ref_pos, ref_base, alt_base = position_dic[str(position)]
        tmp_base_dic = {'A':0, 'C':0, 'G':0, 'T':0}
        for pileupread in pileupcolumn.pileups:
            if not pileupread.is_del and not pileupread.is_refskip:
                # query position is None if is_del or is_refskip is set.
                # read_name = pileupread.alignment.query_name,
                position_base = pileupread.alignment.query_sequence[pileupread.query_position]
                tmp_base_dic[position_base] += 1
        result_lst.append([chrom, str(position), ref_base, alt_base, "{:.2f}%".format((tmp_base_dic[alt_base]/depth)*100), str(depth)])
        # max_base_type = max(tmp_base_dic, key=tmp_base_dic.get)
        # max_base_count = tmp_base_dic[max_base_type]
        # print(tmp_base_dic,position,"REF:",ref_base,"最多碱基:",max_base_type,"最多数量:",max_base_count,"深度:",depth,"预期的alt_base:",alt_base)
        #print(ref_base, max_base_type)
    else:
        continue

samfile.close()

header_str = '\t'.join(['chrom','position','ref_base','alt_base','percent','depth'])
with open('alt_percent.xls',mode='wt',encoding='utf-8') as out:
    out.write(header_str+'\n')
    for  record in result_lst:
        out.write('\t'.join(record)+'\n')
