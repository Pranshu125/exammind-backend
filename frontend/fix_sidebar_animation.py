with open("src/pages/Dashboard.jsx", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update <main> to have transition-all
old_main = '<main className={`flex-1 overflow-y-auto w-full relative z-10 p-4 md:p-8 lg:p-12 ${!desktopSidebarOpen ? \'lg:pl-24\' : \'\'}`}>'
new_main = '<main className={`flex-1 overflow-y-auto w-full relative z-10 p-4 md:p-8 lg:p-12 transition-all duration-300 ease-in-out ${!desktopSidebarOpen ? \'lg:pl-24\' : \'\'}`}>'
content = content.replace(old_main, new_main)

# 2. Update mini-sidebar to always render, but animate in/out
old_mini_start = "{!desktopSidebarOpen && ("
old_mini_div = '<div className="hidden lg:flex flex-col justify-between absolute inset-y-0 left-0 w-20 z-40 bg-[#141A21] border-r border-gray-800 shadow-sm py-6 items-center">'
new_mini_div = '<div className={`hidden lg:flex flex-col justify-between absolute inset-y-0 left-0 w-20 z-40 bg-[#141A21] border-r border-gray-800 shadow-sm py-6 items-center transform transition-all duration-300 ease-in-out ${desktopSidebarOpen ? \'-translate-x-full opacity-0 pointer-events-none\' : \'translate-x-0 opacity-100\'}`}>'

# Remove the conditional rendering wrapper
import re
# We need to find the mini sidebar block and strip the {!desktopSidebarOpen && ( ... )}
# It's easier to just do a string replace on the exact block.

start_block = """        {!desktopSidebarOpen && (
          <div className="hidden lg:flex flex-col justify-between absolute inset-y-0 left-0 w-20 z-40 bg-[#141A21] border-r border-gray-800 shadow-sm py-6 items-center">"""

new_start_block = """        {/* Mini Sidebar */}
        <div className={`hidden lg:flex flex-col justify-between absolute inset-y-0 left-0 w-20 z-40 bg-[#141A21] border-r border-gray-800 shadow-sm py-6 items-center transform transition-all duration-300 ease-in-out ${desktopSidebarOpen ? '-translate-x-full opacity-0 pointer-events-none' : 'translate-x-0 opacity-100 delay-100'}`}>"""

content = content.replace(start_block, new_start_block)

# Now we need to remove the closing )} of the mini sidebar.
# The mini sidebar ends with:
end_block = """              </button>
            </div>
          </div>
        )}"""
new_end_block = """              </button>
            </div>
          </div>"""
content = content.replace(end_block, new_end_block)


with open("src/pages/Dashboard.jsx", "w", encoding="utf-8") as f:
    f.write(content)
print("done")
