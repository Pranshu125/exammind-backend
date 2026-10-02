import re

with open("src/components/CustomSelect.jsx", "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace(
    "export default function CustomSelect({ value, onChange, options, className = '', direction = 'down' }) {",
    "export default function CustomSelect({ value, onChange, options, className = '', direction = 'down', size = 'default' }) {"
)

old_div = """<div
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center justify-between w-full p-3 bg-white dark:bg-gray-800 dark:bg-gray-800 border border-gray-200 dark:border-gray-600 dark:border-gray-700 rounded-lg cursor-pointer hover:border-blue-400 focus:ring-2 focus:ring-blue-500 outline-none transition-colors"
      >"""
new_div = """<div
        onClick={() => setIsOpen(!isOpen)}
        className={`flex items-center justify-between w-full ${size === 'small' ? 'px-3 py-2 text-xs' : 'p-3 text-sm'} bg-white dark:bg-gray-800 dark:bg-gray-800 border border-gray-200 dark:border-gray-600 dark:border-gray-700 rounded-lg cursor-pointer hover:border-blue-400 focus:ring-2 focus:ring-blue-500 outline-none transition-colors`}
      >"""

content = content.replace(old_div, new_div)

with open("src/components/CustomSelect.jsx", "w", encoding="utf-8") as f:
    f.write(content)

print("done")
