#! /usr/bin/env python
# -*- coding: utf-8 -*-
   #python 多进程并行编程 ProcessPoolExecutor
   #https://blog.csdn.net/itnerd/article/details/102477783
from concurrent.futures import ProcessPoolExecutor, as_completed
import random


#斐波那契数列
#当 n 大于 30 时抛出异常
def fib(n):
    if n > 30:
        raise Exception('can not > 30, now %s' % n)
    if n <= 2:
        return 1
    return fib(n-1) + fib(n-2)




def main():
    nums = [random.randint(0, 33) for _ in range(0, 10)]
    '''
    [13, 17, 0, 22, 19, 33, 7, 12, 8, 16]
    '''
    
    #submit 按照子进程执行结束的先后顺序输出结果，不可控
    with ProcessPoolExecutor(max_workers=3) as executor:
        futures = {executor.submit(fib, n):n for n in nums}
        for f in as_completed(futures):
            try:
                print('fib(%s) result is %s.' % (futures[f], f.result()))
            except Exception as e:
                print(e)
    '''
fib(13) result is 233.
fib(17) result is 1597.
fib(0) result is 1.
fib(22) result is 17711.
fib(19) result is 4181.
can not > 30, now 33
fib(7) result is 13.
fib(12) result is 144.
fib(8) result is 21.
fib(16) result is 987.

    '''
    #上面的submit等价写法
    with ProcessPoolExecutor(max_workers=3) as executor:
        futures = {}
        for n in nums:
            job = executor.submit(fib, n)
            futures[job] = n

        for job in as_completed(futures):
            try:
                re = job.result()
                n = futures[job]
                print('fib(%s) result is %s.' % (n, re))
            except Exception as e:
                print(e)
    '''
fib(13) result is 233.
fib(17) result is 1597.
fib(0) result is 1.
fib(22) result is 17711.
can not > 30, now 33
fib(7) result is 13.
fib(19) result is 4181.
fib(8) result is 21.
fib(12) result is 144.
fib(16) result is 987.
    '''


    #map 按照输入数组的顺序输出结果
    #缺点：某一子进程异常会导致整体中断
    with ProcessPoolExecutor(max_workers=3) as executor: #最大3个数字
        try:
            results = executor.map(fib, nums) #ProcessPoolExecutor(max_workers=3)map(func, arg)
            for num, result in zip(nums, results): #zip() 同时输出两个list 的元素，同一行输出元组(num, result)
                print('fib(%s) result is %s.' % (num, result))
        except Exception as e:
            print(e)

    '''
fib(13) result is 233.
fib(17) result is 1597.
fib(0) result is 1.
fib(22) result is 17711.
fib(19) result is 4181.
can not > 30, now 33
    '''

if __name__ == '__main__':
    main()