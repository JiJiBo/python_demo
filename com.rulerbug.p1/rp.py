import requests

response = requests.get("https://www.baidu.com/img/bd_logo1.png")
t=response.content
with open("b.png", "wb") as f:  # 保存的文件名 保存的方式（wb 二进制  w 字符串）
    f.write(response.content)