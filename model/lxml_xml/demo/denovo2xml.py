from lxml import etree
from xml.etree import ElementTree as ET
from xml.dom import minidom
import sys
import pandas as pd

from collections import OrderedDict
"""
该函数用于向XML根元素添加子元素。

参数:
    root (Element): XML的根元素。
    tag_string (str): 要添加的子元素的标签名。
    text_string (str): 子元素的文本内容。
    attribute (dict, optional): 子元素的属性字典。默认为空字典。

返回:
    Element: 添加了子元素后的根元素。

示例:
    >>> root = ET.Element('root')
    >>> AddSubElement(root, 'child', 'text', {'attr': 'value'})
"""
def AddSubElement(root, tag_string,text_string,attribute={}):
    obj = ET.SubElement(root, tag_string,attrib=attribute)
    obj.text = text_string
    return root

def dict2xmltree(root,infomation_dictionary,attribute_key_lst):
    '''
    生成xml树
    :param root: 根标签，返回修改后的数据结构
    :param infomation_dictionary: 字典,key 为标签名,value 为标签值；遵循亲本关系
    :param attribute_key_lst: 列表,判断哪些是标签属性
    :return: xml树
    '''
    for key, val in infomation_dictionary.items():
        if isinstance(val, str):
            # key 是属性标签
            if key in attribute_key_lst:
                # attrib
                root.set(key,val)
            else:
                # key 不是属性标签
                key_obj = ET.SubElement(root, key)
                key_obj.text = val
        elif isinstance(val, dict):
            # 单独创建一个
            key_obj = ET.SubElement(root,key)
            val_dic = val
            key_obj = dict2xmltree(key_obj,val_dic,attribute_key_lst)
    return root

def split_dict_by_item_count(input_dict, max_items):
    """
    将字典根据元素个数拆分为多个字典
    :param input_dict: 输入的字典
    :param max_items: 每个字典允许的最大元素个数
    :return: 包含拆分后的字典的列表
    """
    result = []
    current_dict = OrderedDict()
    for key, value in input_dict.items():
        if len(current_dict) < max_items:
            current_dict[key] = value
        else:
            result.append(current_dict)
            current_dict = {key: value}
    if current_dict:
        result.append(current_dict)
    return result

