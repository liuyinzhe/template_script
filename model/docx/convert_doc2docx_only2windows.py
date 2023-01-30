import docx
import win32com.client as wc
import operator
import os
from pathlib import Path

# 跳转脚本所在目录
pwd = os.path.split(os.path.realpath(__file__))[0]
pwd = Path(pwd)
os.chdir(pwd)

input_doc=pwd.joinpath('FM_cd7.doc')
out_docx=pwd.joinpath('FM_cd7.docx')

#doc文件另存为docx
word = wc.Dispatch("Word.Application")
doc = word.Documents.Open(str(input_doc))
# 12代表转换后为docx文件
doc.SaveAs(str(out_docx), 12)
doc.Close
word.Quit


# 读取docx 输出所有段落文字
file = docx.Document(out_docx)
for p in file.paragraphs:
    print(p.text)
