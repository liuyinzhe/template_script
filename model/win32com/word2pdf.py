from win32com.client import constants,gencache
import win32com.client as wc
import os
from pathlib import Path
def createpdf(wordPath,pdfPath):
    #word=gencache.EnsureDispatch('Word.Application')
    #word=gencache.EnsureDispatch('kwps.Application')
    try:
        word=gencache.EnsureDispatch('Word.Application')
        doc=word.Documents.Open(wordPath,ReadOnly=1)
        #转换方法
        doc.ExportAsFixedFormat(pdfPath,constants.wdExportFormatPDF)
    except:
        word=gencache.EnsureDispatch('kwps.Application')
        doc=word.Documents.Open(wordPath,ReadOnly=1)
        #转换方法
        doc.ExportAsFixedFormat(pdfPath,constants.wdExportFormatPDF)

## 跳转脚本所在目录
#pwd = os.path.split(os.path.realpath(__file__))[0]
pwd = os.getcwd()
pwd = Path(pwd)
os.chdir(pwd)



#多个文件的转换
print(os.listdir('.')) #当前文件夹下的所有文件
wordfiles=[]
for file in os.listdir('.'):
    if file.endswith(('.doc','.docx')):
        wordfiles.append(file)

print(wordfiles)
for file in wordfiles:
    filepath=os.path.abspath(file)
    index=filepath.rindex('.')
    # 拼接文件名及.pdf后缀
    pdfpath=filepath[:index]+'.pdf'
    createpdf(filepath,pdfpath) 

#https://www.5axxw.com/wiki/content/5o4dge
