import re

with open("src/contexts/ThemeContext.jsx", "r", encoding="utf-8") as f:
    content = f.read()

old_css = """      /* Fluid Edge (Ultimate Radial Gradient) */
      border-radius: 40px 0 0 40px !important;
      margin-right: -1px !important; 
      padding-right: 1.5rem !important;
      border: none !important;
    }"""

new_css = """      /* Fluid Edge (Ultimate Radial Gradient) */
      border-radius: 40px 0 0 40px !important;
      margin-right: 0 !important; 
      padding-right: 1.5rem !important;
      border: none !important;
    }"""

content = content.replace(old_css, new_css)

with open("src/contexts/ThemeContext.jsx", "w", encoding="utf-8") as f:
    f.write(content)

print("done")
