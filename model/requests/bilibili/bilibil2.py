import os
import requests
import re
import pprint
import json
import subprocess


headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
           'cooike':r"_uuid=4DEBAA6F-D40B-5C01-B2CB-DB466B1D2C0E62289infoc; buvid3=6C6C2324-B32B-4F7F-BB95-13624FC9C88E143093infoc; rpdid=|(JYYRlYRRuu0J'ulmYJ~J~mm; LIVE_BUVID=AUTO1615975095236996; blackside_state=1; _ga=GA1.2.1650794814.1599307889; CURRENT_FNVAL=80; fingerprint3=da4bcdb1040a4fd3d4ba0b80304324c7; buivd_fp=6C6C2324-B32B-4F7F-BB95-13624FC9C88E143093infoc; buvid_fp_plain=6C6C2324-B32B-4F7F-BB95-13624FC9C88E143093infoc; buvid_fp=6C6C2324-B32B-4F7F-BB95-13624FC9C88E143093infoc; fingerprint_s=83e7450440c3e03b1e278d6fc2490cac; bsource=search_baidu; bp_video_offset_52581914=519735736247684563; fingerprint=b7f9aaf77389071e94dc6ebccc647a24; SESSDATA=2f37db7d,1635520023,e5e20*51; bili_jct=4597ac1211aa2eec25383e382be87a8d; DedeUserID=52581914; DedeUserID__ckMd5=0afae22c3efc3e5a; sid=abshz0fv; PVID=2; bfe_id=1e33d9ad1cb29251013800c68af42315"
          }


headers_1 = {
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.9",
    "access-control-request-method": "GET",
    "cache-control": "no-cache",
    "origin": "https://www.bilibili.com",
    "pragma": "no-cache",
    "referer": "https://www.bilibili.com/",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "cross-site",
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
    "cooike":r"_uuid=4DEBAA6F-D40B-5C01-B2CB-DB466B1D2C0E62289infoc; buvid3=6C6C2324-B32B-4F7F-BB95-13624FC9C88E143093infoc; rpdid=|(JYYRlYRRuu0J'ulmYJ~J~mm; LIVE_BUVID=AUTO1615975095236996; blackside_state=1; _ga=GA1.2.1650794814.1599307889; CURRENT_FNVAL=80; fingerprint3=da4bcdb1040a4fd3d4ba0b80304324c7; buivd_fp=6C6C2324-B32B-4F7F-BB95-13624FC9C88E143093infoc; buvid_fp_plain=6C6C2324-B32B-4F7F-BB95-13624FC9C88E143093infoc; buvid_fp=6C6C2324-B32B-4F7F-BB95-13624FC9C88E143093infoc; fingerprint_s=83e7450440c3e03b1e278d6fc2490cac; bsource=search_baidu; bp_video_offset_52581914=519735736247684563; fingerprint=b7f9aaf77389071e94dc6ebccc647a24; SESSDATA=2f37db7d,1635520023,e5e20*51; bili_jct=4597ac1211aa2eec25383e382be87a8d; DedeUserID=52581914; DedeUserID__ckMd5=0afae22c3efc3e5a; sid=abshz0fv; PVID=2; bfe_id=1e33d9ad1cb29251013800c68af42315"
}
headers_2 = {
    "accept": "*/*",
    "accept-encoding": "identity",
    "accept-language": "zh-CN,zh;q=0.9",
    "cache-control": "no-cache",
    "dnt": "1",
    "origin": "https://www.bilibili.com",
    "pragma": "no-cache",
    "referer": "https://www.bilibili.com/",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "cross-site",
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
    "cooike":r"_uuid=4DEBAA6F-D40B-5C01-B2CB-DB466B1D2C0E62289infoc; buvid3=6C6C2324-B32B-4F7F-BB95-13624FC9C88E143093infoc; rpdid=|(JYYRlYRRuu0J'ulmYJ~J~mm; LIVE_BUVID=AUTO1615975095236996; blackside_state=1; _ga=GA1.2.1650794814.1599307889; CURRENT_FNVAL=80; fingerprint3=da4bcdb1040a4fd3d4ba0b80304324c7; buivd_fp=6C6C2324-B32B-4F7F-BB95-13624FC9C88E143093infoc; buvid_fp_plain=6C6C2324-B32B-4F7F-BB95-13624FC9C88E143093infoc; buvid_fp=6C6C2324-B32B-4F7F-BB95-13624FC9C88E143093infoc; fingerprint_s=83e7450440c3e03b1e278d6fc2490cac; bsource=search_baidu; bp_video_offset_52581914=519735736247684563; fingerprint=b7f9aaf77389071e94dc6ebccc647a24; SESSDATA=2f37db7d,1635520023,e5e20*51; bili_jct=4597ac1211aa2eec25383e382be87a8d; DedeUserID=52581914; DedeUserID__ckMd5=0afae22c3efc3e5a; sid=abshz0fv; PVID=2; bfe_id=1e33d9ad1cb29251013800c68af42315"
}

