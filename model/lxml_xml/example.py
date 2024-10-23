from lxml import etree
from xml.etree import ElementTree as ET
from xml.dom import minidom

# ET  去打开xml 文件
tree = ET.parse("1571990288_f_v3.xml")

# 获得根标签
root = tree.getroot()

print(root) # <Element 'flash_show_info' at 0x000001E362F531A0>


############################
content = '''
<data>
    <country  name= "county_name" id="999">
        <rank updated="yes"> 2</rank>
    </country>
    <country  name= "county_name2">
        <rank>22</rank>
    </country>
</data>
'''
root = ET.XML(content)
#print(root) # <Element 'data' at 0x0000024F1B7231A0>

# 获得 child 标签
for child in root:
    # child.tag = country
    # child.attrib = {"name":"county_name"}
    #print(child.tag,child.attrib)
    for node in child:
        pass
        #print(node.tag,node.attrib,node.text)
'''
country {'name': 'county_name'}
rank {'updated': 'yes'}  2
country {'name': 'county_name2'}
rank {} 22
'''

###############################
country_object = root.find("country") 
print(country_object.tag,country_object.attrib)
# country {'name': 'county_name', 'id': '999'}



#######################################################
for child in root.iter('rank'):
    print(child.tag,child.text)
'''
rank  2
rank 22
'''

v1 = root.findall("country")
print(v1)
'''
[<Element 'country' at 0x000001AEEE583420>, <Element 'country' at 0x000001AEEE5834C0>]
'''

v2 = root.find("country").find('rank')
print(v2)
'''
<Element 'rank' at 0x000001FB32D77470>
'''

#########################  删改  ##############################

from xml.etree import ElementTree as ET

content = '''
<data>
    <country  name= "county_name" id="999">
        <rank updated="yes"> 2</rank>
    </country>
    <country  name= "county_name2">
        <rank>22</rank>
    </country>
</data>
'''

root = ET.XML(content)

# 修改 节点内容 和属性
rank = root.find('country').find('rank')
print(rank.text)
rank.text = "999" # 只能是字符串
rank.set("updata","2024-10-10")
print(rank.text,rank.attrib)

###############   保存文件
tree = ET.ElementTree(root)
tree.write('new.xml',encoding='utf-8')


############### 删除
root.remove(root.find('country')) # 找到第一个标签，删除
print(root.findall("country"))

################################################   从头构建文档   #################################################
'''
<home>
    <son name="儿1">
        <grandson name="儿11"></grandson>
        <grandson name="儿12"></grandson>
    </son>
    <son name="儿2"></son>
</home>
'''

from xml.etree import ElementTree as ET

# 创建根标签
root = ET.Element("home")

# son 
son1 = ET.Element('son',{'name': '儿1'})
son2 = ET.Element('son',{'name': '儿2'})
son2.text="value"

# grandson
grandson1 = ET.Element('grandson',{'name': '儿11'})
grandson2 = ET.Element('grandson',{'name': '儿12'})

# grandson append to son
son1.append(grandson1)
son2.append(grandson2)
# son append root
root.append(son1)
root.append(son2)

tree = ET.ElementTree(root)
tree.write('cool.xml',encoding='utf-8',short_empty_elements=False)


#创建XML树并写入文件,更好看一点
xml_string = ET.tostring(root, encoding="utf-8",method='xml').decode('utf-8')
xml_pretty_string = minidom.parseString(xml_string).toprettyxml(indent="  ",encoding="utf-8").decode('utf-8')
with open("cool_output.xml", "w",encoding="utf-8") as file:
    file.write(xml_pretty_string)

################################ makeelement

from xml.etree import ElementTree as ET

# 创建根节点
root = ET.Element("famliy")

# son 
son1 = root.makeelement('son',{'name': '儿1'})
son2 = root.makeelement('son',{'name': '儿2'})
son2.text="value"

# grandson
grandson1 = son1.makeelement('grandson',{'name': '儿11'})
grandson2 = son2.makeelement('grandson',{'name': '儿12'})

# grandson append to son
son1.append(grandson1)
son2.append(grandson2)

# son append root
root.append(son1)
root.append(son2)

tree = ET.ElementTree(root)
tree.write('cool.xml',encoding='utf-8',short_empty_elements=False)

#################################### SubElement

from xml.etree import ElementTree as ET

# 创建根节点
root = ET.Element("famliy")

# son 
son1 = ET.SubElement(root,'son',attrib={'name': '儿1'})
son2 = ET.SubElement(root,'son',attrib={'name': '儿2'})
son2.text="value"

# grandson
grandson1 = ET.SubElement(son1,'age',attrib={'name': '儿11'})
grandson1.text = '孙子'

et = ET.ElementTree(root)
et.write('test.xml',encoding='utf-8')

#################################### 额外信息

from xml.etree import ElementTree as ET

# 创建根节点
root = ET.Element("user")
root.text = "<![CDATA{你好呀}]"


et = ET.ElementTree(root)
et.write('test.xml',encoding='utf-8')


################################################################### 解析为字典

from xml.etree import ElementTree as ET

info = {}
root = ET.XML(content)
for node in root:
    # print(node.tag,node.text)
    info[node.tag] = node.text

print(info)
