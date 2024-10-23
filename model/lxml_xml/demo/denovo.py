from lxml import etree
from xml.etree import ElementTree as ET
from xml.dom import minidom

def AppendElement(root, tag_string,text_string):
    Element_obj = ET.Element(tag_string)
    Element_obj.text = text_string
    root.append(Element_obj)
    return root
#root = add_tag(root,'HEADERVERSION','0.9')

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

# 创建根标签
root = ET.Element("NDNADImportFile",{'xmlns':'urn:NDNADImportFile-schema'})
tree = ET.ElementTree(root)

target_dic = {
    'HEADERVERSION':'0.9',
    'MESSAGETYPE':'Import',
    'DESTINATIONLAB':'BEIJING',
    'NDNADLABORATORYID':'',
    'SOURCELAB':'BEIJING',
    'SOURCELABORTORYID':'',
    'SUBMITBYUSERID':'GNIBUIL',
    'SUBMITDATETIME':'2020-02-02T21:51:44',
    'BATCHID':'GEL2012_01_04_101',
    'KITNAME':'SampleKIT',
    'KITID':'2020-01-01.1',
    'KITBRACODENUMBER':'',
    'SEQUENCERMANUFACTURER':'Sample SEQ 001',
    'SEQUENCERMANUFACTURERID':'',
    'SERIALNUMBER':'',
    'SEQUENCINGMETHOD':'',
    'SEQUENCEANALYSISSOFTWARE':'',
}


# Sequencer_Manufacturer_ID = ET.Element('SEQUENCERMANUFACTURERID')
# Sequencer_Manufacturer_ID.text = ''

for key, val in target_dic.items():
    root = AddSubElement(root, key, val)

specimens = ET.Element('SPECIMENS')
root.append(specimens)
specimen_A = ET.Element('SPECIMEN')
specimens.append(specimen_A)
#specimens = ET.SubElement(root, 'SPECIMENS',attrib={'SOURCEID':'YES','CASEID':'FL2020_02_02_ABC','PARTIAL':'true'})

# sample A 
# specimen_A = ET.SubElement(specimens,"SPECIMEN",attrib={'SOURCEID':'YES','CASEID':'FL2020_02_02_ABC','PARTIAL':'true'})
# sample A infomation
A_info_dic = {
            'SOURCEID':'YES',
            'CASEID':'FL2020_02_02_ABC',
            'PARTIAL':'true',
            'SPECIMENID':'IMP_0001A',
            'SPECIMENCATEGORY':'Forensic, Unknown',
            'SPECIMENCOMMENT':'This is comment',
            'MTDNA':{
                'LOCUSID':'',
                'READINGBY':'',
                'READINGDATETIME':'',
                'BATCHID':'',
                'KIT':'',
                'SEQUENCEDLENGTH':'16570',
                'FRAGMENTSTART':'1',
                'FRAGMENTEND':'16570',
                'FRAGMENTSEQUENCEDDATA':'GATCACAGGTCTATCACCCTATTAACCACTCACG',
                'DIFFERENTIALBASEDATA':'',
                'HETEROPLASMYBASEDATA':'',
            }
        }

attribute_key_lst = ['SOURCEID','CASEID','PARTIAL']

specimen_A = dict2xmltree(specimen_A,A_info_dic,attribute_key_lst)
# for key, val in A_info_dic.items():
#     if isinstance(val, str):
#         key_obj = ET.SubElement(specimen_A, key)
#         key_obj.text = val
#     elif isinstance(val, dict):
#         # 一级字典
#         # son1 = ET.SubElement(root,'son',attrib={'name': '儿1'})
#         key_obj = ET.SubElement(specimen_A, key, attrib=val)
# sample B
specimen_B = ET.SubElement(specimens,"SPECIMEN",attrib={'SOURCEID':'YES','CASEID':'FL2024_02_02_ABC','PARTIAL':'true'})

# for key, val in target_dic.items():
#     specimens = AddSubElement(specimens, key, val)
############################# 根标签下一级标签
# 1
# root = AddSubElement(root,'HEADERVERSION','0.9')
# 2
# root = AppendElement(root,'HEADERVERSION','0.9')
# example
# header_version = ET.Element('HEADERVERSION')
# header_version.text = '0.9'
# root.append(header_version)


# message_type = ET.Element('MESSAGETYPE')
# message_type.text = 'Import'

# destination_lab= ET.Element('DESTINATIONLAB')
# destination_lab.text = 'BEIJING'

# NDNAD_laboratory_id = ET.Element('NDNADLABORATORYID')
# NDNAD_laboratory_id.text = ''

# source_lab = ET.Element('SOURCELAB')
# source_lab.text = 'BEIJING'

# source_labortory_id = ET.Element('SOURCELABORTORYID')
# source_labortory_id.text=""

# submit_by_user_id = ET.Element('SUBMITBYUSERID')
# submit_by_user_id.text = 'GNIBUIL'

# submit_date_time = ET.Element('SUBMITDATETIME')
# submit_date_time.text = '2020-02-02T21:51:44'

# batch_id = ET.Element('BATCHID')
# batch_id.text = '2020-02-02T21:51:44'


# kit_name = ET.Element('KITNAME')
# kit_name.text = 'SampleKIT'

# kit_id = ET.Element('KITID')
# kit_id.text = '2020-01-01.1'

# kit_bracode_number = ET.Element('KITBRACODENUMBER')
# kit_bracode_number.text = ''

# Sequencer_Manufacturer = ET.Element('SEQUENCERMANUFACTURER')
# Sequencer_Manufacturer.text = 'Sample SEQ 001'

# Sequencer_Manufacturer_ID = ET.Element('SEQUENCERMANUFACTURERID')
# Sequencer_Manufacturer_ID.text = ''


# root.append(message_type)
# root.append(destination_lab)
# root.append(NDNAD_laboratory_id)
# root.append(source_lab)
# root.append(source_labortory_id)
# root.append(submit_by_user_id)
# root.append(submit_date_time)
# root.append(batch_id)
# root.append(kit_name)

############################# 根标签下一级标签

# (1) 版本
tree.write('cool.xml',encoding='utf-8',short_empty_elements=True)
# (2) 版本
#创建XML树并写入文件,更好看一点
xml_string = ET.tostring(root, encoding="utf-8",method='xml',short_empty_elements=False).decode('utf-8')
xml_pretty_string = minidom.parseString(xml_string).toprettyxml(indent="  ",encoding="utf-8").decode('utf-8')
with open("cool_output2.xml", "w",encoding="utf-8") as file:
    file.write(xml_pretty_string)

# ET.Element
'''
# 子集追加
# son 
son1 = ET.Element('son',{'name': '儿1'})
son2 = ET.Element('son',{'name': '儿2'})
son2.text="value"

grandson1 = ET.Element('grandson',{'name': '儿11'})


# grandson append to son
son1.append(grandson1)

# son append root
root.append(son1)
'''
# root.makeelement
'''
# 子集追加
# son 
son1 = root.makeelement('son',{'name': '儿1'})
son2 = root.makeelement('son',{'name': '儿2'})
son2.text="value"

# grandson
grandson1 = son1.makeelement('grandson',{'name': '儿11'})
# grandson append to son
son1.append(grandson1)

# son append root
root.append(son1)
'''
# ET.SubElement
'''
# 子集追加

# son 
son1 = ET.SubElement(root,'son',attrib={'name': '儿1'})
son2 = ET.SubElement(root,'son',attrib={'name': '儿2'})
son2.text="value"

# grandson
grandson1 = ET.SubElement(son1,'age',attrib={'name': '儿11'})
grandson1.text = '孙子'

'''
