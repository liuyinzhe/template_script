import hashlib
from pathlib import Path
import io

#参考自#https://www.iteye.com/blog/ryan-liu-1530029
def md5hex(word):
    """ MD5加密算法，返回32位小写16进制符号 """
    #python3#all strings are now Unicode
    #if isinstance(word, unicode):
    #    word = word.encode("utf-8")
    #elif not isinstance(word, str):
    #    word = str(word)
    
    if isinstance(word, bytes):
       word = str(word,encoding="utf-8")
    elif not isinstance(word, str):
        word = str(word,encoding="utf-8")
    m = hashlib.md5()
    m.update(word)
    return m.hexdigest()


def md5sum(fname):
    """ 计算文件的MD5值 """
    def read_chunks(fh):
        fh.seek(0)
        default_buffer_size = io.DEFAULT_BUFFER_SIZE
        chunk = fh.read(default_buffer_size)
        while chunk:
            yield chunk
            chunk = fh.read(default_buffer_size)
        else: #最后要将游标放回文件开头
            fh.seek(0)
    m = hashlib.md5()
    fname_obj = Path(fname)
    if isinstance(fname, str) \
            and fname_obj.exists():
        with open(fname, "rb") as fh:
            for chunk in read_chunks(fh):
                m.update(chunk)
    #上传的文件缓存 或 已打开的文件流
    elif fname.__class__.__name__ in ["StringIO", "StringO"] \
                or fname_obj.is_file():
        for chunk in read_chunks(fname):
            m.update(chunk)
    else:
        return ""
    return m.hexdigest()

print(md5sum(r'C:\Users\xxxx\Desktop\xxx.txt'))
