import httpx
import asyncio

from bs4 import BeautifulSoup
#from lxml import etree


#https://curlconverter.com/
#https://reqbin.com/curl

#todo:
#JA3

def get_token(html):
    '''
    from bs4 import BeautifulSoup
    https://cuiqingcai.com/1319.html
    筛选提取页面的html内容
    :param html:
    第一次访问网页存在隐藏项目authenticity_token
    '''
    soup = BeautifulSoup(html,'lxml')
    res = soup.find("input",attrs={"name":"authenticity_token"})
    token = res["value"]
    return token


def construction_multipart_encoded_str (new_list_tuple,boundary_str):
    '''
    format_str = construction_multipart_encoded_str(a_list+b_list,'--'+boundary_str)
    #boundary_str
    ------WebKitFormBoundaryhTmOInhA14nYnzK0
    #分隔符：--
    #单个内容结构
    ----WebKitFormBoundaryGtgXulVY19zxw4Ub\r\nContent-Disposition: form-data; name="domain"\r\n\r\n*Microbiome\r\n
    '''
    new_list=[]
    start=''
    new_list.append(start)
    for name,value in new_list_tuple:
        new_str= '''\r\nContent-Disposition: form-data; name="{}"\r\n\r\n{}\r\n'''.format(name.strip(),value.strip())
        new_list.append(new_str)
    end_str=''
    new_list.append(end_str)
    final_str = boundary_str.join(new_list)+'--\r\n'
    return final_str
