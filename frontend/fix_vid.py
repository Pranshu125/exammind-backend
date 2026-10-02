import re

with open("src/pages/PrepMode.jsx", "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("vid.channel_name", "vid.channel_title")

with open("src/pages/PrepMode.jsx", "w", encoding="utf-8") as f:
    f.write(content)

print("done")
