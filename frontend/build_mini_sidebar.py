with open("src/pages/Dashboard.jsx", "r", encoding="utf-8") as f:
    content = f.read()

import re

# We need icons: PanelLeft, PanelRight, Cpu, Settings
if "PanelRight" not in content:
    content = content.replace("import { Menu, PanelLeft } from 'lucide-react';", "import { Menu, PanelRight, Cpu, Settings } from 'lucide-react';")

# We also need useNavigate to click settings
if "useNavigate" not in content:
    content = content.replace("import { Routes, Route, useLocation } from 'react-router-dom';", "import { Routes, Route, useLocation, useNavigate } from 'react-router-dom';")

if "const location = useLocation();" in content and "const navigate = useNavigate();" not in content:
    content = content.replace("const location = useLocation();", "const location = useLocation();\n  const navigate = useNavigate();")

# The old button block
old_button_block = """        {!desktopSidebarOpen && (
          <div className="hidden lg:flex absolute top-5 left-6 z-40 items-center gap-3">
            <div className="w-8 h-8 rounded-full overflow-hidden shrink-0 border border-gray-200 dark:border-gray-700 shadow-sm flex items-center justify-center">
              <img src="/logo.jpg" alt="Logo" className="w-full h-full object-cover" />
            </div>
            <button 
              onClick={() => setDesktopSidebarOpen(true)}
              className="p-2 text-gray-400 hover:text-black dark:hover:text-white transition-colors rounded-lg hover:bg-gray-200 dark:hover:bg-gray-700"
              title="Open Menu"
            >
              <PanelLeft size={20} />
            </button>
          </div>
        )}"""

mini_sidebar = """        {!desktopSidebarOpen && (
          <div className="hidden lg:flex flex-col justify-between absolute inset-y-0 left-0 w-20 z-40 bg-[#141A21] border-r border-gray-800 shadow-sm py-6 items-center">
            
            {/* Top section: Logo & Toggle */}
            <div className="flex flex-col items-center gap-6">
              <div className="w-10 h-10 rounded-full overflow-hidden shrink-0 border border-gray-700 shadow-sm flex items-center justify-center">
                <img src="/logo.jpg" alt="Logo" className="w-full h-full object-cover" />
              </div>
              <button 
                onClick={() => setDesktopSidebarOpen(true)}
                className="p-2 text-gray-400 hover:text-white transition-colors rounded-lg hover:bg-white/10"
                title="Expand Menu"
              >
                <PanelRight size={20} />
              </button>
            </div>

            {/* Bottom section: Settings & AI Provider */}
            <div className="flex flex-col items-center gap-6">
              <button 
                onClick={() => navigate('/settings')}
                className="p-2 text-gray-400 hover:text-white transition-colors rounded-lg hover:bg-white/10"
                title="AI Settings"
              >
                <Cpu size={20} />
              </button>
              <button 
                onClick={() => navigate('/settings')}
                className="p-2 text-gray-400 hover:text-white transition-colors rounded-lg hover:bg-white/10"
                title="Settings"
              >
                <Settings size={20} />
              </button>
            </div>
          </div>
        )}"""

content = content.replace(old_button_block, mini_sidebar)

# To prevent overlap with main content, we need to add left padding to main when desktopSidebarOpen is false
old_main = '<main className="flex-1 overflow-y-auto w-full relative z-10 p-4 md:p-8 lg:p-12">'
new_main = '<main className={`flex-1 overflow-y-auto w-full relative z-10 p-4 md:p-8 lg:p-12 ${!desktopSidebarOpen ? \'lg:pl-24\' : \'\'}`}>'
content = content.replace(old_main, new_main)

with open("src/pages/Dashboard.jsx", "w", encoding="utf-8") as f:
    f.write(content)
print("done")
