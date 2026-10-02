with open("src/pages/Dashboard.jsx", "r", encoding="utf-8") as f:
    content = f.read()

import re

# 1. Change sidebarOpen to mobileSidebarOpen and add desktopSidebarOpen
content = content.replace("const [sidebarOpen, setSidebarOpen] = useState(false);", """const [mobileSidebarOpen, setMobileSidebarOpen] = useState(false);
  const [desktopSidebarOpen, setDesktopSidebarOpen] = useState(true);""")

# 2. Update the mobile overlay
content = content.replace("{sidebarOpen && (", "{mobileSidebarOpen && (")
content = content.replace("onClick={() => setSidebarOpen(false)}", "onClick={() => setMobileSidebarOpen(false)}")

# 3. Update the sidebar div classes to support desktop toggle
old_sidebar_div = """<div className={`fixed inset-y-0 left-0 z-50 transform transition-transform duration-300 ease-in-out lg:relative lg:translate-x-0 ${sidebarOpen ? 'translate-x-0' : '-translate-x-full'}`}>
        <Sidebar onClose={() => setSidebarOpen(false)} />"""

new_sidebar_div = """<div className={`fixed inset-y-0 left-0 z-50 transform transition-transform duration-300 ease-in-out lg:relative ${desktopSidebarOpen ? 'lg:translate-x-0 lg:w-64' : 'lg:-translate-x-full lg:w-0'} ${mobileSidebarOpen ? 'translate-x-0' : '-translate-x-full'}`}>
        <div className="w-64 h-full"><Sidebar onClose={() => setMobileSidebarOpen(false)} /></div>"""

content = content.replace(old_sidebar_div, new_sidebar_div)

# 4. Update Mobile Top Bar
content = content.replace("onClick={() => setSidebarOpen(true)}", "onClick={() => setMobileSidebarOpen(true)}")

# 5. Add a floating toggle button in the top left for desktop when sidebar is closed (or even when open on deep pages)
# Wait, they want "a small option tin nt corner to open and close the mainmenu when we are on a page that is directly not connected to the mainmenu".
# We can check the route. If it starts with "/exam", we are deep.
# Let's just put it fixed in the top-left corner of the main content area for Desktop.
# The mobile header already has a menu button. We just need one for Desktop.

main_area_start = """        <div className="flex-1 flex flex-col min-w-0 w-full h-full relative">"""

desktop_toggle = """        <div className="flex-1 flex flex-col min-w-0 w-full h-full relative">
          
          {/* Desktop Sidebar Toggle (Only visible on lg screens) */}
          <button 
            onClick={() => setDesktopSidebarOpen(!desktopSidebarOpen)}
            className={`hidden lg:flex absolute top-6 z-40 p-2.5 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-xl shadow-sm text-gray-500 hover:text-[var(--matte-primary)] transition-all ${desktopSidebarOpen ? 'left-6 opacity-0 hover:opacity-100' : 'left-6 opacity-100'}`}
            title="Toggle Menu"
          >
            <Menu size={20} />
          </button>
"""

content = content.replace(main_area_start, desktop_toggle)

with open("src/pages/Dashboard.jsx", "w", encoding="utf-8") as f:
    f.write(content)
print("done")
