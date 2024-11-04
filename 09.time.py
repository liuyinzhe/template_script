import sys
import time
from datetime import datetime
 
def convert_time2Timestamp(time_str, UTC_FORMAT="%Y-%m-%dT%H:%M:%SZ"):
    '''
    字符串时间格式转为时间戳
    2021-03-19T21:37:25Z
    2021-03-26T20:44:31Z
    #UTC_FORMAT = "%Y-%m-%dT%H:%M:%SZ" #huawei cloud
    #LOCAL_FORMAT = "%Y-%m-%d %H:%M:%S"
    #huawei cloud  使用的是 UTC GMT 格林尼治标准时间
    #本地时间戳 进行修改
    #https://blog.csdn.net/weixin_34080951/article/details/94101201
    #https://www.cnblogs.com/jfl-xx/p/8024596.html
    '''
    timeArray = time.strptime(time_str, UTC_FORMAT)
    timeStamp = time.mktime(timeArray)
    return timeStamp
 
 
 
def Timestamp_local2utc(local_stamp):
    '''
    local_stamp 来自本地时间转换
    根据时区与 UTC 时区的 时间偏移offset  ，计算utc 时区的时间戳
    '''
    now_stamp = time.time()
    #offset,看下 时间戳之间的偏移 是否是一个时区
    local_time = time.mktime(time.localtime(now_stamp))
    utc_time = time.mktime(time.gmtime(now_stamp))
    #print(local_time)
    #print(utc_time)
    offset = utc_time - local_time
    #print('offset', offset)
    if utc_time == local_time:
        return local_stamp
    else:
        utc_stamp = local_stamp + offset
        return utc_stamp

def TimeStamp2TimeStr(TimeStamp,FormatStr="%Y-%m-%d %H:%M:%S",TimeOffset_h=8):
    '''
    将UTC时间转换为北京时间(UTC时间8小时偏移)
    Dependence:import datetime
    '''

    utc_time = datetime.datetime.utcfromtimestamp(TimeStamp)  # 将时间戳转换为UTC时间
    # 将UTC时间转换为北京时间 TimeOffset_h = 8
    OffsetTimeZone = datetime.timezone(datetime.timedelta(hours=TimeOffset_h))
    NewTimeStamp = utc_time.astimezone(OffsetTimeZone)
    #print(f"从时间戳{TimeStamp}转换得到的时间为：{NewTimeStamp}")
    # 从时间戳1687565839转换得到的时间为：2023-06-24 08:17:19+08:00
    # https://www.zhihu.com/question/608209144/answer/3087188010
    FormattedTime = NewTimeStamp.strftime(FormatStr)
    return FormattedTime

def get_current_time_format():
    #获取当前时间
    time_obj = datetime.now()
    #格式化时间
    time_format = '{}-{:0>2d}-{:0>2d} {:0>2d}:{:0>2d}:{:0>2d}'.format(time_obj.year,time_obj.month,time_obj.day,time_obj.hour,time_obj.minute,time_obj.second)
    time_format = '{}-{:0>2d}-{:0>2d}'.format(time_obj.year,time_obj.month,time_obj.day)
    '''
    print(time_format)
    2024-08-23 15:04:28
    2024-08-23
    '''
    return time_format
  
def main():
  pass


if __name__ == "__main__":
    if sys.version[0] == "3":
        start_time = time.perf_counter()
    else:
        start_time = time.clock()
    main()
    if sys.version[0] == "3":
        end_time = time.perf_counter()
    else:
        end_time = time.clock()
    print("%s %s %s\n" % ("main()", "use", str(
        datetime.timedelta(seconds=end_time - start_time))))
