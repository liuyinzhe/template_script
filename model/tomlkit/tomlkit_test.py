import tomlkit

toml_data = """
[nested]  # Not necessary

    [nested.table]
    string       = "Hello, TOML!"
    weird_string = '''Literal
        Multiline'''
"""
print(tomlkit.dumps(tomlkit.loads(toml_data)))

tomlkit.dumps(tomlkit.loads(toml_data)) == toml_data
# True

# 使用tomlkit创建一个新的TOML文件
from tomlkit import comment, document, nl, table
toml = document() # 创建文档
toml.add(comment("Written by TOML Kit")) # 添加注释信息
toml.add(nl()) # 添加 None line
toml.add("board_size", 3) #添加 key 与 value



player_x = table() # 作为子表
player_x.add("symbol", "X")
player_x.add("color", "blue")
player_x.comment("Start player")
toml.add("player_x", player_x) # 表明为player_x 下面添加了 symbol/color key 值,以及注释Start player

player_o = table()
player_o.update({"symbol": "O", "color": "green"})
toml["player_o"] = player_o

#.add()添加键和值，也可以使用
#.update() 直接从字典添加键和值
'''
# Written by TOML Kit

board_size = 3

[player_x] # Start player
symbol = "X"
color = "blue"

[player_o]
symbol = "O"
color = "green"
'''
print(toml.as_string()) # 转为字符串输出



############################# tomlkit 读取
import tomlkit
with open("read_example.toml", mode="rt", encoding="utf-8") as fp:
        config = tomlkit.load(fp)

print(config)
'''
{'name': 'TOML', 'info': '在TOML中，\n支持多行字符串\n', 'pyVersion': 3.11, 'date': Date(2022, 12, 26)}
'''
# 可以用.add()添加新元素，但无法用.add()更新现有key的值。
config.add("app_name", "Tic-Tac-Toe")

# 批量字典形式添加
from tomlkit import aot, comment, inline_table, nl, table
player_data = [
    {"user": "gah", "first_name": "Geir Arne", "last_name": "Hjelle"},
    {"user": "tompw", "first_name": "Tom", "last_name": "Preston-Werner"},
]

players = aot()
for dic in player_data:
    players.append(
        table()
        .add("username", dic["user"])
        .add("name",
            inline_table()
            .add("first", dic["first_name"])
            .add("last", dic["last_name"])
        )
    )
# 添加空行后添加注释内容,再添加players表
config.add(nl()).add(comment("Players")).add("players", players)


# 更新后写入同一个文件
with open("new_config.toml", mode="wt", encoding="utf-8") as fp:
    tomlkit.dump(config, fp)
