
import re
import time
from pathlib import Path
from playwright.sync_api import Playwright, sync_playwright, expect

from lxml import etree


def run(playwright: Playwright) -> None:
    # 获取当前目录
    current_dir = Path.cwd()
    browser = playwright.chromium.launch(headless=False)
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
    out_file_path = geneMap_path.joinpath("0.tsv")
    page.get_by_role("button", name="Download As").click()
    with page.expect_download() as download_info:
        page.get_by_role("link", name="Tab-delimited File").click()
    download = download_info.value
    download.save_as(out_file_path)
    time.sleep(1.3)
    for i in range(1,time_int+1):
        # 翻页
        time.sleep(1.1)
        page.get_by_role("link", name="Next ›").first.click()
        out_file_path = geneMap_path.joinpath(str(i)+".tsv")
        page.get_by_role("button", name="Download As").click()
        with page.expect_download() as download_info:
            page.get_by_role("link", name="Tab-delimited File").click()
        download = download_info.value
        download.save_as(out_file_path)
        print(i)
        time.sleep(3.3)

    # # 下载 table
    # page.get_by_role("button", name="Download As").click()
    # with page.expect_download() as download1_info:
    #     page.get_by_role("link", name="Tab-delimited File").click()
    # download1 = download1_info.value
    #  # 下载 excel
    # page.get_by_role("button", name="Download As").click()
    # with page.expect_download() as download2_info:
    #     page.get_by_role("link", name="Excel File").click()
    # download2 = download2_info.value
    # # 翻页
    # page.get_by_role("link", name="Next ›").first.click()

    # page.get_by_role("link", name="Last »").first.click()
    # page.get_by_text("Next ›").first.click()
    # page.get_by_role("link", name="‹ Previous").first.click()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
