import re

with open("src/contexts/ThemeContext.jsx", "r", encoding="utf-8") as f:
    content = f.read()

# I will replace the Fluid Edge section
old_css = """      /* Fluid Edge (Radial Gradient Perfected) */
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

# Use massive 40px curves for that perfect sweeping Apple style
# Use right: -1px to push the curves over the edge just in case
new_css = """      /* Fluid Edge (Ultimate Sweeping Curve) */
      border-radius: 40px 0 0 40px !important;
      margin-right: -2px !important; /* Force overlap into main content */
      padding-right: calc(1.5rem + 2px) !important;
      border: none !important;
    }
    
    /* Inverted Curves */
    .sidebar-link.active::before {
      content: "";
      position: absolute;
      right: -2px; /* Pull it slightly right to cover seams */
      bottom: calc(100% - 1px);
      width: 40px;
      height: 41px;
      background: radial-gradient(circle at 0 0, transparent 40px, var(--matte-bg) 40px);
      pointer-events: none;
      z-index: 10;
    }
    
    .sidebar-link.active::after {
      content: "";
      position: absolute;
      right: -2px;
      top: calc(100% - 1px);
      width: 40px;
      height: 41px;
      background: radial-gradient(circle at 0 41px, transparent 40px, var(--matte-bg) 40px);
      pointer-events: none;
      z-index: 10;
    }
    
    /* Force obliterate scrollbar layout space on Windows */
    .custom-scrollbar::-webkit-scrollbar {
      width: 0px !important;
      height: 0px !important;
      background: transparent !important;
      display: none !important;
    }
    .custom-scrollbar {
      scrollbar-width: none !important;
      -ms-overflow-style: none !important;
    }"""

content = content.replace(old_css, new_css)

with open("src/contexts/ThemeContext.jsx", "w", encoding="utf-8") as f:
    f.write(content)

print("done")
