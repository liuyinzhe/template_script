import os,sys,re
import requests
import argparse
from pathlib import Path
from playwright.sync_api import Playwright, sync_playwright
from lxml import etree
from bs4 import BeautifulSoup,element
from collections import OrderedDict
from docx import Document

#https://blog.csdn.net/zjkpy_5/article/details/122418811
# https://zhuanlan.zhihu.com/p/405927510
# https://zhuanlan.zhihu.com/p/405927800
# https://zhuanlan.zhihu.com/p/347213089

# https://zhuanlan.zhihu.com/p/405936849
# 监听 https://www.diandian100.cn/c4007c36.html

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
    for child in target_path.rglob('*.docx'):
        if child.is_dir():
            pass
        elif child.is_file():
            #child完整路径,child.relative_to(pwd) 相对于pwd的相对路径，其实就是文件名;可以通过child.name获得
            files_lst.append(child.relative_to(pwd))
            #print(child.relative_to(pwd))
    return files_lst

def read_docx(seq_id,doc_file):
    doc = Document(str(doc_file))
    original_flag = False
    dna_seq = ''
    GC_perc = ''
    Length = ''
    #每一段的内容
    flag = False
    for para in doc.paragraphs:
        line = str(para.text).strip()
        if 'original' in line:
            original_flag = True
            #print(line)
        elif 'GC%' in line:
            record = re.split('\s',line)
            # A_count = record[1]
            # T_count = record[3]
            # C_count = record[5]
            # G_count = record[7]
            GC_perc = record[10]
            Length = record[13]
            #print(line)
        elif 'OP' in line:
            flag = True
            #print(line)
        elif flag and original_flag and re.match('^[ATGC]+$',line.strip()):
            dna_seq=line.strip()
            #print(line)
            break
    return [seq_id,GC_perc,Length,dna_seq]

def get_RestrictionEnzymeName_id(html):
    all_list=[
    "Target_A",
    "Target_B",
    "Target_C",
    "Target_D",
    "Target_E",
    "Target_F",
    "Target_H",
    "Target_K",
    "Target_M",
    "Target_N",
    "Target_P",
    "Target_R",
    "Target_S",
    "Target_T",
    "Target_X",
    "Target_Z",
    ]
    
    soup = BeautifulSoup(html,'lxml')
    value_name_dic = OrderedDict() #{key:value,key:value} #存储 value关键词 以及 标题
  
    for x in all_list:
        res = soup.find_all(attrs={'class':'col-xs-3 '+x})
        for link in res:
            # input
            input_element = link.find_all("input",attrs={"type":"checkbox"})
            for each in input_element:
                col_id = each['id'].strip()
                col_name = each["name"].strip()
                value_name_dic[col_name] = col_id
    return value_name_dic

def get_host_info(html):

    ECS_dic = OrderedDict()
    html = etree.HTML(html)
    for idx in range(2,26):
        html_data = html.xpath('//*[@id="ECS"]/option[{}]'.format(idx))
        #print(html_data[0].text,html_data[0].attrib['value'])
        ECS_dic[html_data[0].text] = html_data[0].attrib['value']
    return ECS_dic

def get_verification_code(html_string):
    html = etree.HTML(html_string)
    html_match = html.xpath('//*[@id="LIEC"]/text()')
    first_match = html_match[0]
    #print(first_match)
    #print(type(first_match))
    pattern = re.compile(r"：(\S+?)。")
    result = pattern.search(str(first_match))
    return str(result.group(1))

def on_response(response):
    if response.status == 200:
        print(response.json())

