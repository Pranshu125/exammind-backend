with open("src/components/ProfileView.jsx", "r", encoding="utf-8") as f:
    c = f.read()

c = c.replace("Github, Linkedin,", "Code, Briefcase,")
c = c.replace("<Github ", "<Code ")
c = c.replace("<Linkedin ", "<Briefcase ")

with open("src/components/ProfileView.jsx", "w", encoding="utf-8") as f:
    f.write(c)

print("done")
