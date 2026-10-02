with open("src/pages/Dashboard.jsx", "r", encoding="utf-8") as f:
    content = f.read()

old_sidebar = '<div className="w-64 h-full"><Sidebar onClose={() => setMobileSidebarOpen(false)} /></div>'
new_sidebar = '<div className="w-64 h-full"><Sidebar onClose={() => setMobileSidebarOpen(false)} onToggleDesktop={() => setDesktopSidebarOpen(!desktopSidebarOpen)} /></div>'

content = content.replace(old_sidebar, new_sidebar)

with open("src/pages/Dashboard.jsx", "w", encoding="utf-8") as f:
    f.write(content)

# Now modify Sidebar.jsx
with open("src/components/Sidebar.jsx", "r", encoding="utf-8") as f:
    sidebar_content = f.read()

# 1. Update Props
old_props = "export default function Sidebar({ onClose }) {"
new_props = "import { PanelLeftClose } from 'lucide-react';\n\nexport default function Sidebar({ onClose, onToggleDesktop }) {"
if "export default function Sidebar({ onClose }) {" in sidebar_content:
    sidebar_content = sidebar_content.replace(old_props, new_props)

# 2. Add the toggle button next to the Logo
old_logo = """        <h1 className="sidebar-title text-xl font-bold tracking-tight mb-8 flex items-center gap-2 pr-4">
          <div className="w-8 h-8 rounded-full overflow-hidden shrink-0 border border-gray-700 shadow-sm flex items-center justify-center">
            <img src="/logo.jpg" alt="Logo" className="w-full h-full object-cover" />
          </div>
          EXAMMIND
        </h1>"""

new_logo = """        <div className="sidebar-title mb-8 flex items-center justify-between pr-4">
          <h1 className="text-xl font-bold tracking-tight flex items-center gap-2">
            <div className="w-8 h-8 rounded-full overflow-hidden shrink-0 border border-gray-700 shadow-sm flex items-center justify-center">
              <img src="/logo.jpg" alt="Logo" className="w-full h-full object-cover" />
            </div>
            EXAMMIND
          </h1>
          <button onClick={onToggleDesktop} className="hidden lg:flex p-1.5 text-gray-500 hover:text-white rounded-lg transition-colors" title="Close Sidebar">
            <PanelLeftClose size={20} />
          </button>
        </div>"""

if "EXAMMIND" in sidebar_content:
    sidebar_content = sidebar_content.replace(old_logo, new_logo)

with open("src/components/Sidebar.jsx", "w", encoding="utf-8") as f:
    f.write(sidebar_content)

print("done")
