import json

######################begin     json parse      begin######################

def read_json(input_json):
    '''
    json文件读取，存为字典
    from pathlib import Path
    '''
    json_dic = {}
    P=Path(input_json)
    if P.exists():
        if not P.is_absolute():
            input_json = str(P.resolve())
    else:
        print("Warring! "+input_json+" is not  exists! \n")
    with open(input_json, encoding='utf-8', mode='r') as f:
        json_dic = json.load(f)
    return json_dic

def dict_generator(indict, pre=None):
    pre = pre[:] if pre else []
    if isinstance(indict, dict):
        for key, value in indict.items():
            if isinstance(value, dict):
                for d in dict_generator(value, pre + [key]):
                    yield d
            elif isinstance(value, list) or isinstance(value, tuple):
                for v in value:
                    for d in dict_generator(v, pre + [key]):
                        yield d
            else:
                yield pre + [key, value]
    else:
        yield pre + [indict]
 
######################end     json parse      end######################

#################begin  dict 转目录 begin#####################
 
def dic2path(input_dic,pre="/a/b/c/\\S+?/\\S+?"):
    path_lst = []
    for x in dict_generator(input_dic):
        #a="\\".join(x)
        #a=os.path.join(*x)
        new_path=Path('/').joinpath(pre,*x)
        path_lst.append(str(new_path))
    return path_lst
 
################end  dict转目录  end########################
 

#################begin 序列化 begin#####################
def save_json(json_dic,file_path):
    #sort_keys	True    按键名字母排序(False)
    #indent    4	空格缩进数量(None)
    #separators	(',', ':')    移除多余的分隔符空格，使JSON字符串更加紧凑(', ', ': ')
    #ensure_ascii	True    处理非ASCII字符为Unicode序列
    json_str = json.dumps(json_dic, sort_keys=True, indent=4, separators=(',', ':'), ensure_ascii=False)
    with open(file_path,mode='wt',encoding='utf-8') as f:
        f.write(json_str)
################end  序列化  end########################
