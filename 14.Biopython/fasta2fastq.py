from pathlib import Path
#from needletail import parse_fastx_file
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord


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


def main():
    # script_path =Path(__file__)
    # script_dir = Path(script_path).parent
    #print(script_dir)
    current_dir = Path.cwd()
    file_paths = GetAllFilePaths(current_dir,"*.fasta")
    for fasta_path in file_paths:
        file_name = fasta_path.stem # S5
        file_dir = fasta_path.parent
        fastq_records = [] # 存储每个SeqRecord单元
        #for record in parse_fastx_file("S5.fasta"):
        for record in SeqIO.parse(fasta_path, "fasta"):
            fastq_record = SeqRecord(
                        seq=Seq(record.seq),# str 必须转为 Seq类型
                        id=record.id, #序列名字
                        description="", # 描述为空
                        letter_annotations={ # 质量值信息
                            "phred_quality": [ord("I")-33] * len(record.seq) # I质量值符号 ，转为ascii码数字, [1] * 2 就是 [1,1]
                        }
                    )
            fastq_records.append(fastq_record) # 添加到列表中

        #I
        #fastq_file = "S5.fastq" # 指定输出名字
        fastq_file = file_dir.joinpath(file_name+".fastq")
        SeqIO.write(fastq_records, fastq_file, "fastq") # 输出


if __name__ == "__main__":
    main()


