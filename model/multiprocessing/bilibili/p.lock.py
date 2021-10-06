from multiprocessing import Process, Lock
 
def f(l, i):
    l.acquire()#锁激活 ，控制前后顺序； 屏幕接受print 的内容
    try:
        print('hello world', i)
    finally:
        l.release()  #打开锁
 
if __name__ == '__main__':
    lock = Lock()
 
    for num in range(10):
        Process(target=f, args=(lock, num)).start()