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
