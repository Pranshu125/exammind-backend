import re

with open("src/pages/PrepMode.jsx", "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("Youtube", "Video")

with open("src/pages/PrepMode.jsx", "w", encoding="utf-8") as f:
    f.write(content)

print("done")
