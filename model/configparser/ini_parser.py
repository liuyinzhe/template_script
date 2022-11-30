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
            # print(dict(conf.items("mysql_conf")))
            _option_dict = dict(conf.items(section=section))
            _dict.update({section: _option_dict})
        return _dict

    # 使用python-box模块，方便链式调用
    def __getattr__(self, item):
        _box = Box(self.to_dict())
        # https://www.jianshu.com/p/2bc2605f84fb
        # getattr(self, '类的属性或者函数名', '没有属性或函数则返回这里的内容not found')
        return getattr(_box, item)


if __name__ == '__main__':
    conf = ConfTool(file="./db_conf.ini")
    # 配置文件中如没有配置mysql登录名user字段，则默认取root
    print(conf.get_or_default("mysql_conf", "user", "root"))
    print(conf.to_dict())
    # 可以通过属性调用的形式，获取配置
    print(conf.mysql_conf.host)
