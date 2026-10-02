with open("src/pages/Dashboard.jsx", "r", encoding="utf-8") as f:
    content = f.read()

import re

# We will add useEffect to auto-collapse the sidebar on deep routes
old_import = "import { useState } from 'react';"
new_import = "import { useState, useEffect } from 'react';"
if new_import not in content:
    content = content.replace(old_import, new_import)

old_state = "const [desktopSidebarOpen, setDesktopSidebarOpen] = useState(true);"
new_state = """const [desktopSidebarOpen, setDesktopSidebarOpen] = useState(true);

  // Auto-collapse sidebar on deep routes to save space
  useEffect(() => {
    if (location.pathname.includes('/prep/')) {
      setDesktopSidebarOpen(false);
    } else {
      setDesktopSidebarOpen(true);
    }
  }, [location.pathname]);
"""
if "Auto-collapse" not in content:
    content = content.replace(old_state, new_state)

# Let's also make the toggle button Always Visible if it's closed, and subtly visible if it's open
old_button = "className={`hidden lg:flex absolute top-6 z-40 p-2.5 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-xl shadow-sm text-gray-500 hover:text-[var(--matte-primary)] transition-all ${desktopSidebarOpen ? 'left-6 opacity-0 hover:opacity-100' : 'left-6 opacity-100'}`}"
new_button = "className={`hidden lg:flex absolute top-6 z-40 p-2.5 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-xl shadow-sm transition-all ${desktopSidebarOpen ? '-left-4 opacity-0 hover:opacity-100 hover:left-6' : 'left-6 opacity-100 text-[var(--matte-primary)] hover:bg-[var(--matte-primary)] hover:text-white'}`}"
content = content.replace(old_button, new_button)


with open("src/pages/Dashboard.jsx", "w", encoding="utf-8") as f:
    f.write(content)
print("done")
