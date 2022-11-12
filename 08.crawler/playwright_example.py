from playwright.sync_api import Playwright, sync_playwright, expect
import time
import re
import os
from pathlib import Path

def write_html(name,response):
    '''
    response 写入本地文件
    '''
    with open(name+".html",mode='w',encoding='utf-8') as fh:
        fh.write(response.text)
    return 0
    
def GetAllFileNames(pwd):
    '''
    param: str  "pwd"
    return:dirname pathlab_obj
    return:list [ str ]
    #https://zhuanlan.zhihu.com/p/36711862
    #https://www.cnblogs.com/sigai/p/8074329.html
    '''
    files_lst = []
    #字符串路径 工厂化为 pathlib 对象，可使用pathlib 对象的方法(函数)/属性(私有变量)
    target_path = Path(pwd)
    for child in target_path.rglob('*.tsv'):
        if child.is_dir():
            pass
        elif child.is_file():
            #child完整路径,child.relative_to(pwd) 相对于pwd的相对路径，其实就是文件名;可以通过child.name获得
            files_lst.append(child.relative_to(pwd))
            #print(child.relative_to(pwd))
    return files_lst

def download(page,gene_name,tsv_dir,idx):

    # 点击输入
    if idx == 0:
        page.get_by_placeholder("INFO").click()
        page.get_by_placeholder("INFO").fill(gene_name)
        page.get_by_placeholder("INFO").press("Enter")
        page.wait_for_load_state('networkidle')
    else:
        page.get_by_placeholder("INFO2").click()
        page.get_by_placeholder("INFO2").fill(gene_name)
        page.get_by_placeholder("INFO2").press("Enter")
        page.wait_for_load_state('networkidle')
    # 停顿1秒
    page.wait_for_timeout(1000)
    html_str = str(page.content())
    if re.search('not match any document',html_str):
        '''
        html_str = str(page.content())
        通过源码进行判断 not match any document
        '''
        print('nothing1:not match')
        return gene_name
    else:
        page.locator('xpath=//*[@id="mimContent"]/div[1]/div[5]/div[2]/span[1]/a').click()
        page.wait_for_load_state('networkidle')
        # 停顿1秒
        page.wait_for_timeout(1000)
        html_str = page.content()
        # with open("gene.html",mode='w',encoding='utf-8') as fh:
        #     fh.write(html_str)
        if re.search('Table View',html_str):
            page.get_by_role("link", name="Table View").click()
            page.wait_for_load_state('networkidle')
            page.get_by_role("button", name="Download As").click()
            page.wait_for_load_state('networkidle')

            # 停顿0.5秒
            page.wait_for_timeout(500)
            with page.expect_download() as download_info:
                page.get_by_role("link", name="Tab-delimited File").click()
                page.wait_for_load_state('networkidle')
            download = download_info.value
            download.save_as(Path.joinpath(tsv_dir,gene_name+'.tsv'))
            page.wait_for_load_state('networkidle')
            # 停顿0.5秒
            page.wait_for_timeout(500)
            return ''
        else:
            print('nothing2:Table View')
            return gene_name


def read_xxxx_tsv(file_path):
    mim_id = ''
    gene_name = ''
    disease_snp_list = []
    with open(file_path,mode='r',encoding='utf-8') as fh:
        for line in fh:
            if re.match('INFO',line) or  re.match('Downloaded',line) or re.match('Copyright',line) or re.match('Number',line) or re.match('Allelic',line) or re.match('ANKYRIN',line):
                continue
            elif re.match('\d+',line):
                mim_id = line.strip()
                print(mim_id)
            elif line.strip() and re.search('rs\d{3}',line):
                record = re.split('\t',line.strip())
                '''
                Number	Phenotype	Mutation	SNP	gnomAD SNP	ClinVar
                '''
                number = record[0]
                print(record)
                phenotype = record[1]
                dbsnp = record[3]
                ClinVar = record[5]
                target_id = mim_id + number
                tmp_mut = record[2]
                gene_name, Mutation = re.split(', ',tmp_mut,maxsplit=1)
                Mutation = re.sub('\(\S+?\)','',Mutation)
                disease_snp_str = '\t'.join([dbsnp,Mutation,gene_name,target_id,phenotype,ClinVar])
                yield disease_snp_str

def run(playwright: Playwright,tsv_dir,name_list) -> None:
    # playwright.firefox
    # playwright.chromium
    browser = playwright.firefox.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://main.com/")
    page.wait_for_load_state('networkidle')
    page.get_by_role("button", name="Close").click()
    #########################################################
    other_list = []
    for idx in range(len(name_list)):
        gene_name = name_list[idx]
        unverify_name = download(page,gene_name,tsv_dir,idx)
        if unverify_name != '':
            other_list.append(unverify_name)

    ##################################################
    context.close()
    browser.close()

    return other_list

with sync_playwright() as playwright:

    # 跳转脚本所在目录
    pwd = os.path.split(os.path.realpath(__file__))[0]
    pwd = Path(pwd)
    os.chdir(pwd)

    tsv_dir = Path.joinpath(pwd,'tsv')
    tsv_dir.mkdir(parents=True,exist_ok=True)
    
    # 遍历目录获得已经下载过的gene list 
    files_lst = GetAllFileNames(tsv_dir)
    available_gene_set = set([re.sub('\.tsv','', str(x)) for x in files_lst])
    print('available:',available_gene_set)

    # 如果文件存在则读取
    other_old_list = []
    other_gene_id = Path.joinpath(pwd,'other_list.txt') #xxxx无法查询的
    if other_gene_id.exists():
        with open(other_gene_id,mode='r',encoding='utf-8') as fh:
            for line in fh:
                gname = line.strip()
                if gname:
                    other_old_list.append(gname)

    # 获取需要的gene list
    name_set = set()
    with open('gene_input_list.txt',mode='r',encoding='utf-8') as fh:
        for line in fh:
            gene_name = line.strip()
            if gene_name:
                name_set.add(gene_name)
    print('input:',name_set)
    # 剔除已知下载样品
    gene_name_list = list(name_set - available_gene_set - set(other_old_list))
    print('download:',gene_name_list)

    if len(gene_name_list) > 0:
        # 开始下载
        other_new_list = run(playwright,tsv_dir,gene_name_list)

    other_list = other_old_list + other_new_list
    with open('other_list.txt',mode='a',encoding='utf-8') as out:
        for line in other_list:
            out.write(line+'\n')

# 遍历解析结果 合并为一个文件
with open('target_snp.txt',mode='w',encoding='utf-8') as out:
    header_str = 'dbsnp\tMutation\tgene_name\ttarget_id\tphenotype\tClinVar\n'
    out.write(header_str)
    for file_name in files_lst:
        file_path = Path.joinpath(tsv_dir,file_name)
        for disease_snp_str in read_xxxx_tsv(file_path):
            out.write(disease_snp_str+'\n')