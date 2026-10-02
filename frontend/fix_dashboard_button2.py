with open("src/pages/Dashboard.jsx", "r", encoding="utf-8") as f:
    content = f.read()

old_button_block = """        {!desktopSidebarOpen && (
          <div className="hidden lg:flex absolute top-6 left-6 z-40 items-center gap-2">
            <button 
              onClick={() => setDesktopSidebarOpen(true)}
              className="p-2 text-gray-500 hover:text-black dark:text-gray-400 dark:hover:text-white transition-colors rounded-lg hover:bg-gray-200 dark:hover:bg-gray-700"
              title="Open Menu"
            >
              <PanelLeft size={24} />
            </button>
          </div>
        )}"""

new_button_block = """        {!desktopSidebarOpen && (
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

content = content.replace(old_button_block, new_button_block)

with open("src/pages/Dashboard.jsx", "w", encoding="utf-8") as f:
    f.write(content)
print("done")
