import chardet


def get_encoding(file):
    with open(file, "rb") as f:
        # 10k bit
        data = f.read(10000)
        return chardet.detect(data)['encoding']

def change_encoding(file,code_type):
    '''
    原始代码来自:https://github.com/KpiHang/Python-utilities/blob/master/%E6%96%87%E6%9C%AC%E8%BD%AC%E7%A0%81/other2utf8.py
    '''
    # decoding-->binary；
    with open(file, "r", encoding=code_type) as f:
        content = f.read()
    
    # bytes 转为字符串  #enconde
    # str(content,encoding='utf')
    # string 转为bytes  #decode
    # bytes(content.encode(encoding='utf-8'))

    # binary-->encoding；
    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)
    print("编码已经转为：utf-8。")

