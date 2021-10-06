import re,os
import matplotlib.pyplot as plt
import numpy as np
#pip install -U pillow
import PIL.Image as image
from wordcloud import WordCloud, ImageColorGenerator
#from scipy.misc import imread

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
'id':'习语','j':'简称','r':'代词','c':'连词','p':'介词','u':'助词','y':'语气助词',
'e':'叹词','o':'拟声词','g':'语素','w':'标点','x':'其它'
}
#过滤计划，对1个字的进行过滤；但是保留一些内容
#大于1个字的，提前筛选
    '''
    #过滤1个字的词；
    #   1个字中不过滤与蚕 有关的字
    work_dir = "C:\\Users\\Family\\Desktop\\wb\\result"
    file = "蚕丛.txt"
    input_fh =os.path.join(work_dir,file)
    output_fh =os.path.splitext(input_fh)[0] + ".filter.txt"
    word_freq = {}
    word_all_string = "" #存储云图所需要的字符串，每个word 之间用空格分隔
    #word_filter_lst = ['附錄','',,]
    with open(input_fh,'r',encoding ='utf-8') as fh, open(output_fh,'w',encoding="utf-8") as out:
        for line in fh:
            word,freq,tag = re.split("\t",line.strip())
            
            if len(word) <2 and tag in ['d','q','p','c']:
                #过滤 1个字的
                #'d':'副词','q':'量词','p':'介词','c':'连词'
                continue
            elif word in ['附圖','第1','《','》','來稿','刋詞']:
                #过滤 2个字以上有问题不需要的
                continue
            out.write(line)
            word_freq[word] = int(freq)
            #生成图云 读取的 空格间隔字符串
            if int(freq)>1 :
                tmp_str = (word+' ')*int(freq)
                word_all_string += tmp_str
            else:
                word_all_string += word
    # read the mask / color image
    # 设置背景图片
    ##设置词云形状，若设置了词云的形状，生成的词云与图片保持一致，后面设置的宽度和高度将默认无效
    #https://www.cnblogs.com/cherish-hao/p/12593903.html
    mask_np = np.array(image.open(os.path.join(work_dir,"hua.jpg")))
    #信息来源
    # https://blog.csdn.net/cskywit/article/details/79285988
    #https://amueller.github.io/word_cloud/generated/wordcloud.WordCloud.html
    wc = WordCloud(font_path="C:\\Windows\\Fonts\\simhei.ttf", #simhei.ttf 黑体；STXINWEI.TTF 华文新魏；
                width = 400 , #输出的画布宽度，默认为400像素
                height = 200 ,#输出的画布高度，默认为200像素
                prefer_horizontal = 0.90, #词语水平方向排版出现的频率，默认 0.9 （所以词语垂直方向排版出现频率为 0.1 ）
                mask=mask_np,     #None, #nd-array or None (default=None)如果参数为空，则使用二维遮罩绘制词云。如果 mask 非空，设置的宽高值将被忽略，遮罩形状被 mask 取代。除全白（#FFFFFF）的部分将不会绘制，其余部分会用于绘制词云。如：bg_pic = imread('读取一张图片.png')，背景图片的画布一定要设置为白色（#FFFFFF），然后显示的形状为不是白色的其他颜色。可以用ps工具将自己要显示的形状复制到一个纯白色的画布上再保存，就ok了。
                #mask=back_coloring,#设置背景图片 #若不指定图片，则默认生成矩形词云
                scale = 1, #按照比例进行放大画布，如设置为1.5，则长和宽都是原来画布的1.5倍。
                min_font_size = 4, #显示的最小的字体大小
                max_font_size = None , #显示的最大的字体大小
                ##max_font_size=100, #字体最大值
                font_step = 1 , #不建议修改#字体步长，如果步长大于1，会加快运算但是可能导致结果出现较大的误差
                max_words=2000,# 词云显示的最大词数,200
                background_color="white", #背景颜色
                mode = "RGB" , #当参数为“RGBA”并且background_color不为空时，背景为透明。
                relative_scaling = .5 ,#词频和字体大小的关联性
                color_func = None ,#生成新颜色的函数，如果为空，则使用 self.color_func
                regexp = None , #使用正则表达式分隔输入的文本
                collocations = True , #是否包括两个词的搭配
                colormap = "viridis", #给每个单词随机分配颜色，若指定color_func，则忽略该方法 #string or matplotlib colormap, default=”viridis” 字典dict：kwargs: "white"，kwargs: (255,0,0)
                random_state=None, 
                repeat = False, #是否重复单词和短语直到达到max_words或min_font_size。
                include_numbers = False, # 是否将数字作为段落
                min_word_length = 0 , #一个单词最短长度
                collocation_threshold = 30 #
    )

    # generate word cloud
    #word_all_string = "xxdsd 中文 繁體 xxdsd  883  883  實踐"
    wc.generate(word_all_string)
    # store to file
    fname=os.path.splitext(file)[0] 
    wc.to_file(os.path.join(work_dir, fname+".jpg"))
if __name__ == '__main__':
    main()