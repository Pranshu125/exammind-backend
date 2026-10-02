import re

with open("src/pages/PrepMode.jsx", "r", encoding="utf-8") as f:
    content = f.read()

pattern = re.compile(r'let markdownText = "";.*?setContent\(prev => \(\{ \.\.\.prev, \[tabId\]: markdownText \}\)\);', re.DOTALL)

good_string = r"""let markdownText = "";
        if (data.sections) {
           markdownText = data.sections.map(s => `## ${s.heading}\n${s.content}`).join('\n\n');
           markdownText += `\n\n### Summary\n${data.summary}`;
        } else if (data.detail) {
           throw new Error(data.detail);
        } else {
           markdownText = data.notes || JSON.stringify(data);
        }
        setContent(prev => ({ ...prev, [tabId]: markdownText }));"""

content = pattern.sub(good_string, content)

with open("src/pages/PrepMode.jsx", "w", encoding="utf-8") as f:
    f.write(content)

print("done")
