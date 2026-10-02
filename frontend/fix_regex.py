with open("src/pages/PrepMode.jsx", "r", encoding="utf-8") as f:
    content = f.read()

bad_string = "String(children).replace(/\n  $/, '')"
good_string = "String(children).replace(/\\\\n$/, '')"
content = content.replace(bad_string, good_string)

bad_string2 = "String(children).replace(/\n$/, '')"
content = content.replace(bad_string2, good_string)

with open("src/pages/PrepMode.jsx", "w", encoding="utf-8") as f:
    f.write(content)

print("done")
