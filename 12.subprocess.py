import subprocess
 
def run_obs_ls_cmd(obsutil_bin, completed_obs_path):
    '''
        param:obs_path
        param:check_dir_list
        #https://www.cnblogs.com/lgj8/p/12132829.html
    '''
    cmd = " ".join([obsutil_bin ,'ls', completed_obs_path])
    ret = subprocess.run(args=cmd, encoding='utf8',
                             stdout=subprocess.PIPE, shell=True, check=True)
    return ret.stdout
 

def run_cmd(exce_bin, args_lst):
    '''
        param:obs_path
        param:check_dir_list
        #https://www.cnblogs.com/lgj8/p/12132829.html
    '''
    command_lst = []
    command_lst.append(exce_bin)
    command_lst.extend(args_lst)
    cmd = " ".join(command_lst)
    ret = subprocess.run(args=cmd, encoding='utf8',
                             stdout=subprocess.PIPE, shell=True, check=True)
    return ret.stdout


def runshell(shell_script,env=None):
    '''
    python subprocess模块设置环境变量,加载动态库
    https://blog.csdn.net/lrzkd/article/details/119931547
    env={"LD_LIBRARY_PATH": "bin/linux/release"}
    subprocess.pOpen("bin/linux/release/a.exe", shell=True, env={"LD_LIBRARY_PATH": "bin/linux/release"})
    
    check:如果该参数设置为 True,并且进程退出状态码不是 0,则弹出CalledProcessError异常
    shell:如果该参数为 True,将通过操作系统的 shell 执行指定的命令。
    text: 默认False, 决定是否启动"文本模式";设置True 所有I/O流都按 Unicode字符串(str类型)处理,自动管理编码解码;
          相反则按照原始字节流(bytes)对待,不会涉及任何编码转换操作
    subprocess.DEVNULL表示使用os.devnull
    subprocess.STDOUT 特殊值,可传递给 stderr 参数,表示 stdout 和 stderr 合并输出
    subprocess.PIPE 管道,可传递给 stdout、stdin 和 stderr 参数。
    '''
    command = "bash "+ str(shell_script)
    return_obj =subprocess.run(command,
                            shell=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            check=True,
                            env=env,
                            text=True,
                            timeout=None)
    returncode = return_obj.returncode
    return returncode
