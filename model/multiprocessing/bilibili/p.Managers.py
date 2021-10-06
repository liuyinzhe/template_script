from multiprocessing import Process, Manager
 
 '支持所有进程的数据共享 support types list, dict, Namespace, Lock, RLock, Semaphore, BoundedSemaphore, Condition, Event, Barrier, Queue, Value and Array.'
 
def f(d, l):
    d[1] = '1'
    d['2'] = 2
    d[0.25] = None
    l.append(1)
    print(l)
 
if __name__ == '__main__':
    with Manager() as manager:
        d = manager.dict()#可在多个进程之间可以传递和共享的 字典
 
        l = manager.list(range(5)) #可在多个进程之间可以传递和共享的 列表
        p_list = []
        for i in range(10):
            p = Process(target=f, args=(d, l))
            p.start()
            p_list.append(p)
        for res in p_list:
            res.join()
 
        print(d)
        print(l)