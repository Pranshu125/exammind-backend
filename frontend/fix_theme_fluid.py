import re

with open("src/contexts/ThemeContext.jsx", "r", encoding="utf-8") as f:
    content = f.read()

# I will replace the sidebar CSS block.
old_sidebar_css = """      /* Sidebar Specific Logic */
      .sidebar-container {
        background-color: var(--sidebar-bg) !important;
        color: var(--sidebar-text) !important;
        border-color: var(--sidebar-bg) !important;
      }
      .sidebar-footer {
        background-color: rgba(0,0,0,0.1) !important;
        border-color: rgba(0,0,0,0.1) !important;
      }
      .sidebar-title { color: var(--sidebar-text) !important; }
      .sidebar-link {
        color: var(--sidebar-text) !important;
        opacity: 0.8;
      }
      .sidebar-link:hover {
        background-color: var(--sidebar-hover) !important;
        opacity: 1;
      }
      .sidebar-link.active {
        background-color: var(--sidebar-active) !important;
        opacity: 1;
        font-weight: bold;
      }
      .sidebar-icon {
        color: var(--sidebar-text) !important;
        opacity: 0.8;
      }
      .sidebar-link.active .sidebar-icon, .sidebar-link:hover .sidebar-icon {
        opacity: 1;
      }"""

new_sidebar_css = """      /* Sidebar Specific Logic (Fluid Tabs) */
      .sidebar-container {
        background-color: var(--sidebar-bg) !important;
        color: var(--sidebar-text) !important;
        border-color: var(--sidebar-bg) !important;
      }
      .sidebar-footer {
        background-color: rgba(0,0,0,0.15) !important;
        border-color: rgba(0,0,0,0.15) !important;
      }
      .sidebar-title { color: var(--sidebar-text) !important; }
      
      .sidebar-link {
        color: var(--sidebar-text) !important;
        opacity: 0.8;
        border-radius: 12px;
        margin-right: 16px; /* Pill effect off the edge */
        position: relative;
      }
      .sidebar-link:hover {
        background-color: var(--sidebar-hover) !important;
        opacity: 1;
      }
      
      .sidebar-link.active {
        background-color: var(--matte-bg) !important;
        color: var(--matte-text) !important;
        opacity: 1;
        font-weight: bold;
        
        /* Fluid Edge */
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
      }
      
      .sidebar-icon {
        color: var(--sidebar-text) !important;
        opacity: 0.8;
      }
      .sidebar-link:hover .sidebar-icon {
        opacity: 1;
      }
      .sidebar-link.active .sidebar-icon {
        color: var(--matte-primary) !important;
        opacity: 1;
      }"""

content = content.replace(old_sidebar_css, new_sidebar_css)

with open("src/contexts/ThemeContext.jsx", "w", encoding="utf-8") as f:
    f.write(content)

print("done")
