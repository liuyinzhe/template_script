from pathlib import Path
import argparse
import sys


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
            files_lst.append(str(child))
    return files_lst


def get_args():
    '''
    python draw.py -i base_info.tsv
    '''
    parser = argparse.ArgumentParser(
        description='''''', usage="python3 %(prog)s [options]")
    # 输入文件
    parser.add_argument(
        "-i","--input_dir", help="dir for clone.", required=True,type=str, metavar="File")
    # 输出文件与输入文件路径相同
    if len(sys.argv) < 1:
        parser.print_help()
        sys.exit()
    else:
        args = parser.parse_args()

    return args

def main():
    script_path =Path(__file__)
    script_dir = Path(script_path).parent
    #print(script_dir)
    current_dir = Path.cwd()
    '''
    获取目标目录，遍历目录下所有文件;
    获取文件父目录名字, 软连接文件
    
    判断目录名  在文件名是否有重叠
    有重叠则判断为样品名目录
    用于创建目录 和 软连接文件
    字典为 {样品名:[目录下软连接文件全路径]}

    '''
    args = get_args()
    input_dir = args.input_dir
    #file_lst = GetAllFilePaths(input_dir,wildcard='*.gz')
    file_lst = GetAllFilePaths(input_dir)
    sample_dict = {}
    for file_path in file_lst:
        parent_dir = Path(file_path).parent
        parent_dir_name = parent_dir.name
        file_name = Path(file_path).name
        if parent_dir_name in file_name:
            if parent_dir_name not in sample_dict:
                sample_dict[parent_dir_name] = []
            sample_dict[parent_dir_name].append(file_path)

    '''
    遍历sample_dict,当前目录创建样品名目录,并在样品名目录下创建软连接文件
    '''
    for sample_name in sample_dict:
        sample_dir = current_dir.joinpath(sample_name)
        sample_dir.mkdir(exist_ok=True,parents=True)
        for file_path in sample_dict[sample_name]:
            file_name = Path(file_path).name
            link_path = sample_dir.joinpath(file_name)
            if not link_path.exists():

                link_path.symlink_to(file_path)
                # 软链接 {link_path}，指向 {file_path}
            else:
                if link_path.is_symlink():
                    link_path.unlink()
                    link_path.symlink_to(file_path)
if __name__ == "__main__":
    main()
