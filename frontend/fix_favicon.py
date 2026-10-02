import re

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

# Replace favicon
content = content.replace(
    """<link rel="icon" type="image/svg+xml" href="/favicon.svg" />""",
    """<link rel="icon" type="image/jpeg" href="/logo.jpg" />"""
)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(content)

print("done")
