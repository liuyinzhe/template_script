
import re
import time
from pathlib import Path
from playwright.sync_api import Playwright, sync_playwright, expect

from lxml import etree


from copy import copy 
from lxml import etree

def parse_html(html_string):
    '''
        # 1#//*[@id="mimContent"]/div[1]/div[5]/div/table/tbody/tr[3]/td[1]/a/text()
        # 2# //*[@id="mimContent"]/div[1]/div[5]/div/table/tbody/tr[1]/td[2]/span/a[1]/text()
        # //*[@id="mimContent"]/div[1]/div[5]/div/table/tbody/tr[10]/td[2]/span/a/text()
        # //*[@id="mimContent"]/div[1]/div[5]/div/table/tbody/tr[10]/td[2]/span/text()

        # 3# //*[@id="mimContent"]/div[1]/div[5]/div/table/tbody/tr[1]/td[3]/span/text()
        # 4# //*[@id="mimContent"]/div[1]/div[5]/div/table/tbody/tr[1]/td[4]/span/text()
        # 5# //*[@id="mimContent"]/div[1]/div[5]/div/table/tbody/tr[1]/td[5]/span/a/text()
        # 6# //*[@id="mimContent"]/div[1]/div[5]/div/table/tbody/tr[1]/td[6]/span/text()
        # 7# //*[@id="mimContent"]/div[1]/div[5]/div/table/tbody/tr[1]/td[7]/span/a/text()
        # 8# //*[@id="mimContent"]/div[1]/div[5]/div/table/tbody/tr[1]/td[8]/span/abbr/text()
        # 9# //*[@id="mimContent"]/div[1]/div[5]/div/table/tbody/tr[1]/td[9]/span/abbr/text()
        # 10# //*[@id="mimContent"]/div[1]/div[5]/div/table/tbody/tr[1]/td[10]/span/text()
        # 11# //*[@id="mimContent"]/div[1]/div[5]/div/table/tbody/tr[1]/td[11]/span/a/text()
    '''
    all_record = []
