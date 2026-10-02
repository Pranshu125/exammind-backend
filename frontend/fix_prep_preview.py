with open("src/pages/PrepMode.jsx", "r", encoding="utf-8") as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if "Failed to generate notes" in line:
        new_lines.append("      if (tabId === 'notes') setContent(prev => ({ ...prev, [tabId]: `Failed to generate notes: ${error.message}` }));\n")
    elif "max-h-[600px]" in line:
        new_lines.append(line.replace("max-h-[600px]", "max-h-[250px]"))
    elif "h-64" in line:
        new_lines.append(line.replace("h-64", "h-32"))
    else:
        new_lines.append(line)

with open("src/pages/PrepMode.jsx", "w", encoding="utf-8") as f:
    f.writelines(new_lines)

print("done")
