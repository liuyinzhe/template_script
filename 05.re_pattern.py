import re
######################begin 正则  begin##################
#https://www.cnblogs.com/xp1315458571/p/13720333.html
def pattern_check(pattern_lst ,input_string):
    '''
    多个正则表达式，有任何一个匹配则 返回True
    '''
    check_bool = False
    for pat in pattern_lst:
        pattern = re.compile(str(pat))
        if re.search(pattern, input_string):
            check_bool = True
            break
    return check_bool
 
 
def sub_star(star_str):
    result = re.sub(r'\*', r'\\S+?', star_str)
    #result = str(star_str).replace(r'*', r'\S+?')
    return result

######################begin 正则  end##################