def run_submit(playwright: Playwright,seq_dic: OrderedDict,flags_seq_type: str,flags_ECS: str,RestrictionEnzyme_list: list,outfile: Path,progress_record: Path,headless:bool) -> None:
    browser = playwright.chromium.launch(headless=headless,slow_mo=3000)
    context = browser.new_context()

    # Open new page
    page = context.new_page()
    page.set_default_timeout(360000)
    page.goto("https://xx.com/XO")

    # Click [placeholder="email"]
    page.locator("[placeholder=\"email\"]").click()

    # Fill [placeholder="email"]
    page.locator("[placeholder=\"email\"]").fill("xxx@yyy.com")

    # Click [placeholder="passwd"]
    page.locator("[placeholder=\"passwd\"]").click()

    # Fill [placeholder="passwd"]
    page.locator("[placeholder=\"passwd\"]").fill("12345678")

    # Click #UserPass >> text=login
    page.locator("#UserPass >> text=login").click()


    page.goto("https://xx.com")
    

    page.locator(".gwz-thumb-img.img-css").click()
    # # assert page.url == "https://xxx.com"

    #verification_code_list =[]
    for  seq_name in seq_dic:
        # Select 序列类型
        page.locator("select[name=\"SequenceType\"]").select_option(flags_seq_type)

        # Click input[name="SequenceName"] 序列名称
        page.locator("input[name=\"SequenceName\"]").click()
        # Fill input[name="SequenceName"]
        page.locator("input[name=\"SequenceName\"]").fill(seq_name)

        # Click textarea[name="Sequence"] 填入序列
        page.locator("textarea[name=\"Sequence\"]").click()
        # Fill textarea[name="Sequence"]
        page.locator("textarea[name=\"Sequence\"]").fill(seq_dic[seq_name])

        # Select 选择表达宿主
        page.locator("select[name=\"EV\"]").select_option(flags_ECS)

        # 选择限制性内切酶 酶切位点排除
        for RestrictionEnzyme in RestrictionEnzyme_list:
            First_letter = RestrictionEnzyme[0]
            #选择开始字母
            page.locator("form[role=\"form\"] a:has-text(\""+First_letter+"\")").click()
            #点在 复选框上
            page.locator("text="+RestrictionEnzyme+" >> input[type=\"checkbox\"]").check()
            # 点在文本上
            #page.locator("text=BsaBI").click()

        #开监控
        page.on("response", on_response)

        page.locator("#gs").click()
        html_str = str(page.content())
        verification_code = get_verification_code(html_str)
        
        #修改为 追加模式,完成一个写入一个
        with open(outfile,mode='a',encoding='utf-8') as out,open(progress_record,mode='a',encoding='utf-8') as record_fh:
            out.write('\t'.join([seq_name,verification_code])+'\n')
            record_fh.write(seq_name+'\n')

        #verification_code_list.append([seq_name,verification_code])
        # wait for 3 second
        page.wait_for_timeout(3000)

        # Click 定位点击需求返回内容
        page.locator("text=需求确认").click()

        # sometime later...
        page.remove_listener("response", on_response)

        # 刷新页面新的循环
        page.goto("https://xx.com/COS")
    
    # Close page
    page.close()

    # ---------------------
    context.close()
    browser.close()


def run_download(playwright: Playwright,data_id_dic: dict,tmp_dir: Path,download_progress_record: Path,headless:bool) -> None:
    browser = playwright.chromium.launch(headless=headless,slow_mo=3000)
    context = browser.new_context()

    # Open new page
    page = context.new_page()
    page.set_default_timeout(360000)
    page.goto("https://xx.com/ROC")

    # Click [placeholder="email"]
    page.locator("[placeholder=\"email\"]").click()

    # Fill [placeholder="email"]
    page.locator("[placeholder=\"email\"]").fill("xx@yyy.com")

    # Click [placeholder="passwd"]
    page.locator("[placeholder=\"passwd\"]").click()

    # Fill [placeholder="passwd"]
    page.locator("[placeholder=\"passwd\"]").fill("123456")

    page.locator("#UserPass >> text=login").click()
    # assert page.url == "https://xx.com"

    page.goto("https://xx.com/RS")
    
    page.locator(".gwz-thumb-img.img-xs").click()
    # # assert page.url == "https://xx.com"
    
    for seq_id in data_id_dic:
        docx_name=Path("\\").joinpath(tmp_dir,seq_id+'.docx')
        ID = data_id_dic[seq_id]
        
        # wait for 3 second
        page.wait_for_timeout(3000)
        

        page.locator("text=result").click()

        # Click input[name="ID"]
        page.locator("input[name=\"ID\"]").click()

        # Fill input[name="ID"]
        page.locator("input[name=\"ID\"]").fill(ID)

        # Click text=调取结果
        with page.expect_download() as download_info:
            page.locator("text=调取结果").click()
        download = download_info.value
        download.save_as(docx_name)

        # wait for 3 second
        page.wait_for_timeout(3000)
        
        # 修改为 追加模式,完成一个写入一个
        with open(download_progress_record,mode='a',encoding='utf-8') as record_fh:
            record_fh.write(seq_id+'\n')

        # 刷新页面新的循环
        page.goto("https://xx.com/CTS")
        
    # 循环结束

    # Close page
    page.close()

    # ---------------------
    context.close()
    browser.close()

