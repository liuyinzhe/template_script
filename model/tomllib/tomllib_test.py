#import tomllib

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib
from decimal import Decimal

############# 读取
with open("read_example.toml", mode="rb") as f:
    data = tomllib.load(f,parse_float=Decimal) # 默认实现满足使用 64 位浮点数,Decimal则是更高精度
    '''
    load()和 loads()之间的一个区别是，当您使用loads()时，您使用的是常规字符串而不是字节。
    '''
from pprint import pprint
pprint(data) # 可视化更好一些
print(data['pyVersion'])
print(data)

r'''
\b  退格
\t	tab	
\n	换行
\f	换页
\r	回车
"	引号
\\  斜杠
\uXXXX可表示码号为XXXX的unicode字符。
'''

############## 写入
'''
tomli_w有两个函数： dump() 和 dumps()
类似于tomli的load()和loads()。dump()写入文件，dumps()写入字符串。
Python 3.11 中的新 tomllib 库不包括 dump() 和 dumps()
需要安装tomli_w
python -m pip install tomli_w
'''

import tomli_w

config = {
    "user": {
        "player_x": {"symbol": "X", "color": "blue", "ai": True},
        "player_o": {"symbol": "O", "color": "green", "ai": False},
        "ai_skill": 0.85,
    },
    "board_size": 3,
    "server": {"url": "https://tictactoe.example.com"},
}

with open("config.toml", mode="wb") as fp:
    tomli_w.dump(config, fp)
