# import os
# import time
import datetime
#时间模块 

print('Hello World!')#python 3的 print 写法
print('Time is ', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S %A'))
#.datetime.now()使用datetime模块来获取当前的日期和时间
#.strftime(format[, t]) 格式化时间
#%Y 四位数的年份表示（000-9999）
#%m 月份（01-12）
#%d 月内中的一天（0-31）
#%H 24小时制小时数（0-23）
#%S 秒（00-59）
#%A 本地完整星期名称
#参考资料
#https://www.runoob.com/python/python-date-time.html
print('__name__ value: ', __name__)
#直接执行__main__

#还有一个妙用
PATH_A="H:/script/model/main"

def main():
    print('this message is from main function')
#函数功能 输出字符串"this message is from main function"

if __name__ == '__main__':#判断变量__name__ 中是否是字符串"__main__";如果是则调用main()函数
    main()
    # print(__name__)