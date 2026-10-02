with open("src/components/SettingsView.jsx", "r", encoding="utf-8") as f:
    content = f.read()

header_code = """<div className="px-6 py-4 bg-gray-50 border-b border-gray-200 font-bold text-gray-900 text-lg uppercase tracking-wider">
              Settings Menu
            </div>"""

if header_code in content:
    content = content.replace(header_code, "")
else:
    # try one-liner if it's formatted differently
    header_code_2 = '<div className="px-6 py-4 bg-gray-50 border-b border-gray-200 font-bold text-gray-900 text-lg uppercase tracking-wider">Settings Menu</div>'
    content = content.replace(header_code_2, "")

with open("src/components/SettingsView.jsx", "w", encoding="utf-8") as f:
    f.write(content)

print("done")
