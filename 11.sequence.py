import gzip
import re


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
