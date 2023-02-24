# _*_coding:utf-8_*_

from box import Box
from configparser import ConfigParser

#source: https://www.jianshu.com/p/2e795cba28ab
#https://github.com/cdgriffith/Box
#https://zhuanlan.zhihu.com/p/437046499

class ConfTool(ConfigParser):

    def __init__(self, file, encoding="utf-8"):
        # 执行父类的构造函数
        super().__init__()
        self.read(filenames=file, encoding=encoding)

    # 获取不到section或者option，直接返回给定的默认值
    def get_or_default(self, section, option, default=None):
        if not self.has_section(section):
            return default
        elif not self.has_option(section, option):
            return default
            # https://github.com/cdgriffith/Box
        return self.get(section=section, option=option)

    # ini文件内容转换成dict输出
    def to_dict(self):
        _dict = {}
        for section in self.sections():
            # print(dict(self.items("mysql_conf")))
            _option_dict = dict(self.items(section=section))
            _dict.update({section: _option_dict})
        return _dict

    # 使用python-box模块，方便链式调用
    def __getattr__(self, item):
        '''
        __getattr__函数的作用： 如果属性查找（attribute lookup）在实例以及对应的类中（通过__dict__)失败， 那么会调用到类的__getattr__函数, 如果没有定义这个函数，那么抛出AttributeError异常。由此可见，__getattr__一定是作用于属性查找的最后一步，兜底。

        '''
        # Box 返回对象自身 self, 方便调用其属性/函数，所以叫做链式调用，如self.len().sum().value
        _box = Box(self.to_dict())
        # https://www.jianshu.com/p/2bc2605f84fb
        # getattr(object, name[, default])
        # 类，函数或者属性变量，找不到函数或属性返回内容
        return getattr(_box, item)


if __name__ == '__main__':
    conf = ConfTool(file="./db_conf.ini")
    # 配置文件中如没有配置mysql登录名user字段，则默认取root
    print(conf.get_or_default("mysql_conf", "user", "root"))
    print(conf.to_dict())
    # 可以通过属性调用的形式，获取配置
    print(conf.mysql_conf.host)
'''
[mysql_conf]        ; 1、在ini配置文件中,[]中的值被称为section
host = 127.0.0.1    ; 3、一个section下的键值对被称为option
port = 3306         ; 4、同一个section下也可以存在多个option，也就是多个键值对的配置项
username = root
password = 123456
[python]            ; 2、同一个ini文件中可以存在多个section
version = 0.1.9
system_env = mac
'''
