import re

with open("src/contexts/ThemeContext.jsx", "r", encoding="utf-8") as f:
    content = f.read()

# I will replace the previous fluid CSS block
old_css = """      /* Fluid Edge (Subpixel Perfect) */
      border-radius: 20px 0 0 20px !important;
      margin-right: -2px !important; /* Overlap right edge slightly to kill gaps */
      padding-right: calc(1.5rem + 2px) !important;
      border: none !important;
    }
    
    /* Inverted Curves */
    .sidebar-link.active::before {
      content: "";
      position: absolute;
      right: 0;
      bottom: calc(100% - 1px); /* Overlap link slightly to kill horizontal gaps */
      width: 24px;
      height: 24px;
      background-color: transparent;
      border-bottom-right-radius: 20px;
      box-shadow: 0 12px 0 0 var(--matte-bg);
      pointer-events: none;
      z-index: 10;
    }
    
    .sidebar-link.active::after {
      content: "";
      position: absolute;
      right: 0;
      top: calc(100% - 1px);
      width: 24px;
      height: 24px;
      background-color: transparent;
      border-top-right-radius: 20px;
      box-shadow: 0 -12px 0 0 var(--matte-bg);
      pointer-events: none;
      z-index: 10;
    }"""

new_css = """      /* Fluid Edge (Radial Gradient Perfected) */
      border-radius: 20px 0 0 20px !important;
      margin-right: -1px !important; /* Perfect overlap to kill container gap */
      padding-right: calc(1.5rem + 1px) !important;
      border: none !important;
    }
    
    /* Inverted Curves */
    .sidebar-link.active::before {
      content: "";
      position: absolute;
      right: 0;
      bottom: calc(100% - 1px); /* Overlap 1px vertically to prevent subpixel line */
      width: 20px;
      height: 21px;
      background: radial-gradient(circle at 0 0, transparent 20px, var(--matte-bg) 20px);
      pointer-events: none;
      z-index: 10;
    }
    
    .sidebar-link.active::after {
      content: "";
      position: absolute;
      right: 0;
      top: calc(100% - 1px); /* Overlap 1px vertically */
      width: 20px;
      height: 21px;
      background: radial-gradient(circle at 0 21px, transparent 20px, var(--matte-bg) 20px);
      pointer-events: none;
      z-index: 10;
    }"""

content = content.replace(old_css, new_css)

with open("src/contexts/ThemeContext.jsx", "w", encoding="utf-8") as f:
    f.write(content)

print("done")
