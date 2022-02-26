from bs4 import BeautifulSoup
from collections import OrderedDict

def get_id_name(html):
    all_list=[
      'A',
      'B',
      'C',
    ]
    
    soup = BeautifulSoup(html,'lxml')
    value_name_dic = OrderedDict() #{key:value,key:value} #存储 value关键词 以及 标题
  
    for x in all_list:
        # 上级关键词搜索 'class':'col-xs-3 '
        res = soup.find_all(attrs={'class':'col-xs-3 '+x})
        for link in res:
            # input 开头的
            input_element = link.find_all("input",attrs={"type":"checkbox"})
            for each in input_element:
                col_id = each['id'].strip()
                col_name = each["name"].strip()
                value_name_dic[col_name] = col_id
    return value_name_dic