def create_DDEM(sample_info_dic,index,out_prefix="str"):
    # 创建根标签
    root = ET.Element("NDNADImportFile",{'xmlns':'urn:NDNADImportFile-schema'})
    tree = ET.ElementTree(root)
    # 头部信息添加
    target_dic = {
        'VERSION':'0.9',

    }
    for key, val in target_dic.items():
        # 字典key:value作为属性添加到root
        root = AddSubElement(root, key, val)

    # 布局子元素SPECIMENS 到 NDNADImportFile 字段下
    specimens = ET.Element('SPECIMENS')
    root.append(specimens)


    # 单个样品
    # 创建 5层
    # (1) SPECIMEN 基本信息
    # (2) LOCUS 第二层
    # (3) ALLELES 属性层
    # (4) ALLELE 属性层
    # 之后组层追加append()
    # 遍历每个样品
    for sample_name in sample_info_dic:
        sample_locus_dic = sample_info_dic[sample_name] # locus:[[Allele1,Seq1],[Allele2,Seq2]]
        
        ################################  单个样品  ###################################
        # 创建 单个样品 SPECIMEN
        specimen_sample_A = ET.Element('SPECIMEN')

        # 作为属性的字段
        attribute_key_lst = ['SOURCEID','ALLELEREQUIRED']
        
        # (1) SPECIMEN 基本信息
        specimen_dic = {
                    'SOURCEID':'Yes',
                    'SPECIMENID':sample_name,
        }
        # 写入子标签
        specimen_sample_A = dict2xmltree(specimen_sample_A,specimen_dic,attribute_key_lst)
        
        for locus_name in sample_locus_dic:
            # (2) LOCUS 第二层
            # 创建 LOCUS 标签
            sample_A_locus = ET.Element('LOCUS')
            locus_dic = {
                    'LOCUSNAME':locus_name,
            }
            # 写入子标签
            sample_A_locus = dict2xmltree(sample_A_locus,locus_dic,attribute_key_lst)
            # locus 在 specimen_sample_A 下级
            specimen_sample_A.append(sample_A_locus)

            # (3) ALLELES 层
            alleles = ET.Element('ALLELES')

            alleles_dic={
                'ALLELEREQUIRED':"true",
            }
            # 写入子标签
            alleles = dict2xmltree(alleles,alleles_dic,attribute_key_lst)
            # alleles 在 locus_sample_A 下级
            sample_A_locus.append(alleles)

            locus_lst = sample_locus_dic[locus_name]
            # 遍历locus_lst 写入子标签
            for allele,seq in locus_lst:
                # (4) ALLELE 属性层
                sub_allele_sample = ET.Element('ALLELE')
                sub_allele_sample_dic = {
                    'ALLELEVALUE':allele,
                    'ALLELESEQS':seq,
                    'ALLELESEQL':seq,
                }
                # 写入子标签
                sub_allele_sample = dict2xmltree(sub_allele_sample,sub_allele_sample_dic,attribute_key_lst)

                # 每个子allele 追加到alleles下面
                alleles.append(sub_allele_sample)

        # 最终
        # 布局specimen_sample_A 追加在SPECIMENS 子类下
        specimens.append(specimen_sample_A)
    #
    ############################# 输出文件

    # (1) 版本
    tree.write(out_prefix+''+str(index)+'.xml',encoding='utf-8',short_empty_elements=False)
    # (2) 版本
    #创建XML树并写入文件,更好看一点
    xml_string = ET.tostring(root, encoding="utf-8",method='xml',short_empty_elements=False).decode('utf-8')
    xml_pretty_string = minidom.parseString(xml_string).toprettyxml(indent="  ",encoding="utf-8").decode('utf-8')
    with open(out_prefix+''+str(index)+'.type2.xml', "w",encoding="utf-8") as file:
        file.write(xml_pretty_string)

    return None

def main():
    
    # 读取表格获取信息
    '''
    SPECIMENID : sample,
    LOCUSNAME:locus,
        ALLELEVALUE:Allele1,
        ALLELESEQS:Seq1,
        ALLELESEQL:Seq1,

        ALLELEVALUE:Allele2,
        ALLELESEQS:Seq2,
        ALLELESEQL:Seq2,
    '''
    # 读取文件
    input_file = sys.argv[1]
    dataframe_df = pd.read_csv(input_file,encoding="utf-8",sep='\t',index_col=None)

    # 存储 样品字典
    sample_info_dic = OrderedDict()
    '''
    {
        sample:{
            locus:[[Allele1,Seq1],[Allele2,Seq2]]
    }
    '''
    #按行遍历
    for index, row in dataframe_df.iterrows():
        # print(index) # 输出每行的索引值
        # print(row) # 输出每一行
        # print(row['age'], row['sex'])  # 输出每一行指定字段值
        
        # Sample STR_ID Allele1  Seq1 Allele2 Seq2
        sample_name = row['Sample']
        str_id = row['STR_ID']
        allele1 = row['Allele1']
        allele2 = row['Allele2']
        seq1 = row['Seq1']
        seq2 = row['Seq2']
        # if pd.isna(allele2):
        #     print(sample_name,str_id,allele1,seq1,allele2,seq2)
        # 第一次创建value字典与value 列表类型
        if sample_name not in sample_info_dic:
            #print(sample_name)
            sample_info_dic[sample_name] = {}
        if str_id not in sample_info_dic[sample_name]:
            sample_info_dic[sample_name][str_id] = []

        sample_info_dic[sample_name][str_id].append([allele1,seq1])
        if not pd.isna(allele2):
            sample_info_dic[sample_name][str_id].append([allele2,seq2])
    
    sample_info_dic_lst = split_dict_by_item_count(sample_info_dic, max_items=150)

    for index, sample_sub_info_dic in enumerate(sample_info_dic_lst):
        create_DDEM(sample_sub_info_dic,index,out_prefix="str")



if __name__ == '__main__':
    main()
