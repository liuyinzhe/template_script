#Python之路,Day9, 进程、线程、协程篇
#https://www.cnblogs.com/alex3714/articles/5230609.html

#视频
#https://www.bilibili.com/video/BV1X54y1R7JD?p=2

#import multiprocessing, threading
from multiprocessing import Process
from threading import Thread, get_ident
import time,multiprocessing

#进程之间共享通讯
# def f(q):
    # q.put([42, None, 'hello'])

# if __name__ == '__main__':
    # q = multiprocessing.Queue()
    # p = Process(target=f, args=(q,))
    # p.start()
    # print(q.get())    # prints "[42, None, 'hello']"
    # p.join()


def thread_run():
    #print(threading.get_ident())
    print(get_ident()) #get_ident 是对线程里获得线程id 的函数


def info(title):
    print(title)
    print('module name:', __name__)       #获得模块自身名字
    print('parent process:', os.getppid()) # 获得父母(parents) 进程ID 
    print('process id:', os.getpid())      #当进程 ID
    print("\n\n")


def f(name):
    time.sleep(2)
    print('hello', name)
 
if __name__ == '__main__':
    all_process=[] 
    for i in range(10):
        p = Process(target=f, args=('bob',))
        #p = multiprocessing.Process(target=f, args=('bob',))
        p.start()
        t = Thread(target=thread_run, ) 
        #t = threading.Thread(target=thread_run, ) 
        t.start()
        
        all_process.append(p)
        #p.join()  #p.join()加这里 就不是 同时执行多个任务了， 而是按顺序一个一个执行，会比较慢
        #不加 p.join() 也是多个一起执行， 但是程序不会等待这些任务结束，直接去往下执行了
    for obj in all_process:
        p.join()


    print("all done")