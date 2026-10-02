import re

with open("src/components/Sidebar.jsx", "r", encoding="utf-8") as f:
    content = f.read()

# Use regex to find whatever div contains the Sparkles icon inside the h1 tag
pattern = re.compile(r'<h1 className="sidebar-title[^>]*>.*?<div[^>]*>.*?<Sparkles[^>]*>.*?</div>\s*EXAMMIND\s*</h1>', re.DOTALL)

new_header = """<h1 className="sidebar-title text-xl font-bold tracking-tight mb-8 flex items-center gap-2 pr-4">
          <div className="w-8 h-8 rounded-full overflow-hidden shrink-0 border border-gray-700 shadow-sm flex items-center justify-center">
            <img src="/logo.jpg" alt="Logo" className="w-full h-full object-cover" />
          </div>
          EXAMMIND
        </h1>"""

content = pattern.sub(new_header, content)

with open("src/components/Sidebar.jsx", "w", encoding="utf-8") as f:
    f.write(content)

print("done")
