import rtoml

data = {
    "project": {
        "name": "rtoml Demo",
        "version": "1.0.0",
        "authors": ["Alice <alice@example.com>", "Bob <bob@example.com>"],
    },
    "database": {
        "url": "postgresql://user:pass@localhost/db",
        "timeout": 30,
    }
}

with open("config.toml", "w", encoding="utf-8") as f:
    rtoml.dump(data, f)


with open("config.toml", "r", encoding="utf-8") as f:
    try:
        config = rtoml.load(f)
    except rtoml.TomlParsingError as e:
        print(f"TOML 解析失败: {e}")

# 取已知值
print(config["database"]["url"])
# 安全获取嵌套字段
print(config.get("database").get("url"))  # None



# 修改
config["project"]["version"] = "3.0.0"
config["dependencies"] ={"new":["rtoml>=0.9.0", "requests>=2.28.0"]}

# 写入
with open("config_updated.toml", "w", encoding="utf-8") as f:
    rtoml.dump(config, f)
