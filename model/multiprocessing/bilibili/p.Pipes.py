from multiprocessing import Process, Pipe
 
def f(conn):
    conn.send([42, None, 'hello']) #发送
    conn.close()
 
if __name__ == '__main__':
    parent_conn, child_conn = Pipe()  #管道
    p = Process(target=f, args=(child_conn,))#子进程通讯作为参数
    p.start()
    print(parent_conn.recv())   # prints "[42, None, 'hello']" #接受，也可以反过来 parent发送
    p.join()