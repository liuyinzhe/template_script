import requests,re,os
from urllib.request import quote
from lxml import etree
from multiprocessing import Pool
from ffmpy3 import FFmpeg
from prettytable import PrettyTable
order,infors = 1,[]
table = PrettyTable(['序号', 'up主', '标题', '视频时长', '投稿日期', '播放量', '试看链接'])
path='E:\spider_train\\bilibili'
path_='E:\spider_train\\bilibili\m4s'


#python爬虫使用Cookie的两种方法
#https://blog.csdn.net/weixin_38706928/article/details/80376572

# folder=os.path.exists(path)
# if not folder:                #判断是否存在文件夹如果不存在则创建为文件夹
#     os.makedirs(path)
# os.makedirs(path_)
def data(content,page):
    global order,infors
    url='https://search.bilibili.com/all?keyword=%s&from_source=banner_search&page=%d'%(quote(content),page)
    headers={
        'Cookie': '_uuid=4DEBAA6F-D40B-5C01-B2CB-DB466B1D2C0E62289infoc; buvid3=6C6C2324-B32B-4F7F-BB95-13624FC9C88E143093infoc; rpdid=|(JYYRlYRRuu0J'ulmYJ~J~mm; sid=kq21rukq; LIVE_BUVID=AUTO1615975095236996; blackside_state=1; _ga=GA1.2.1650794814.1599307889; CURRENT_FNVAL=80; DedeUserID=52581914; DedeUserID__ckMd5=0afae22c3efc3e5a; SESSDATA=5ccea644,1617980765,d02d3*a1; bili_jct=99cb7e8249be7c3176b6295df1f5f58d; fingerprint3=da4bcdb1040a4fd3d4ba0b80304324c7; fingerprint=c56f8a492111d69a77aead3bb633ad85; buivd_fp=6C6C2324-B32B-4F7F-BB95-13624FC9C88E143093infoc; buvid_fp_plain=6C6C2324-B32B-4F7F-BB95-13624FC9C88E143093infoc; fingerprint_s=29f3b8e716e608a1d49ed852790469ea; Hm_lvt_8a6e55dbd2870f0f5bc9194cddf32a02=1610197619; bp_t_offset_52581914=486413344156968553; bp_video_offset_52581914=486453678191062532; PVID=1; bsource=search_baidu; finger=1571944565'
        'Referer':'https://www.bilibili.com/',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
    }
    if page==1:
        responses=etree.HTML(requests.get(url,headers=headers).content.decode('utf-8')).xpath('//*[@id="all-list"]/div[1]/div[2]/ul[2]/li')
        if responses==[]:
            responses=etree.HTML(requests.get(url,headers=headers).content.decode('utf-8')).xpath('//*[@id="all-list"]/div[1]/div[2]/ul/li')
    else:
        responses=etree.HTML(requests.get(url,headers=headers).content.decode('utf-8')).xpath('//*[@id="all-list"]/div[1]/ul/li')
    for response in responses:
        infors.append([str(order),
                       response.xpath('./div/div[3]/span[4]/a/text()')[0],
                       response.xpath('./div/div[1]/a/@title')[0],
                       response.xpath('./a/div/span[1]/text()')[0],
                       response.xpath('./div/div[3]/span[3]/text()')[0].replace('\n', '').replace(' ', ''),
                       response.xpath('./div/div[3]/span[1]/text()')[0].replace('\n','').replace(' ',''),
                       'https:'+response.xpath('./div/div[1]/a/@href')[0].split('?')[0]])
        order+=1
def make(content,page):
    global table,infors
    for i in range(1, page+1):
        data(content, i)
    for i in infors:
        table.add_row(i)
    print(table)
    number=input('输入要下载的视频序号：').split('.')
    return [infors[int(i)-1][-1] for i in number]
def download(url):
    global path
    hv={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
    response=requests.get(url,headers=hv).content.decode('utf-8')
    print(url)
    urls1=re.findall('"baseUrl":"(.+?)"',response)
    urls2=re.findall('"url":"(.+?)"',response)
    headers={
        'Referer':url,
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
        'Range':'bytes=0-'
    }
    if urls1!=[]:
        print(url.split('/')[-1] + '开始下载!')
        with open(path_+'\%s.mp4'%(url.split('/')[-1]),'wb')as f:
            f.write(requests.get( urls1[0],headers=headers).content)
        with open(path_+'\%s.mp3'%(url.split('/')[-1]),'wb')as f:
            f.write(requests.get(urls1[-1],headers=headers).content)
        ff = FFmpeg(inputs={path_+'\%s.mp4'%(url.split('/')[-1]): None, path_+'\%s.mp3' % (url.split('/')[-1]): None},
                    outputs={path+'\%s.mp4'%(url.split('av')[-1]): '-c:v h264 -c:a ac3'})
        ff.run()
        print(url.split('/')[-1]+'下载完成!')
    else:
        print(url.split('/')[-1] + '开始下载!')
        with open(path+'\%s.flv'%(url.split('/')[-1]),'wb')as f:
            f.write(requests.get (urls2[0],headers=headers).content)
        print(url.split('/')[-1] + '下载完成!')
def start(content,page):
    urls=make(content,page)
    pool=Pool(processes=4)
    pool.map(download,urls)


if __name__ == '__main__':
    content=input('输入内容：')
    start(content,3)