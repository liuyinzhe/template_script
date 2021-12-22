import httpx
import asyncio

from bs4 import BeautifulSoup
#from lxml import etree

#https://curlconverter.com/
#https://reqbin.com/curl


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
