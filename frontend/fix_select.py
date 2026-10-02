import re

with open("src/components/CustomSelect.jsx", "r", encoding="utf-8") as f:
    content = f.read()

# Add size prop
content = content.replace(
    "export default function CustomSelect({ value, onChange, options, className = '', direction = 'down' }) {",
    "export default function CustomSelect({ value, onChange, options, className = '', direction = 'down', size = 'default' }) {"
)

# Modify padding based on size prop
content = content.replace(
    """className="flex items-center justify-between w-full p-3 bg-white""",
    """className={`flex items-center justify-between w-full ${size === 'small' ? 'px-3 py-1.5' : 'p-3'} bg-white"""
)

# Also fix the inner div to close properly for the template literal string
# Wait, the original was className="... string ...". Now it's className={`... string ...`}
content = content.replace(
    """focus:ring-blue-500 outline-none transition-colors">""",
    """focus:ring-blue-500 outline-none transition-colors`}>"""
)

# Wait, let me just do a targeted regex for the whole div to be safe
