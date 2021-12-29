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
    for idx in range(str_len):
        now_len = idx+1
        if now_len % format_len == 0 :
            order = idx+1
            new_string +=string[start:order]+'\n'
            start = idx+1
    if order < str_len: 
        new_string +=string[order:]
    return new_string
        

def get_seq(file_nm,id_list,format_len=0):
    '''
    fasta 提取序列
    format_len 0 原样输出
    yield 迭代器返回结果 seq_id,seq
    节省内存
    '''
    seq_id = ''
    seq = ''
    if check_gzip_format(file_nm) :
        with gzip.open(file_nm,mode='rb') as fh:
            for bytes_line in fh:
                line= str(bytes_line,encoding='utf-8')
                if line.startswith('>'):
                    # output
                    if seq_id and seq_id in id_list:
                        # 在就直接返回yield,清空
                        id_list.remove(seq_id)
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
                yield seq_id,seq.strip()
    else:
        with open(file_nm,mode='r') as fh:
            for line in fh:
                if line.startswith('>'):
                    # output
                    if seq_id and seq_id in id_list:
                        # 在就直接返回yield,清空
                        id_list.remove(seq_id)
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
                yield seq_id,seq.strip()
