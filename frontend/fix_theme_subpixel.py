import re

with open("src/contexts/ThemeContext.jsx", "r", encoding="utf-8") as f:
    content = f.read()

# I will replace the Fluid Edge section in the CSS
old_fluid = """      /* Fluid Edge */
      border-radius: 20px 0 0 20px !important;
      margin-right: 0 !important;
      padding-right: 1.5rem !important;
      border: none !important;
    }
    
    /* Inverted Curves */
    .sidebar-link.active::before {
      content: "";
      position: absolute;
      right: 0;
      bottom: 100%;
      width: 20px;
      height: 20px;
      background-color: transparent;
      border-bottom-right-radius: 20px;
      box-shadow: 0 10px 0 0 var(--matte-bg);
      pointer-events: none;
    }
    
    .sidebar-link.active::after {
      content: "";
      position: absolute;
      right: 0;
      top: 100%;
      width: 20px;
      height: 20px;
      background-color: transparent;
      border-top-right-radius: 20px;
      box-shadow: 0 -10px 0 0 var(--matte-bg);
      pointer-events: none;
    }"""

new_fluid = """      /* Fluid Edge (Subpixel Perfect) */
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
    }
    
    /* Hide scrollbar entirely to prevent layout shifts/gaps */
    .custom-scrollbar::-webkit-scrollbar {
      display: none;
    }
    .custom-scrollbar {
      -ms-overflow-style: none;
      scrollbar-width: none;
    }"""

content = content.replace(old_fluid, new_fluid)

with open("src/contexts/ThemeContext.jsx", "w", encoding="utf-8") as f:
    f.write(content)

print("done")
