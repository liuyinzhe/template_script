# -*- coding: utf-8 -*-
# 设置默认编码输出的,python3 默认内部 unicode,输出 utf-8

# unicode方便于跨平台
# python3 内部存储字符串按照 unicode, 输出为utf-8
# str.decode('ascii').encode('utf-8')
# 

import gzip
import shutil

def get_gzip_ISIZE(gzip_file):
    '''
    https://blog.csdn.net/jison_r_wang/article/details/52068607
    #取模(mod)与取余(rem)的区别
    #https://www.runoob.com/w3cnote/remainder-and-the-modulo.html
    # 这里都是正整数所以不需要区分取模还是取余
    '''
    with open(gzip_file, 'rb') as f:
        data = data = f.read(1)
        if not data:
            print(gzip_file,'gz_is_empty')
            return -1
        f.seek(-4 , os.SEEK_END)
        length = int.from_bytes(f.read(), byteorder='little')
        isize = length%(2**32)
    return isize

#Example of how to GZIP compress an existing file

with open('/home/joe/file.txt', 'rb') as f_in:
    with gzip.open('/home/joe/file.txt.gz', 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)

 def check_complete_file(task_list):
    uncomplete_task_list = []
    for child_jobs_list in task_list: # split_num
        sizeInBytes,file_type,url,outfile = child_jobs_list
        file_obj = Path(outfile)
        # 检查文件是否存在
        if file_obj.exists():
            if outfile.endswith(".gz"):
                # 存在，则检查大小
                isize = get_gzip_ISIZE(file_obj) # gzip input size
                size_mod = sizeInBytes%(2**32)
                if size_mod == isize:
                    continue
                else:
                    uncomplete_task_list.append(child_jobs_list)
            else: 
                # 检查文件对象大小
                fsize=file_obj.stat().st_size
                if sizeInBytes == fsize:
                    continue
                else:
                    uncomplete_task_list.append(child_jobs_list)
        else:
            uncomplete_task_list.append(child_jobs_list)
    return uncomplete_task_list


def check_gzip_format(file):
    '''
    绝大多数gzip 前两位为"\x1f\x8b",但是不全都灵验
    '''
    # suffix check
    if file.endswith('.gz'):
        return True
    #magic_number check
    magic_flag = False
    with open(file,mode='rb') as fh:
        magic_number =fh.read(2)
        if magic_number==b'\x1f\x8b':
            magic_flag = True
        else:
            magic_flag = False
    return magic_flag

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





with gzip.open('input.gz',mode='rb') as fh:
    for bytes_line in fh:
        print(type(bytes_line)) #bytes
        line = bytes_line.encode()
        print(line.decode('utf-8'))# source 是已知 字符串为utf-8 编码的情况; 解码为unicode
        #乱码，则可能是 中文编码 gb2312,gbk,utf-8-sig
        print(line)

with gzip.open('input.gz',mode='rt') as fh:
    for line in fh:
        print(type(line))
        print(line.decode('utf-8'))# source 是已知 字符串为utf-8 编码的情况; 解码为unicode
        #乱码，则可能是 中文编码 gb2312,gbk,utf-8-sig
        print(line)

with gzip.open('unicode.gz',mode='wb') as out:
    out.write('unicode\n'.encode())#.encode('utf-8') ,字符串方法，默认编码成 utf-8
    out.write(b'unicode\n') # ASCII 字符 转二进制
    out.write(bytes('unicode\n'.encode('utf-8'))) # 转化为 bytes 类型，对于非 ASCII 字符，print 输出的是它的字符编码值（十六进制形式）
    # bytes 类也有一个 decode() 方法，通过该方法可以将 bytes 对象转换为字符串
    # bytes_str.decode('utf-8')
