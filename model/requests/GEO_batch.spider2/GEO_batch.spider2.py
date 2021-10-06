"""
利用python爬取并翻译GEO数据库
"""
#XXXXX
"""
python包安装
file -> setting -> project interpreter -> 点击右侧+号 -> 输入包名 -> 点击包 -> 左下角install
"""
import os 
import re
import urllib.request
import urllib.parse
import time
import requests
import random
import copy
import urllib






def spider(id):

    header={'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'max-age=0',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}

    #pro = ['112.95.22.8','222.249.238.138','112.237.68.133','222.95.144.243','61.153.251.150','220.173.106.168','123.15.24.200','211.147.226.4','	122.224.65.198','222.85.28.130','119.131.88.20','103.10.86.203','182.92.242.11','183.167.217.152']
    #html_src = requests.post(url='https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=' + id, proxies={'http': random.choice(pro)}, headers = header,timeout=60).text
    html_src = requests.post(url='https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=' + id, headers = header,timeout=60).text

    regexp = re.compile(r"<td style=\"text-align: justify\">Gender: (\D+?)<br>Age: (\S+?)<br>Tissue: (\D+?)<br>Disease state: (\D+?)<br>Individual: (\S+?)<br>Clinical info: Submitting diagnosis: (\D+?)<br>Clinical info: Final microarray diagnosis: (\D+?)<br>Clinical info: Follow up status: (\D+?)<br>Clinical info: Follow up years: (\S+?)<br>Clinical info: Chemotherapy: (\D+?)<br>Clinical info: ECOG performance status: (\S+?)<br>Clinical info: Stage: (\S+?)<br>Clinical info: LDH ratio: (\S+?)<br>Clinical info: Number of extranodal sites: (\S+?)<br></td>",re.I)
    result=re.search(regexp, html_src)

    Gender = result.group(1).strip()
    Age = result.group(2).strip()
    Tissue = result.group(3).strip()
    Disease_state = result.group(4).strip()
    Individual = result.group(5).strip()
    Submitting_diagnosis = result.group(6).strip()
    Final_microarray_diagnosis = result.group(7).strip()
    Follow_up_status = result.group(8).strip()
    Follow_up_years = result.group(9).strip()
    Chemotherapy = result.group(10).strip()
    ECOG_performance_status= result.group(11).strip()
    Stage = result.group(12).strip()
    LDH_ratio = result.group(13).strip()
    Number_of_extranodal_sites = result.group(14).strip()

    result = (id,Gender,Age,Tissue,Disease_state,Individual,Submitting_diagnosis,Final_microarray_diagnosis,Follow_up_status,Follow_up_years,Chemotherapy,ECOG_performance_status,Stage,LDH_ratio,Number_of_extranodal_sites)
    tmp = open("tmp.xls",'a')
    tmp.write('\t'.join(result)+"\n")
    tmp.close()
    return result


if __name__ == '__main__':
    os.chdir("C:\\Users\\Family\\Desktop\\pachong\\new_20201231")
    # 文件名
    list_fh = 'list2.txt'
    id_list = []
    with open(list_fh,'r',encoding='utf-8') as fh:
        for line in fh:
            records = re.split("\s",line.strip())
            id_list.append(records[0])
    
    #print(id_list)
    all_list = []
    header=["Id","Gender","Age","Tissue","Disease_state","Individual","Submitting_diagnosis","Final_microarray_diagnosis","Follow_up_status","Follow_up_years","Chemotherapy","ECOG_performance_status","Stage","LDH_ratio","Number_of_extranodal_sites"]
    #all_list.append(header)
    id_list_back=copy.deepcopy(id_list)
    all = False
    while all == False:
        id_list = copy.deepcopy(id_list_back)
        all = True
        count=0
        second= [1,1,2,2,3,3,3,4,5,6]
        for id in id_list:
            try:
                print('正在爬取：' + id + '，进度：'+ str( count + 1) + ' / '  + str(len(id_list_back)) + ' 个id' )
                result = spider(id)
                all_list.append(result)
                count = count + 1
                t = random.choice(second)
                print(id+' 完成,sleep '+str(t)+"秒")
                time.sleep(t)
                id_list_back.remove(id)
            except:
                print('爬取超时，跳过本id')
                all = False
    all_list_sorted = sorted(all_list, key=lambda x:x[0], reverse=False)
    #print('\t'.join(header))
    tmp = [header,]
    all_list_sorted = tmp + all_list_sorted
    all_zip_result = zip(*all_list_sorted)
    #print(list(all_zip_result))
    with open("result.xls",'w') as fh:
        for x in list(all_zip_result):
            fh.write('\t'.join(x)+"\n")
