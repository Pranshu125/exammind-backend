with open("src/pages/PrepMode.jsx", "r", encoding="utf-8") as f:
    lines = f.readlines()

new_lines = []
skip = False
for line in lines:
    if 'let markdownText = "";' in line:
        skip = True
        new_lines.append('        let markdownText = "";\n')
        new_lines.append('        if (data.sections) {\n')
        new_lines.append('           markdownText = data.sections.map(s => `## ${s.heading}\\n${s.content}`).join(\'\\n\\n\');\n')
        new_lines.append('           markdownText += `\\n\\n### Summary\\n${data.summary}`;\n')
        new_lines.append('        } else if (data.detail) {\n')
        new_lines.append('           throw new Error(data.detail);\n')
        new_lines.append('        } else {\n')
        new_lines.append('           markdownText = data.notes || JSON.stringify(data);\n')
        new_lines.append('        }\n')
        new_lines.append('        setContent(prev => ({ ...prev, [tabId]: markdownText }));\n')
        continue
    
    if skip:
        if 'setContent(prev => ({ ...prev, [tabId]: markdownText }));' in line:
            skip = False
        continue
        
    new_lines.append(line)

with open("src/pages/PrepMode.jsx", "w", encoding="utf-8") as f:
    f.writelines(new_lines)

print("done")
