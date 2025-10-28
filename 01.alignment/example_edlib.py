import edlib
# 3-20
#<Iteration_query-len>20</Iteration_query-len>
# <Hsp_hit-frame>-1</Hsp_hit-frame>
# 简单示例  3290-3307
#           3290-3309
#query = "AATCCCGCTCACAGGTCCTCTGCTA"
query = "GATACAAGGGGGCTGCCATT"
        # "  TACAAGGGGGCTGCCATT"
        # "GGTACAAGGGGGCTGCCATT"
target = "TTGGTGAGAGGGTACAAGGGGGCTGCCATTTCTGCAAACC" # 前后5bp;或者不错位  # 输入是1-base [4,10] ,转0-base [3,10]
result = edlib.align(query, target, mode="HW",task="path")# NW SHW HW
nice = edlib.getNiceAlignment(result, query, target)
print(result)
'''
{
    'editDistance': 1,
    'alphabetLength': 4,
    'locations': [(10, 29)],
    'cigar': '1=1X18='}
'''
print("#############")
# editDistance 1 <class 'int'>  错配情况总数
print("editDistance",result["editDistance"],type(result["editDistance"]))
# print("matched_aligned",result["matched_aligned"])
print("#############")
print("matched_aligned",nice["matched_aligned"])
print(nice)
'''
{  
   'query_aligned':    'GATACAAGGGGGCTGCCATT', 
   'matched_aligned':  '|.||||||||||||||||||',
   'target_aligned':   'GGTACAAGGGGGCTGCCATT'
}
'''

print(nice.values())
print("\n".join(nice.values()))

'''
12345678901234567890  20
GATACAAGGGGGCTGCCATT  query
|.||||||||||||||||||
GGTACAAGGGGGCTGCCATT  target
'''


'''
minimap2  mapy  根据index提取ref区域序列
import mappy as mp
a = mp.Aligner("test/MT-human.fa")  # load or build index
if not a: raise Exception("ERROR: failed to load/build index")
s = a.seq("MT_human", 100, 200)     # retrieve a subsequence from the index


needletail      遍历序列
from needletail import parse_fastx_file
for record in parse_fastx_file("myfile.fastq"):
    print(record.id)
    print(record.seq)
    print(record.qual)
'''
