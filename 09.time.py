import sys
import time
import datetime


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