def send_requests(url):
    '''请求数据'''
    session = requests.session()
    session.options(url,headers = headers_1)
    response = session.get(url=url,headers = headers_2)
    
    #response = requests.get(url=url,headers=headers)
    return response

def get_video_data(html_data):
    """解释视频数据"""
    #提取视频的标题
    '''
    <span class="tit">python爬虫-爬取B站视频，原来爬取B站视频只要有了这个就可以了。</span>
    '''
    title=re.findall('<span class="tit">(.+?)</span>',html_data)[0]
    #re.search('<span class="tit">(.+?)</span>',html_data)
    print('视频标题：',title)
    json_data=re.findall('<script>window\.__playinfo__=(.+?)</script>',html_data)[0]
    #pprint.pprint(json_data) 
    #print(json_data)
    
    json_data_dic = json.loads(json_data) 
    pprint.pprint(json_data_dic) 

    # 提取 音频的 url 地址
    audio_url = json_data_dic['data']['dash']['audio'][0]['backupUrl'][0]
    print("解析到的音频地址：",audio_url)

    # 提取视频 画面的url 地址
    video_url = json_data_dic['data']['dash']['video'][0]['backupUrl'][0]
    print("解析到的视频地址：",video_url)

    video_data = [title,audio_url,video_url]
    return video_data

def save_data(file_name, audio_url,video_url):
    # 请求数据
    print('正在请求音频数据')
    audio_data = send_requests(audio_url).content #二进制音频
    print('正在请求视频数据')
    video_data = send_requests(video_url).content #二进制音频

    print('正在保存音频数据')
    with open(file_name + '.mp3',mode='wb') as f:
        f.write(audio_data)
    
    print('正在保存视频数据')
    with open(file_name + '.mp4',mode='wb') as f:
        f.write(video_data)
    

def  merge_data(video_name):
    """数据合并"""
    print('视频合成开始：',video_name)
    #ffmpeg -i video.mp4 -i audio.wav -c:v copy  -c:a acc -strict experimental output.map4
    CONMMAND = 'ffmpeg -i {video_name}.mp4 -i {video_name}.mp3 -c:v copy  -c:a acc  -strict experimental output.mp4'
    subprocess.Popen(CONMMAND, shell=True)
    print('视频合成结束：',video_name)

   

def main():
    #执行目录修改
    os.chdir(r'E:\spider_train\bilibili')

    #session_class_obj = requests.session()
    #response = session_class_obj.get(r'https://space.bilibili.com/279942172')
    #pprint.pprint(response.cookies.get_dict())

    html_data = send_requests('https://www.bilibili.com/video/BV1Fy4y1D7XS').text
    print(html_data)
    video_data = get_video_data(html_data)

    save_data(video_data[0],video_data[1],video_data[2]) #file_name, audio_url,video_url
    #merge_data(video_data[0])
if __name__=='__main__':
    main()

