import re

with open("src/components/SettingsView.jsx", "r", encoding="utf-8") as f:
    content = f.read()

# Add White to accentOptions
old_options = """const accentOptions = [
    { value: 'blue', label: 'Blue (Default)' },
    { value: 'purple', label: 'Purple' },
    { value: 'green', label: 'Green' },
    { value: 'orange', label: 'Orange' }
  ];"""

new_options = """const accentOptions = [
    { value: 'white', label: 'Monochrome (White/Black)' },
    { value: 'blue', label: 'Deep Blue' },
    { value: 'purple', label: 'Deep Purple' },
    { value: 'green', label: 'Deep Green' },
    { value: 'orange', label: 'Deep Orange' }
  ];"""

content = content.replace(old_options, new_options)

with open("src/components/SettingsView.jsx", "w", encoding="utf-8") as f:
    f.write(content)

print("done")
