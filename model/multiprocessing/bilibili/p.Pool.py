from  multiprocessing import Process, Pool, freeze_suppport
import time,
 
def Foo(i):
    time.sleep(2)
    return i+100
 
def Bar(arg):
    print('-->exec done:',arg,os.getpid())#当前进程ID，这里是子进程回调函数，回去调用
 
if __name__=='__main__':
    #windows
    #freeze_suppport()
    pool = Pool(5)  #设置10个进程
    print("主进程",os.getpid())#当前进程ID
    for i in range(10):
        pool.apply_async(func=Foo, args=(i,),callback=Bar) #apply_async 是并行，callback=Bar， 回调,执行Bar；每次一个进程执行完，运行bar;主进程调用回调
        #pool.apply(func=Foo, args=(i,),callback=Bar) #apply 是串行
        #pool.apply(func=Foo, args=(i,))
 
    print('end')
    pool.close()  #先close 然后 join
    pool.join()#进程池中进程执行完毕后再关闭，如果注释，那么程序直接关闭。