import re

with open("src/contexts/ThemeContext.jsx", "r", encoding="utf-8") as f:
    content = f.read()

# I will find the block starting with "/* Fluid Edge" all the way up to "/* Make sure active icon" or similar
# Wait, let's just find the index of "/* Fluid Edge" and ".sidebar-icon {" and replace everything between them.

start_str = "/* Fluid Edge"
end_str = ".sidebar-icon {"

start_idx = content.find(start_str)
end_idx = content.find(end_str)

if start_idx != -1 and end_idx != -1:
    new_css = """/* Fluid Edge (Ultimate Radial Gradient) */
      border-radius: 40px 0 0 40px !important;
      margin-right: -1px !important; 
      padding-right: 1.5rem !important;
      border: none !important;
    }
    
    /* Inverted Curves */
    .sidebar-link.active::before {
      content: "";
      position: absolute;
      right: 0;
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
    }
    
    /* Hide scrollbar fully */
    .custom-scrollbar::-webkit-scrollbar {
      width: 0px !important;
      display: none !important;
    }
    .custom-scrollbar {
      scrollbar-width: none !important;
      -ms-overflow-style: none !important;
    }
    
    """
    content = content[:start_idx] + new_css + content[end_idx:]
    with open("src/contexts/ThemeContext.jsx", "w", encoding="utf-8") as f:
        f.write(content)
    print("Replaced successfully!")
else:
    print("Could not find boundaries!")
