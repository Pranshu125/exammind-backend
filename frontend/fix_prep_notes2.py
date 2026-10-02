import re

with open("src/pages/PrepMode.jsx", "r", encoding="utf-8") as f:
    content = f.read()

bad_string = """let markdownText = "";
        if (data.sections) {
           markdownText = data.sections.map(s => `## ${s.heading}
${s.content}`).join('\n\n');
           markdownText += `\n\n### Summary\n${data.summary}`;
        } else if (data.detail) {
           throw new Error(data.detail);
        } else {
           markdownText = data.notes || JSON.stringify(data);
        }"""

good_string = """let markdownText = "";
        if (data.sections) {
           markdownText = data.sections.map(s => `## ${s.heading}\\n${s.content}`).join('\\n\\n');
           markdownText += `\\n\\n### Summary\\n${data.summary}`;
        } else if (data.detail) {
           throw new Error(data.detail);
        } else {
           markdownText = data.notes || JSON.stringify(data);
        }"""

content = content.replace(bad_string, good_string)

with open("src/pages/PrepMode.jsx", "w", encoding="utf-8") as f:
    f.write(content)

print("done")