# with open ('xx.html', 'r', encoding='utf-8') as f:
#     html_string = f.read()
    html = etree.HTML(html_string)
    # 表格数量
    tr_num = len(html.xpath('//*[@id="mimContent"]/div[1]/div[5]/div/table/tbody/tr')) 
    # 143
    last_recod = []
    for i in range(1,tr_num+1):
        # 嵌套表格 元素个数
        embedded_tables_row_lst = html.xpath('//*[@id="mimContent"]/div[1]/div[5]/div/table/tbody/tr['+str(i)+']/td')
        # 如果数量小于11,则为嵌套表格，有些内容与上一条序列相同
        #print(len(embedded_tables_row_lst))
        serial_number,location_1,location_2,\
            gene_locus,gene_locus_name,gene_Locus_MIM_number,\
            phenotype,phenotype_MIM_number,inheritance,\
            Pheno_map_key,comments,mouse_symbol = None,None,None,None,None,None,None,None,None,None,None,None
        if len(embedded_tables_row_lst) < 11:
            # 重复4个
            '''
            //*[@id="mimContent"]/div[1]/div[5]/div/table/tbody/tr[31]/td[1]/span/text()
            //*[@id="mimContent"]/div[1]/div[5]/div/table/tbody/tr[31]/td[2]/span/a/text()
            //*[@id="mimContent"]/div[1]/div[5]/div/table/tbody/tr[1]/td[8]/span/abbr/text()
            //*[@id="mimContent"]/div[1]/div[5]/div/table/tbody/tr[2]/td[4]/span/abbr/text()
            '''
            # {Alkaline phosphatase, plasma level of, QTL 2}
            phenotype = html.xpath('//*[@id="mimContent"]/div[1]/div[5]/div/table/tbody/tr['+str(i)+']/td[1]/span/text()')[0].strip()
            # 612367
            phenotype_MIM_number_lst = html.xpath('//*[@id="mimContent"]/div[1]/div[5]/div/table/tbody/tr['+str(i)+']/td[2]/span/a/text()')
            if phenotype_MIM_number_lst == None or len(phenotype_MIM_number_lst) == 0:
                phenotype_MIM_number = ""
            else:
                phenotype_MIM_number = phenotype_MIM_number_lst[0].strip()

            # AR
            inheritance_lst = html.xpath('//*[@id="mimContent"]/div[1]/div[5]/div/table/tbody/tr['+str(i)+']/td[8]/span/abbr/text()')
            if inheritance_lst == None or len(inheritance_lst) == 0 :
                inheritance = ""
            else:
                inheritance = inheritance_lst[0].strip()
            # 2
            Pheno_map_key = html.xpath('//*[@id="mimContent"]/div[1]/div[5]/div/table/tbody/tr['+str(i)+']/td[4]/span/abbr/text()')[0].strip()
            last_recod[6] = phenotype
            last_recod[7] = phenotype_MIM_number
            last_recod[8] = inheritance
            last_recod[9] = Pheno_map_key
            all_record.append('\t'.join(last_recod))
            # last_recod = [serial_number,location_1,location_2,
            #               gene_locus,gene_locus_name,gene_Locus_MIM_number,
            #               phenotype,phenotype_MIM_number,
            #               inheritance,Pheno_map_key,
            #               comments,mouse_symbol]
        else: # 正常11个列
            # 302
            serial_number = html.xpath('//*[@id="mimContent"]/div[1]/div[5]/div/table/tbody/tr['+str(i)+']/td[1]/a/text()')[0].strip()
            # //*[@id="mimContent"]/div[1]/div[5]/div/table/tbody/tr[10]/td[2]/span/a/text()
            # //*[@id="mimContent"]/div[1]/div[5]/div/table/tbody/tr[19]/td[2]/span/text() #[-1]
            # 1:1
            location_1 =  html.xpath('//*[@id="mimContent"]/div[1]/div[5]/div/table/tbody/tr['+str(i)+']/td[2]/span/a/text()')[0].strip()
            # 1p36
            location_2 =  html.xpath('//*[@id="mimContent"]/div[1]/div[5]/div/table/tbody/tr['+str(i)+']/td[2]/span/text()')[-1].strip()

            # AD7CNTP
            gene_locus =  html.xpath('//*[@id="mimContent"]/div[1]/div[5]/div/table/tbody/tr['+str(i)+']/td[3]/span/text()')[0].strip()
            # Alzheimer disease neuronal thread protein
            gene_locus_name = html.xpath('//*[@id="mimContent"]/div[1]/div[5]/div/table/tbody/tr['+str(i)+']/td[4]/span/text()')[0].strip()
            # 607413
            gene_Locus_MIM_number = html.xpath('//*[@id="mimContent"]/div[1]/div[5]/div/table/tbody/tr['+str(i)+']/td[5]/span/a/text()')[0].strip()
            # {Alkaline phosphatase, plasma level of, QTL 2}
            phenotype_lst = html.xpath('//*[@id="mimContent"]/div[1]/div[5]/div/table/tbody/tr['+str(i)+']/td[6]/span/text()')
            if phenotype_lst == None or len(phenotype_lst) == 0 :
                phenotype = ""
            else:
                phenotype = phenotype_lst[0].strip()

            # 612367
            phenotype_MIM_number_lst = html.xpath('//*[@id="mimContent"]/div[1]/div[5]/div/table/tbody/tr['+str(i)+']/td[7]/span/a/text()')
            if phenotype_MIM_number_lst == None or len(phenotype_MIM_number_lst) == 0:
                phenotype_MIM_number = ""
            else:
                phenotype_MIM_number = phenotype_MIM_number_lst[0].strip()
            # AR
            inheritance_lst = html.xpath('//*[@id="mimContent"]/div[1]/div[5]/div/table/tbody/tr['+str(i)+']/td[8]/span/abbr/text()')
            if inheritance_lst == None or len(inheritance_lst) == 0:
                inheritance = ""
            else:
                inheritance = inheritance_lst[0].strip()
            # 2
            Pheno_map_key = html.xpath('//*[@id="mimContent"]/div[1]/div[5]/div/table/tbody/tr['+str(i)+']/td[9]/span/abbr/text()')[0].strip()
            # linkage with rs1780324
            comments_lst = html.xpath('//*[@id="mimContent"]/div[1]/div[5]/div/table/tbody/tr['+str(i)+']/td[10]/span/text()')
            if comments_lst == None or len(comments_lst) == 0 :
                comments = ""
            else:
                comments = comments_lst[0].strip()
            # (from MGI)
            mouse_symbol_lst = html.xpath('//*[@id="mimContent"]/div[1]/div[5]/div/table/tbody/tr['+str(i)+']/td[11]/span/a/text()')
            if mouse_symbol_lst == None or len(mouse_symbol_lst) == 0 :
                mouse_symbol = ""
            else:
                mouse_symbol = mouse_symbol_lst[0].strip()

            last_recod = [serial_number,location_1,location_2,
                          gene_locus,gene_locus_name,gene_Locus_MIM_number,
                          phenotype,phenotype_MIM_number,
                          inheritance,Pheno_map_key,
                          comments,mouse_symbol]
            all_record.append('\t'.join(last_recod))
    return all_record


