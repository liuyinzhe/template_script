from docx import Document


def read_docx(doc_file):
    doc = Document(str(doc_file))
    #输出每一段/行的内容
    for para in doc.paragraphs:
        line = str(para.text).strip()
        print(line)
