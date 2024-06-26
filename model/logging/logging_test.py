#!/usr/bin/python
# -*- coding: UTF-8 -*-
import logging


LOG_FORMAT = "%(asctime)s %(name)s %(levelname)s %(pathname)s %(message)s "#配置输出日志格式
#配置输出时间的格式，注意月份和天数不要搞乱了
DATE_FORMAT = '%Y-%m-%d  %H:%M:%S %A ' #'%Y-%m-%d  %H:%M:%S' 

'''
# 默认生成的 root logger 的 level 是 logging.WARNING，低于该级别的就不输出了。
级别排序：CRITICAL > ERROR > WARNING > INFO > DEBUG。（如果需要显示所有级别的内容，可将 level=logging.NOTSET）
'''
# logging.basicConfig(level=logging.DEBUG, 
#                     format=LOG_FORMAT,
#                     datefmt = DATE_FORMAT ,
#                     filename=r"g:\script\model\logging\logging.log", #有了filename参数就不会直接输出显示到控制台，而是直接写入文件
#                     filemode='w'
#                     )


#设置输出格式
logging.basicConfig(level=logging.DEBUG,
                    format=LOG_FORMAT,
                    datefmt = DATE_FORMAT,
                    )



logging.debug("调试代码")    #默认不输出到屏幕(stdout)
logging.info("######## Checking xxx ########")     #记录程序是否正常运行
logging.warning("记录程序运行过程中的警告信息")  #默认输出格式    #WARNING:root:msg3

logging.error("错误")    #默认输出格式    #ERROR:root:msg4
logging.critical("危险") #默认输出格式    #CRITICAL:root:msg5


#以下为一种应用logging 的情况，涉及 异常处理，其实很简单，可以理解为 自己怎么处理在


#下面是 名为 异常处理 的语法； 不要被名字吓到，其实就是如果报错，我怎么处理;后面我整理下 异常处理的写法
try:#尝试做什么
	fh = open("testfile.txt", "r")#打开文件

except IOError as e:#打不开，文件不存在之类的错误 属于 IOError;
	print (e)
	logging.warning("这里出错了，文件打不开")#和print 作用一样

#以下替换上面的except IOError as e；自定义输出错误，的另外写法，IOError 写什么类型都行，不过最好写对应的
#except IOError :#打不开，文件不存在之类的错误 属于 IOError;，不过你写其他类型错误也行；#这里有总结https://blog.csdn.net/linxinfa/article/details/88671287
#	print ("天哪这个文件不存在")



#参考： 
#logging 的用法
#https://www.cnblogs.com/Nicholas0707/p/9021672.html

# Python logging 模块之 logging.basicConfig 用法和参数详解
#https://blog.csdn.net/colinlee19860724/article/details/90965100

#异常处理的输出
#https://www.runoob.com/python3/python3-errors-execptions.html
#https://blog.csdn.net/linxinfa/article/details/88671287
