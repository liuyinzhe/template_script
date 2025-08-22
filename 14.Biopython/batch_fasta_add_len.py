from Bio import SeqIO
# from Bio.Seq import Seq
# from Bio.SeqRecord import SeqRecord
# import re
import shutil
from pathlib import Path
'''
批量读取,修改并输出
生成后进行替换
'''


def GetAllFilePaths(pwd,wildcard='*'):
    '''
    获取目录下文件全路径，通配符检索特定文件名，返回列表
    param: str  "pwd"
    return:dirname pathlab_obj
    return:list [ str ]
    #https://zhuanlan.zhihu.com/p/36711862
    #https://www.cnblogs.com/sigai/p/8074329.html
    '''
    files_lst = []
    target_path=Path(pwd)
    for child in target_path.rglob(wildcard):
        if child.is_symlink():
            pass
        elif child.is_dir():
            pass
        elif child.is_file():
            files_lst.append(child) #Path object
    return files_lst

def process_fasta(input_file, output_file):
    """
    处理FASTA文件:计算序列长度并更新描述行
    :param input_file: 输入FASTA文件路径
    :param output_file: 输出FASTA文件路径
    """
    records = []
    for record in SeqIO.parse(input_file, "fasta"):
        # 计算序列长度
        seq_length = len(record.seq)
        # 更新描述信息
        record.description = f"{record.description} len={seq_length}"
        records.append(record)
    
    # 写入新文件
    SeqIO.write(records, output_file, "fasta")
    print(f"处理完成，结果已保存到 {output_file}")

def main():
    script_path =Path(__file__)
    script_dir = Path(script_path).parent
    #print(script_dir)
    current_dir = Path.cwd()

    for input_path in GetAllFilePaths(current_dir,'*.fa'):
        out_path = input_path.with_suffix('.len.fa')
        process_fasta(input_path,out_path)
        shutil.move(out_path, input_path)


if __name__ == "__main__":
    main()
