import re

with open("src/contexts/ThemeContext.jsx", "r", encoding="utf-8") as f:
    content = f.read()

# Replace the Ultimate Sweeping Curve section with NO negative margins
old_css = """      /* Fluid Edge (Ultimate Sweeping Curve) */
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
    }"""

new_css = """      /* Fluid Edge (Ultimate Sweeping Curve - NO CLIPPING) */
      border-radius: 40px 0 0 40px !important;
      margin-right: 0 !important; /* MUST BE 0 to prevent nav overflow clipping */
      padding-right: 1.5rem !important;
      border: none !important;
    }
    
    /* Inverted Curves */
    .sidebar-link.active::before {
      content: "";
      position: absolute;
      right: 0; /* MUST BE 0 to prevent nav clipping */
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
      right: 0;
      top: calc(100% - 1px);
      width: 40px;
      height: 41px;
      background: radial-gradient(circle at 0 41px, transparent 40px, var(--matte-bg) 40px);
      pointer-events: none;
      z-index: 10;
    }"""

content = content.replace(old_css, new_css)

with open("src/contexts/ThemeContext.jsx", "w", encoding="utf-8") as f:
    f.write(content)

print("done")