def run(playwright: Playwright) -> None:
    # 获取当前目录
    current_dir = Path.cwd()
    browser = playwright.chromium.launch(headless=False,timeout=90000)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.xxx.com/geneMap")
    # 关闭贡献窗口
    page.get_by_label("Close").click()
    # 勾选常染色体 与 X Y
    page.get_by_label("Autosomal").check()
    page.get_by_label("X").check()
    page.get_by_label("Y").check()
    # 点击搜索
    page.get_by_role("button", name="   Search").click()
    time.sleep(0.7)
    # 只显示 有 表型的信息
    page.get_by_role("button", name="Phenotype Only Entries").click()
    # Show 100 切换
    page.get_by_role("link", name="Show").click()
    time.sleep(0.5)
    # 去除Highlights高亮
    page.get_by_label("Highlights").uncheck()
    time.sleep(0.7)
    # 获得页面
    #html_str = str(page.content())
    # //*[@id="mimContent"]/div[1]/div[3]/div[1]
    # /html/body/div[2]/div[4]/div[1]/div[3]/div[1]
    # <div class="col-lg-2 col-md-2 col-sm-2 col-xs-2">Results: 17,540 entries.</div>


    html_string = str(page.content())
    html = etree.HTML(html_string)
    html_match = html.xpath('//*[@id="mimContent"]/div[1]/div[3]/div[1]/text()')
    first_match = html_match[0].strip()
    #print(first_match)
    # Results: 6,133 entries.
    
    # 匹配数字
    match_obj = re.search(r"[\d,]+", first_match)
    #print(match_obj.group(0))
    match_str = re.sub(",","",match_obj.group(0))
    time_int = int(match_str)//100
    #print(int(match_str))
    
    # 除以100 判断 +0.5 取整数，判断 next 次数
    # 整数 3次 ，就是next 点2次
    # 3.2次， 则是点 3次
    
    # 第一次下载
    geneMap_path = current_dir.joinpath("geneMap")
    geneMap_path.mkdir(parents=True, exist_ok=True)
    # out_file_path = geneMap_path.joinpath("0.tsv")
    # page.get_by_role("button", name="Download As").click()
    # with page.expect_download() as download_info:
    #     page.get_by_role("link", name="Tab-delimited File").click()
    # download = download_info.value
    # download.save_as(out_file_path)
    # time.sleep(1.3)

    all_record = parse_html(html_string)
    geneMap_file_path = geneMap_path.joinpath("geneMap.tsv")
    if geneMap_file_path.exists():
        geneMap_file_path.unlink()

    with open(geneMap_file_path, "a", encoding="utf-8") as out:
        out.write("\t".join(["serial_number","location_1","location_2",
                          "gene_locus","gene_locus_name","gene_Locus_MIM_number",
                          "phenotype","phenotype_MIM_number",
                          "inheritance","Pheno_map_key",
                          "comments","mouse_symbol"])+"\n")
        for line_string in all_record:
            out.write(line_string+"\n")
        # time_int = 3
        for i in range(1,time_int+1):
            # 翻页
            time.sleep(1.1)
            page.get_by_role("link", name="Next ›").first.click()
            # 去除Highlights高亮 *****
            page.get_by_label("Highlights").uncheck()
            time.sleep(0.7)
            html_string = str(page.content())
            all_record = parse_html(html_string)
            for line_string in all_record:
                out.write(line_string+"\n")
            time.sleep(3.3)
        
    #
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