def get_para():
    desc = '''
    Program For Batch CCX

    '''
 
    parser = argparse.ArgumentParser(description=desc)
 
    subparsers = parser.add_subparsers(dest='command', help='sub-command help')
    parser_list = subparsers.add_parser('list', help=' Get a list of available information ')
    parser_chose = subparsers.add_parser('list', help=' CCX ')
    parser_download = subparsers.add_parser('download', help=' CCX ')

    # chose
    parser_chose.add_argument('-l','--headless', action='store_true', default=False,
                               help=" headless browser;default: [%(default)s]")
    parser_chose.add_argument('-it','--input_table', default='template.txt',
                               help=" input table(format) default: [%(default)s] \ntwo col(sep='\t'):name\tdna(prot)Seq;exampel:\r\nabc\tMYKKD\r\nabc2\tMRYKD\r\n")
 
    parser_chose.add_argument('-if','--input_fasta',
                              help=" input file(fasta format) ")

    parser_chose.add_argument('-r','--RI', default='A;C;F',
                              help=" RW;default: [%(default)s] ")

    parser_chose.add_argument('-e','--EH', default='EC',
                              help=" EH;default: [%(default)s] ")

    parser_chose.add_argument('-p','--prefix', default='CC',
                              help=' prefile of out file; default: [%(default)s] "')
    parser_chose.add_argument('-o','--outdir', default=Path.cwd(),
                              help=' output directory ;default: current working directory. ')
    #https://blog.csdn.net/weixin_40446557/article/details/89472929
    #nargs='*' 　　　表示参数可设置零个或多个
    #nargs=' '+' 　　表示参数可设置一个或多个
    #nargs='?'　　　表示参数可设置零个或一个
    #
    
    # download
    # seq_name
    parser_download.add_argument('-i','--input_table', default='id.xls',
                               help=" input table(txt); default: [%(default)s]")
    parser_download.add_argument('-o','--outdir', default=Path.cwd(),
                              help=' output directory ;default: current working directory. ')
    parser_download.add_argument('-r','--result_name', default='result.xls',
                              help=' name of out file; default: [%(default)s] "')
    parser_download.add_argument('-l','--headless', action='store_true', default=False,
                               help=" headless browser;default: [%(default)s]")
    
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit()
 
    args = parser.parse_args()
 
    if args.command == 'chose' and len(sys.argv) == 2:
        parser_chose.print_help()
        sys.exit()
    if args.command == 'download' and len(sys.argv) == 2:
        parser_download.print_help()
        sys.exit()
    return args


