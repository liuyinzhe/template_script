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
