import time
import multiprocessing

def make_calculation():
    count = 0
    for i in range(2000000):
        count  += i
    print('计算结果:',count)

if __name__ == '__main__':
    start_time = time.time()

    process_lst = []
    # make_calculation()
    # make_calculation()
    # make_calculation()
    times = 3
    for i in range(times):
        process = multiprocessing.Process(target=make_calculation)
        process_lst.append(process)
        process.start()

    for process in process_lst:
        process.join() # 主进程等待这个进程，监控

    print('完成，用时{:.2f}秒'.format(time.time() - start_time))