def main():
    args = get_para()
    action = args.command
    headers = {
        'authority': 'xx.com',
        'cache-control': 'max-age=0',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'upgrade-insecure-requests': '1',
        'origin': 'https://xx.com',
        'content-type': 'application/x-www-form-urlencoded',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://xx.com/RL',
        'accept-language': 'zh-CN,zh;q=0.9'}

    #访问页面
    response = requests.get('https://xx.com/target', headers=headers)
    ECS_dic= get_host_info(response.text)
    RestrictionEnzyme_dic = get_RestrictionEnzymeName_id(response.text)
    if action == 'list':
        with open('available_information.txt',mode='w',encoding='utf-8') as out:
            out.write("ECS:\n")
            print("ECS:\n")
            for ECS in ECS_dic:
                print('\t'+ECS)
                out.write('\t'+ECS+'\n')
            print("\n\n",end="")
            out.write('\n\n')

            print('name:\n')
            out.write('name:\n')
            count =1 
            for RestrictionEnzyme in RestrictionEnzyme_dic:
                
                if count % 5 ==0:
                    print('\t'+RestrictionEnzyme)
                    out.write('\t'+RestrictionEnzyme+'\n')
                else:
                    print('\t'+RestrictionEnzyme, end="")
                    out.write('\t'+RestrictionEnzyme)
            print("\n\n")
            out.write('\n\n')
    #爬取
    elif action == 'chose':
        headless = args.headless
        input_table = args.input_table
        input_fasta = args.input_fasta
        prefix = args.prefix
        outdir = args.outdir
        RestrictionEnzyme_str = args.RE
        ECS = args.EH
        outfile = Path('/').joinpath(outdir,prefix+'.id.xls')
        if input_table:
            print('input_table:\t'+input_table)
        elif input_fasta:
            print('input_fasta:\t'+input_fasta)
        print('prefix:\t\t'+prefix)
        print('RW_str:\t'+RestrictionEnzyme_str)
        print('ECS:\t'+ECS)
        print('outfile:\t\t'+str(outfile))
        RE_name_list = re.split(';',RestrictionEnzyme_str.strip())
        flags_check = 0
        RestrictionEnzyme_list = []
        for RestrictionEnzyme in RE_name_list:
            if RestrictionEnzyme in RestrictionEnzyme_dic:
                #RE_idx = RestrictionEnzyme_dic[RestrictionEnzyme]
                RestrictionEnzyme_list.append(RestrictionEnzyme)
            else:
                print('The name '+RestrictionEnzyme+' does not exist, please check the list')
                flags_check = 1
        
        flags_ECS = ECS_dic[ECS]
        
        #progress_record
        #总是追加写入
        #进度文件检查是否存在
        #不存在，就覆盖写
        #存在读取id
        progress_record_lst =[]
        progress_record = Path("\\").joinpath(outdir,'progress_record')
        
        if progress_record.exists():
            with open(progress_record,mode='r',encoding='utf-8') as fh:
                for line in fh:
                    seq_id = line.strip()
                    if seq_id:
                        progress_record_lst.append(seq_id)

            
        seq_dic = OrderedDict()
        name=''
        if input_fasta:
            #print("#"+input_fasta+"#")
            with open(input_fasta,mode='r',encoding='utf-8') as fh:
                for line in fh:
                    if line.startswith('>'):
                        name = re.sub('>','',line.strip())
                        name = list(re.split('\s+?',name))[0]
                        seq_dic[name] = ''
                    else:
                        seq_dic[name] += line.strip()
        elif input_table:
            with open(input_table,mode='r',encoding='utf-8') as fh:
                for line in fh:
                    record = re.split('\t',line.strip())
                    name = record[0].strip()
                    seq = record[1].strip()
                    seq_dic[name] = seq
        
        #根据已完成内容清理ID;如果都跑完了，重新跑则删除progress_record 文件
        if len(progress_record_lst) >0:
            for seq_id in progress_record_lst:
                del seq_dic[seq_id]
        #全部完成后，清空内容，第二次因为清空就重新开始了;还是人工清理吧
        if len(seq_dic) == 0:
            print('All tasks have been delivered, please check result documents or empty \'progress_record\' file.')
            sys.exit()
            
        flags_seq_type = '1'  # 1 DNA 2 Amino Acid
        last_seq = seq_dic[name]
        for s in last_seq:
            if s not in ['A','T','G','C']:
                flags_seq_type='2'
                break
        
        stop_code = ['TGA','TAA','TAG']
        for name in seq_dic:
            seq = seq_dic[name]
            seq_len = len(seq)
            if seq_len%3 != 0 and flags_seq_type==1 :
                print('waring!:\n'+name+'\tlen:'+str(len(seq_dic[name]))+' not a multiple of three.\n')
                flags_check = 1
            #(3,seq_len,3) 最后一个3碱基不会取出，(3,seq_len+,3)，则会取出
            for idx in  range(3,seq_len,3):
                three_code = seq[idx-3:idx]
                if three_code in stop_code:
                    print('stop code in seq(except at the end)\n')
                    flags_check = 1
        
        if flags_check == 1 :
            sys.exit()
        
        # 如果需要清理的id 为空，覆盖写header
        if len(progress_record_lst)==0:
            with open(outfile,mode='w',encoding='utf-8') as out:
                out.write('seq_name\tverification_code\n')
        
        with sync_playwright() as playwright:
            run_submit(playwright,seq_dic,flags_seq_type,flags_ECS,RestrictionEnzyme_list,outfile,progress_record,headless)
        
    elif action == 'download':
        headless = args.headless
        input_table = args.input_table
        outdir = args.outdir
        result_name = args.result_name
        outfile = str(Path('/').joinpath(outdir,result_name))
        tmp_dir = Path('/').joinpath(outdir,'docx')
        tmp_dir.mkdir(parents=True,exist_ok=True)

        #download_progress_record
        #总是追加写入
        #进度文件检查是否存在
        #不存在，就覆盖写
        #存在读取id
        progress_record_lst =[]
        download_progress_record = Path("\\").joinpath(outdir,'download_progress_record')
        
        if download_progress_record.exists():
            with open(download_progress_record,mode='r',encoding='utf-8') as fh:
                for line in fh:
                    seq_id = line.strip()
                    if seq_id:
                        progress_record_lst.append(seq_id)
                        
        #读取id 信息，使用有顺序的字典，避免重复清理时清理掉最后一个
        data_id_dic = OrderedDict()
        with open(input_table,mode='r',encoding='utf-8') as fh:
            for line in fh:
                if 'seq_name' in line or 'verification_code' in line:
                    continue
                record = re.split('\t',line.strip())
                name = record[0].strip()
                submit_id = record[1].strip()
                data_id_dic[name] = submit_id

        #根据已完成内容清理ID;如果都跑完了，重新跑则删除progress_record 文件
        if len(progress_record_lst) >0:
            for seq_id in progress_record_lst:
                del data_id_dic[seq_id]
        #全部完成后，清空内容，第二次因为清空就重新开始了;还是人工清理吧
        if len(data_id_dic) == 0:
            print('All tasks have been delivered, please check result documents or empty \'progress_record\' file.')
            #with open(progress_record,mode='w',encoding='utf-8') as out:
            #    out.write('')
            sys.exit()

        # 如果需要清理的id 为空，覆盖写header
        if len(progress_record_lst)==0:
            with open(outfile,mode='w',encoding='utf-8') as out:
                out.write("seq_id\tperc\tLength\tdna_seq\n")

        with sync_playwright() as playwright:
            run_download(playwright,data_id_dic,tmp_dir,download_progress_record,headless)

        # 读取文件
        with open(outfile,mode='a',encoding='utf-8') as out:
            docx_name_list = GetAllFileNames(tmp_dir)
            for name_file in docx_name_list:
                seq_name=re.sub(r'\.docx','',str(name_file))
                docx_path = Path("\\").joinpath(tmp_dir,name_file)
                #seq_id,GC_perc,Length,protein_seq,dna_seq
                tmp_lst =read_docx(seq_name,docx_path)
                print(tmp_lst)
                out.write('\t'.join(tmp_lst)+'\n')

if __name__ == '__main__':
    main()