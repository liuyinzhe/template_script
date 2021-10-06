import re
import pandas as pd
from opencc import OpenCC
import thulac    


def  filter_words(dic:dict, lst:list):
    if len(lst)==0:
        return dic
    for x in lst:
        if x in dic:
            del dic[x]
    return dic

def chinese_convert(string:str,mode:str ):
    '''
    hk2s: Traditional Chinese (Hong Kong standard) to Simplified Chinese
    s2hk: Simplified Chinese to Traditional Chinese (Hong Kong standard)
    s2t: Simplified Chinese to Traditional Chinese
    s2tw: Simplified Chinese to Traditional Chinese (Taiwan standard)
    s2twp: Simplified Chinese to Traditional Chinese (Taiwan standard, with phrases)
    t2hk: Traditional Chinese to Traditional Chinese (Hong Kong standard)
    t2s: Traditional Chinese to Simplified Chinese
    t2tw: Traditional Chinese to Traditional Chinese (Taiwan standard)
    tw2s: Traditional Chinese (Taiwan standard) to Simplified Chinese
    tw2sp: Traditional Chinese (Taiwan standard) to Simplified Chinese (with phrases)

    '''
    cc = OpenCC(mode)
    converted = cc.convert(str(string))
    return converted
        
def main():
    '''
abbreviate={
'n':'名词','np':'人名','ns':'地名','ni':'机构名','nz':'其它专名',
'm':'数词','q':'量词','mq':'数量词','t':'时间词','f':'方位词','s':'处所词',
'v':'动词','a':'形容词','d':'副词','h':'前接成分','k':'后接成分',
'i':'习语','j':'简称','r':'代词','c':'连词','p':'介词','u':'助词','y':'语气助词',
'e':'叹词','o':'拟声词','g':'语素','w':'标点','x':'其它'
}
    '''
    t2s = True
    info_file = "C:\\Users\\Family\\Desktop\\wb\\new.xls"

    excel_df = pd.read_excel(info_file)
    words_dic = {}
    words_tag_dic = {}

    #set
    #分词#set #T2S=False 繁转简
    thu1 = thulac.thulac(user_dict=None, model_path=None, T2S=t2s, seg_only=False, filt=False)
    #fileter #self.posSet = ["n","np","ns","ni","nz","v","a","id","t","uw"]
    #site-packages\\thulac\\manage\\Filter.py

    for index,row in excel_df.iterrows():
        title = row['题目']
        author = row['作者']
        data = row['期']
        #df.shape 按照iloc 切片取得
        #print(title)
        # convert from Traditional Chinese to Simplified Chinese
        #print(title,converted)

        #针对xx门 处理
        #"門：" 
        #unicode#\u9580\uff1a
        #"門:" 
        #unicode#\u9580\u003a
        #print(str(title))
        #跳过 title 为nan 空白的行
        if isinstance(title,float) :
            print("#"+str(title)+"#")
            continue
        if '\u9580\uff1a' in title or '\u9580\u003a' in title:
            records = re.split("[：:]",title)
            name =records[0].strip()
            if t2s :
                name = chinese_convert(name ,'t2s')
            if name not in words_dic:
                words_dic[name] = 1
                words_tag_dic[name] = 'n'
            else:
                words_dic[name] += 1

        string_lst = thu1.cut(title,text=False) 
        #print(string_lst)
        for enumeration in string_lst:
            word = enumeration[0]
            tag = enumeration[1]
            if word not in words_dic:
                words_dic[word] = 1
                words_tag_dic[word] = tag
            else:
                words_dic[word] += 1
    #过滤词语
    filter_words_lst = ["　",'：','（','）','[',']','…','，','、']
    words_dic = filter_words(words_dic,filter_words_lst)
    #排序
    sorted_word_lst = sorted(words_dic.keys(), key=lambda x:words_dic[x], reverse=True)

    print(len(words_dic))
    word_freq ="C:\\Users\\Family\\Desktop\\wb\\word_frequency.sc.txt"
    #count=0
    
    with open(word_freq,'w',encoding='UTF-8') as out:
        for word in sorted_word_lst:
            word_s = chinese_convert(word ,'s2t')
            out_str =  '\t'.join([word_s,str(words_dic[word]),words_tag_dic[word]])
            #if count == 0:
            #    #print("#"+word+"#")
            #    count =1
            out.write(out_str+"\n")


if __name__ == '__main__':
    main()
    '''
    '''

