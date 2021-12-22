def random_string(length):
    '''
    数字大小写
    参考:https://zhuanlan.zhihu.com/p/88869237
    '''
    src = string.ascii_letters + string.digits
    if 0< length <3:
        list_passwd_all = random.sample(src, length)
        random.shuffle(list_passwd_all) #打乱列表顺序
        str_passwd = ''.join(list_passwd_all) #将列表转化为字符串
        return str_passwd
    elif length < 0:
        length=abs(length)
    elif length == 0:
        return ""
    num=length-3
    list_passwd_all = random.sample(src, num) #从字母和数字中随机取length位
    list_passwd_all.extend(random.sample(string.digits, 1))  #让密码中一定包含数字
    list_passwd_all.extend(random.sample(string.ascii_lowercase, 1)) #让密码中一定包含小写字母
    list_passwd_all.extend(random.sample(string.ascii_uppercase, 1)) #让密码中一定包含大写字母
    random.shuffle(list_passwd_all) #打乱列表顺序
    str_passwd = ''.join(list_passwd_all).strip() #将列表转化为字符串
    return str_passwd
