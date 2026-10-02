with open("src/pages/Dashboard.jsx", "r", encoding="utf-8") as f:
    content = f.read()

if "PanelLeft" not in content:
    content = content.replace("import { Menu } from 'lucide-react';", "import { Menu, PanelLeft } from 'lucide-react';")

insertion_target = '      <div className="flex-1 flex flex-col min-w-0 w-full h-full relative">'
button_code = """      <div className="flex-1 flex flex-col min-w-0 w-full h-full relative">
        {/* Desktop Sidebar Toggle (Only visible when sidebar is closed on lg screens) */}
        {!desktopSidebarOpen && (
          <div className="hidden lg:flex absolute top-6 left-6 z-40 items-center gap-2">
            <button 
              onClick={() => setDesktopSidebarOpen(true)}
              className="p-2 text-gray-500 hover:text-black dark:text-gray-400 dark:hover:text-white transition-colors rounded-lg hover:bg-gray-200 dark:hover:bg-gray-700"
              title="Open Menu"
            >
              <PanelLeft size={24} />
            </button>
          </div>
        )}
"""

if "Desktop Sidebar Toggle" not in content:
    content = content.replace(insertion_target, button_code)

with open("src/pages/Dashboard.jsx", "w", encoding="utf-8") as f:
    f.write(content)
print("done")
