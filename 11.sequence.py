import gzip
import re
from pyfaidx import Fasta

def check_gzip_format(file_nm):
    '''
    绝大多数gzip 前两位为"\x1f\x8b",但是不全都灵验
    '''
    # suffix check
    if file_nm.endswith('.gz'):
        return True
    #magic_number check
    magic_flag = False
    with open(file_nm,mode='rb') as fh:
        magic_number =fh.read(2)
        if magic_number==b'\x1f\x8b':
            magic_flag = True
        else:
            magic_flag = False
    return magic_flag

def format_str(string,format_len):
    '''
    字符按照长度换行
    '''
    string = string.strip()
    start = 0
    new_string = ''
    str_len = len(string)
    if str_len<=format_len:
        new_string = string
        return new_string
    for idx in range(str_len):
        now_len = idx+1
        if now_len % format_len == 0 :
            order = idx+1
            new_string +=string[start:order]+'\n'
            start = idx+1
    if order < str_len: 
        new_string +=string[order:]
    return new_string
        
def format_str(input_str,width):
    '''
    字符按照长度换行,思路2，改进版
    '''
    out_str = ''
    for idx in range(0,len(input_str),width):
        if idx ==0 :
            out_str=input_str[idx:idx+width]
        else:
            out_str += '\n'+input_str[idx:idx+width]
    return out_str
    
def fa_get_seq(file_nm,id_lists,format_len=0):
    '''
    fasta 提取序列
    format_len 0 原样输出
    yield 迭代器返回结果 seq_id,seq
    节省内存
    '''
    seq_id = ''
    seq = ''
    id_list = id_lists.copy()
    if check_gzip_format(file_nm) :
        with gzip.open(file_nm,mode='rb') as fh:
            for bytes_line in fh:
                line= str(bytes_line,encoding='utf-8')
                if line.startswith('>'):
                    # output
                    if len(id_list)==0:
                        break
                    if seq_id and seq_id in id_list:
                        # 在就直接返回yield,清空
                        id_list.remove(seq_id)
                        if format_len != 0:
                            input_str = re.sub('[\n\r]','',seq)
                            seq = format_str(input_str,format_len)
                        yield seq_id,seq.strip()
                    # new obj
                    seq = ''
                    seq_id = re.split('[>\s]',line.strip())[1]
                else:
                    seq += line
            #最后一行yield
            if seq_id in id_list:
                # 在就直接返回yield,清空
                id_list.remove(seq_id)
                if format_len != 0:
                    input_str = re.sub('[\n\r]','',seq)
                    seq = format_str(input_str,format_len)
                yield seq_id,seq.strip()
    else:
        with open(file_nm,mode='r') as fh:
            for line in fh:
                if line.startswith('>'):
                    # output
                    if len(id_list)==0:
                        break
                    if seq_id and seq_id in id_list:
                        # 在就直接返回yield,清空
                        id_list.remove(seq_id)
                        if format_len != 0:
                            input_str = re.sub('[\n\r]','',seq)
                            seq = format_str(input_str,format_len)
                        yield seq_id,seq.strip()
                    # new obj
                    seq = ''
                    seq_id = re.split('[>\s]',line.strip())[1]
                else:
                    seq += line
            #最后一行yield
            if seq_id in id_list:
                # 在就直接返回yield,清空
                id_list.remove(seq_id)
                if format_len != 0:
                    input_str = re.sub('[\n\r]','',seq)
                    seq = format_str(input_str,format_len)
                yield seq_id,seq.strip()

def split_dna(dna, kmer_size):
    '''
    https://www.cnblogs.com/jessepeng/p/12882606.html
    '''
    kmers = []
    for start in range(0,len(dna)-(kmer_size-1),1):
        kmer = dna[start:start+kmer_size]
        kmers.append(kmer)
    return kmers

def split_sw(input_list, win_size ,step):
    '''
    yield type list
    '''
    for start in range(0,len(input_list)-win_size +1,step):
        win = input_list[start:start+win_size]
        yield win



def reverse_complement(seq):
    '''get reverse complement  seq'''
    rule = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G', 'N': 'N',']':'[', '[':']'}
    return ''.join([rule[each] for each in seq.upper()][::-1])


def get_flank_seq(genome_path,chrom,start,end,flank_size):
    
    # 1-base to 0-base
    start -= 1
    end -= 1

    if end < start:
        raise Exception("warnning:end < start:"+str(end)+"<"+str(start))
    
    chrom = chrom.lower()
    # read genome file
    genome = Fasta(genome_path)
    if start == end:
        # SNP
        SNP_base = genome[chrom][start:end+1].seq
        complete_seq = genome[chrom][start-flank_size:end+1+flank_size].seq
        mark_seq = genome[chrom][start-flank_size:start].seq +"["+SNP_base+"]"+genome[chrom][end+1:end+1+flank_size].seq
    elif abs(end - start) == 1: 
        # INS
        INS_base = ""
        complete_seq = genome[chrom][start-flank_size+1:end+1+flank_size].seq
        mark_seq = genome[chrom][start-flank_size+1:start+1].seq +"["+INS_base+"]"+genome[chrom][end:end+flank_size].seq
    else:
        # DEL or delins
        DELINS_base = genome[chrom][start:end+1].seq
        complete_seq = genome[chrom][start-flank_size+1:end+1+flank_size].seq
        mark_seq = genome[chrom][start-flank_size:start].seq +"["+DELINS_base+"]"+genome[chrom][end+1:end+1+flank_size].seq
    rc_mark_seq = reverse_complement(mark_seq)
    return complete_seq,mark_seq,rc_mark_seq
