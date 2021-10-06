# -*- coding: utf-8 -*-

import os 
import subprocess



#执行命令的方法
commond='date'
commond1='ls'
commond2='dir'#这是在windows 上的ls命令



#第一种os.system()
#os.system(commond)
os.system(commond2)#根据具体的命令输入执行

a=os.system(commond2)
print(str(a)+"##")#命令返回的是状态码；就是昨天和你说的shell 下echo $? 出来的数字；返回0表示，运行正常


#第二种
#os.popen
#执行 并返回获得的内容


b=os.popen(commond2)
print(b)
print(b.readlines())#返回 一个对象；需要用readlines() 获得列表形式的内容


#第三种

p = subprocess.Popen('dir', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
# shell=True 指定shell 程序运行
# stdout=subprocess.PIPE  标准输出通过通道获得
#stderr=subprocess.STDOUT  标准输出 给了标准错误 ；这里我也不太清楚
# subprocess.PIPE
# 一个可以被用于Popen的stdin 、stdout 和stderr 3个参数的特输值，表示需要创建一个新的管道。
# subprocess.STDOUT
# 一个可以被用于Popen的stderr参数的输出值，表示子程序的标准错误汇合到标准输出。
#PIPE
print(p.stdout) #这里 p.stdout 就是直接实际的结果，只是 都是一长条字符串，中间带\n

#下面p.stdout.readlines() 会根据\n拆分为多个元素的列表

for line in p.stdout.readlines():
    print (line,)
#下面的可能没啥用
p.wait()#等待进程结束
p.kill()#杀掉进程






def execute_cmd(cmd):
        p = subprocess.Popen(cmd,
                             shell=True,
                             close_fds=True,
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        #windows上subprocess.Popen的参数close_fds=True与管道不能共存
        stdout, stderr = p.communicate()
        if p.returncode != 0:
               return p.returncode, stderr
        return p.returncode, stdout


if __name__=='__main__':
    cmd='ls /u01'
    returncode,out=execute_cmd(cmd)
    if returncode != 0:
        raise SystemExit('execute {0} err :{1}'.format(cmd,out))
    else:
       print("execute command ({0} sucessful)".format(cmd))

# 参考1
# https://www.cnblogs.com/zydev/p/8673620.html
# 参考2
# https://www.jb51.net/article/149668.htm

# 参考3
# https://www.chenyudong.com/archives/python-subprocess-popen-block.html
