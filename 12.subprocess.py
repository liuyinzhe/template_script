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
