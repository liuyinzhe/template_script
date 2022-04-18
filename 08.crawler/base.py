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


async def async_donwload(cookies,child_jobs_list,idx,sem):
    async with httpx.AsyncClient(http2=True,verify=False,cookies=cookies) as client:
        async with sem:
            # session方法,cookies 持久化
            timeout = httpx.Timeout(36000.0, connect=360.0)
            sizeInBytes,file_type,url,outfile = child_jobs_list
            print(outfile,'running')
            #response = await client.get(url,timeout=timeout) 
            if outfile.endswith(".gz"):
                out = gzip.open(outfile,mode='wb')
            else:
                out = open(outfile,mode='wb')
            response_size = 0
            #Streaming responses#www.python-httpx.org/compatibility/
            async with client.stream('GET', url,timeout=timeout) as response:
                status_code = response.status_code
                #if "The server didn't respond in time." in response.text:
                #    async_donwload(cookies,b_jobs_list,idx,sem)
                if status_code != 200:
                    return idx,status_code
                async for chunk in response.aiter_bytes():
                    response_size += len(chunk)
                    out.write(chunk)
            out.close()
            if response_size != sizeInBytes:
                 print(outfile,'000')
                 return idx,000
    return idx,status_code

async def Coroutine_run(cookies,all_jobs_list,sem):
    coroutine_task_list = []
    for idx,child_jobs_list in all_jobs_list: # split_num
        # all_count 爬取所有样品结果的数量
        # 
        # # python >3.7
        # task = asyncio.create_task(async_donwload(client,b_jobs_list,idx,sem))
        # python 3.6.8
        # 检查文件是否存在
        task = asyncio.ensure_future(async_donwload(cookies,child_jobs_list,idx,sem))
        coroutine_task_list.append(task)
    return await asyncio.gather(*coroutine_task_list)

def main():
        user = 'abc'
        pwd = '123'
        timeout = httpx.Timeout(36000.0, connect=360.0)
        sem = asyncio.Semaphore(concurrent_number) #同时运行的协程数量 https://www.cnblogs.com/kcxg/p/15107785.html
        client = httpx.Client(http2=True,verify=False)
        client=jgi_login(client,user,pwd,timeout)
        cookies = client.cookies
        all_jobs_list = []
        sem = 
        # Coroutine
        # ref:https://www.cnblogs.com/kcxg/p/15107785.html
        # ref:https://www.jianshu.com/p/b5e347b3a17c
        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(Coroutine_run(cookies,all_jobs_list,sem))
        client.close()
