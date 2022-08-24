import mappy as mp
aln = mp.Aligner("../NC_007605.1.fa",preset='map-ont')  # load or build index
if not aln: raise Exception("ERROR: failed to load/build index")

'''
sr for single-end short reads;
map-pb for PacBio read-to-reference mapping;
map-ont for Oxford Nanopore read mapping;
splice for long-read spliced alignment;
asm5 for assembly-to-assembly alignment;
asm10 for full genome alignment of closely related species.
Note that the Python module does not support all-vs-all read overlapping.
'''

'''
for name, seq, qual in mp.fastx_read("test/MT-orang.fa"): # read a fasta/q sequence
        for hit in a.map(seq): # traverse alignments
                print("{}\t{}\t{}\t{}".format(hit.ctg, hit.r_st, hit.r_en, hit.cigar_str))
'''

q_id='read_id'
seq='CCGCGGCCATTGGGCCCAGATTGAGAGACCAGTCCAGGGGCCCGAGGTTGGCAGCCAGCGGGCACCCGAGGTCCCAGCACCCGGTCCCTCCGGGGGGCAGAGACAGGCAGGGCCCCCCGGCAGCTGGCCCCGAGGAGGCGCCCGGAGTGGGGCCGGTCGGCTGGGCTGGCCGAGCCCGGGTCTGGGAGGTCTGGGGTGGCGAGCCTGCTGTCTCAGGAGGGGCCTGGCTCCGCCGGGTGGCCCTGGGGTAAGTCTGGGAGGCAGAGGGTCGGCCTAGGCCCGGGGAAGTGGAGGGGGATCGCCCGGGTCTCTGTTGGCAGAGTCCGGGCGATCCTCTGAGACCCTCCGGGCCCGGACGGTCGCCCTCAGCCCCCCAGACAGACCCCAGGGTCTCCAGGCAGGGTCCGGCATCTTCAGGGGCAGCAGGCTCACCACCACAGGCCCCCCAGACCCGGGTCTCGGCCAGCCGAGCCGACCGGCCCCGCGCCTGGCGCCTCCTCGGGGCCAGCCGCCGGGGTTGGTTCTGCCCCTCTCTCTGTCCTTCAGAGGAACCAGGGACCTCGGGCACCCCAGAGCCCCTCGGGCCCGGGGGCATCGGGGGGTGGGGCATGGGGGGCCGCGCATTCCTGGAAAAAGTGGAGGGGGCGTGGCCTTCCCCCGCGGCCCCCCAGCCCCCCCGCACAGAGCGGCGCTACGGCGGGCGGGCGGCGGGGGGTCGGGGTCCGCGGGCTCCGGGGGCTGCGGGCGGTGGATGGCGGCGGACGTTCCGGGGATCGGGGGGGTCGGGGGGCGCCGCGCGGGCGCAGCCATGCGTGACCGTGATGAGGGGGCAGGGTCGCAGGGGGTGTGTCTGGTGGGGGCGGGAGCGGGGGGCGGCGCGGGAGCCTGCACGCCGTTGGAGGGTAGAATGACAGGGGGCGGGGACAGAGAGGCGGTCGCGCCCCCGGCCGCGCCAGCCAAGCCCCCAAGGGGGGCGGGGAGCGGGCAATGGAGCGTGACGAAGGGCCCCAGGGCTGACCCCGGCAAACGTGACCCGGGGCTCCGGGGTGACCCAGCCAAGCGTGACCAAGGGGCCCGTGGGTGACACAGGCAACCCTGACAAAGGCCCCCCAGGAAAGACCCCCGGGGGGCATCGGGGGGGGTGTTGGCGGGGGCATGGGGGGGTCGGATTTCGCCCTTATTGCCCTGTTT'
q_len=len(seq)
for hit in aln.map(seq,seq2=None, cs=False, MD=False): # traverse alignments
    #print("{}\t{}\t{}\t{}\t{}".format(hit.is_primary,hit.read_num, hit.ctg, hit.r_st, hit.r_en, hit.cigar_str))
    #print(dir(hit))
    if not hit.is_primary :
        continue
    print(hit.strand,hit.blen)
    print([q_id,str(q_len), str(hit.q_st),str(hit.q_en),hit.strand ,hit.ctg ,str(hit.ctg_len) ,str(hit.r_st) ,str(hit.r_en),str(hit.NM) ,str(hit.blen) ,str(hit.mapq)])
    result = '\t'.join([q_id,str(q_len), str(hit.q_st),str(hit.q_en),str(hit.strand) ,hit.ctg ,str(hit.ctg_len) ,str(hit.r_st) ,str(hit.r_en),str(hit.NM) ,str(hit.blen) ,str(hit.mapq)])
    print(hit.cigar_str)
    print(hit.cigar)

'''
#Query sequence name
ctg #Target sequence name; reference sequence

#PAF: a Pairwise mApping Format
#q_id	1	string	Query sequence name
#q_len	2	int	Query sequence length
q_st	3	int	Query start (0-based; BED-like; closed)
q_en	4	int	Query end (0-based; BED-like; open)
strand	5	char	Relative strand: "+" or "-"
ctg	6	string	Target sequence name
ctg_len	7	int	Target sequence length
r_st	8	int	Target start on original strand (0-based)
r_en	9	int	Target end on original strand (0-based)
NM	10	int	Number of residue matches
blen	11	int	Alignment block length
mapq	12	int	Mapping quality (0-255; 255 for missing)


ctg: name of the reference sequence the query is mapped to
ctg_len: total length of the reference sequence
r_st and r_en: start and end positions on the reference
q_st and q_en: start and end positions on the query
strand: +1 if on the forward strand; -1 if on the reverse strand
mapq: mapping quality
blen: length of the alignment, including both alignment matches and gaps but excluding ambiguous bases.
mlen: length of the matching bases in the alignment, excluding ambiguous base matches.
NM: number of mismatches, gaps and ambiguous positions in the alignment
trans_strand: transcript strand. +1 if on the forward strand; -1 if on the reverse strand; 0 if unknown
is_primary: if the alignment is primary (typically the best and the first to generate)
read_num: read number that the alignment corresponds to; 1 for the first read and 2 for the second read
cigar_str: CIGAR string
cigar: CIGAR returned as an array of shape (n_cigar,2). The two numbers give the length and the operator of each CIGAR operation.
MD: the MD tag as in the SAM format. It is an empty string unless the MD argument is applied when calling mappy.Aligner.map().
cs: the cs tag.
'''
