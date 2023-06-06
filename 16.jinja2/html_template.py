from jinja2 import Environment, FileSystemLoader 
import json
import re
import os
from pathlib import Path
import math

def convertSizeUnit(sz, source='B', target='auto', return_unit=False):
    '''
    文件大小指定单位互转，自动则转换为最大的适合单位
    '''
    #target=='auto' 自动转换大小进位,大于1000 就进位；对于不能进位的返回原始大小和单位
    #return_unit 是否返回 单位
    source = source.upper()
    target = target.upper()
    return_unit = bool(return_unit)
    unit_lst = ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'AUTO']
    unit_dic = {'B': 0, 'KB': 1, 'MB': 2,
                'GB': 3, 'TB': 4, 'PB': 5, 'AUTO': -1}
    source_index = unit_dic[source]
    target_index = unit_dic[target]
    index = math.log(sz, 1000)  # 计算数字中有几个1000 相乘过；或者说可以被几个1000 除掉
    if target == 'AUTO':
        if index < 1:  # source 比 target 还大，不能进位，自动就返回原始的
            return sz, source
        unit_index = int(index)
        # 得到的 可 进位的数字+原始的 index;或者真正的单位
        target_unit = unit_lst[unit_index+source_index]
        result_sz = sz/1000**(unit_index)  # 进位
 
    else:  # 非自动
        if index < 1:  # source 的单位比 target 还大
            cmp_level = source_index-target_index  # 差距
            result_sz = sz*1000**cmp_level  # 退位，乘以1000
            target_unit = target
 
        else:  # source 的单位比 target 小
            cmp_level = target_index - source_index  # 差距
            result_sz = sz/1000**cmp_level  # 进位 ，除以1000
            target_unit = target
    if return_unit:
        return result_sz, target_unit
    else:
        return result_sz
# convertSizeUnit(sz, source='B', target=target)

def parse_fastp_json(sample,fastp_json):
    # fastp 内容表头
    summary_target_lst = ['total_reads', 'total_bases', 'q20_bases', 'q30_bases', 'q20_rate', 'q30_rate',  'gc_content']
    json_str = ""
    with open(fastp_json,mode='rt',encoding='utf-8') as fh:
        json_str = fh.read()
    fastp_dict = json.loads(json_str)

    # 输出样品名与表头
    summary_header = ['Sample','total reads(M)','total bases(G)','clean reads(M)','clean bases(G)','valid bases',
                    'Q30 bases','GC content']
    #数值
    before_total_reads = int(fastp_dict['summary']['before_filtering']['total_reads'])
    before_total_bases = int(fastp_dict['summary']['before_filtering']['total_bases'])
    after_total_reads = int(fastp_dict['summary']['after_filtering']['total_reads'])
    after_total_bases = int(fastp_dict['summary']['after_filtering']['total_bases'])
    summary_tab_lst = [sample,"{:.2f}%".format(convertSizeUnit(before_total_reads, source='B', target='MB', return_unit=False)), 
                     "{:.2f}%".format(convertSizeUnit(before_total_bases, source='B', target='GB', return_unit=False)), 
                     "{:.2f}%".format(convertSizeUnit(after_total_reads, source='B', target='MB', return_unit=False)),
                     "{:.2f}%".format(convertSizeUnit(after_total_bases, source='B', target='GB', return_unit=False)),
                     "{:.2f}%".format(int(fastp_dict['summary']['after_filtering']['total_bases'])/int(fastp_dict['summary']['before_filtering']['total_bases'])*100),
                     "{:.2f}%".format(float(fastp_dict['summary']['after_filtering']['q30_rate'])*100),
                     "{:.2f}%".format(float(fastp_dict['summary']['after_filtering']['gc_content'])*100)
                     ]

    # 分表
    before_filtering_lst = []
    after_filtering_lst = []
    for  key in summary_target_lst:
        #print(fastp_dict['summary']['before_filtering'][key])
        if key in ['q20_rate', 'q30_rate',  'gc_content']:
            before_filtering_lst.append(str(fastp_dict['summary']['before_filtering'][key]*100))
            after_filtering_lst.append(str(fastp_dict['summary']['after_filtering'][key]*100))
        else:
            before_filtering_lst.append(str(fastp_dict['summary']['before_filtering'][key]))
            after_filtering_lst.append(str(fastp_dict['summary']['after_filtering'][key]))

    return summary_header,summary_tab_lst,summary_target_lst,before_filtering_lst,after_filtering_lst

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
        if child.is_dir():
            pass
        elif child.is_file():
            files_lst.append(child)
    return files_lst


def generate_html( qc_table, institution_str, project_id_str,first_group_str,vs_group):
    env = Environment(loader=FileSystemLoader('./'))
    template = env.get_template('template.html')     
    with open("result.html",mode='w+',encoding='utf-8') as fout:   
        html_content = template.render(institution=institution_str , 
                                       first_group = first_group_str,
                                        project_id=project_id_str,
                                        qc_table=qc_table,
                                        vs_group = vs_group)
        fout.write(html_content)
 
if __name__ == "__main__":
    '''
    <table border="1" width = "40%" cellspacing='0' cellpadding='0' align='left'>
    <tr>        
        <th>机柜号</th>
        <th>检测时间</th>
        <th>检测结果</th>
        <th>详细信息</th>
        <th>图片路径</th>
    </tr>
 
    {% for item in body %}
    <tr align='center'>
        <td>{{ item.cabID }}</td>
        <td>{{ item.shijian }}</td>
        <td>{{ item.final_result }}</td>
        <td>{{ item.info }}</td>
        <td><a href={{item.image_path}}>图片</a> </td>
    </tr>
    {% endfor%}
    </table>
    '''
    ## 跳转脚本所在目录
    pwd = os.path.split(os.path.realpath(__file__))[0]
    #pwd = os.getcwd()
    pwd = Path(pwd)
    os.chdir(pwd)
    file_list = GetAllFilePaths(pwd,wildcard='*.fastp.json')
    summary_header = "" # 
    #summary_tab_all_list = []
    
    qc_table = []
    for sample_path in file_list:
        #print(type(sample_path))
        sample = re.split(r"\.",str(sample_path.name))[0] 
        fastp_json_path = sample_path
        summary_header,summary_tab_lst,summary_target_lst,before_filtering_lst,after_filtering_lst = parse_fastp_json(sample,fastp_json_path)
        #summary_tab_all_list.append(summary_tab_lst)
        sample,total_reads,total_bases,clean_reads,clean_bases,valid,q30,gc = summary_tab_lst
        result = {
                'sample':sample,
                'total_reads':total_reads, 
                'total_bases':total_bases, 
                'clean_reads':clean_reads, 
                'clean_bases':clean_bases,
                'valid':valid,
                'q30':q30,
                'gc':gc}
        qc_table.append(result)
    vs_group = ["A_vs_B",]
    generate_html(qc_table, 'xxxxx', 'Project',"A_vs_B",vs_group)

# 使用Jinja2模板引擎生成html报告
# https://zhuanlan.zhihu.com/p/613119368
# 从零开始学 Python 之Jinja2 模板引擎
# https://zhuanlan.zhihu.com/p/520383462
# Python之jinja2模板引擎生成HTML
# https://blog.csdn.net/zong596568821xp/article/details/100522584
