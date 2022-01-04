import  random
from hashlib import md5

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



# 摘要算法

# 加盐的md5
# 获取原始密码+salt的md5值
def create_md5(pwd,salt):
    md5_obj = md5()
    # print(md5().update(pwd.encode('utf-8')))
    # 大文件可bytes 多份 update 顺序一致,最终md5也一致
    md5_obj.update((pwd + salt).encode('utf-8'))
    return md5_obj.hexdigest()


# 原始密码
pwd = '123456'
# 随机生成4位salt
salt = 'salt'
# 加密后的密码
md5 = create_md5(pwd, salt)

print ('[pwd]\n', pwd)
print ('[salt]\n', salt)
print ('[md5_32]\n', md5)
# 16位 md5
print ('[md5_16]\n', md5[8:-8])
