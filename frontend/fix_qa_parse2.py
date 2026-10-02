with open("src/pages/PrepMode.jsx", "r", encoding="utf-8") as f:
    content = f.read()

import re
old_str = r"parsed = JSON.parse(parsed.replace(/```json/g, '').replace(/```/g, ''));"
new_str = r"""let cleanStr = parsed.replace(/```json/g, '').replace(/```/g, '').trim();
            // Fix unescaped backslashes and newlines
            cleanStr = cleanStr.replace(/\n/g, "\\n").replace(/\r/g, "\\r").replace(/\t/g, "\\t");
            try {
              parsed = JSON.parse(cleanStr);
            } catch (e) {
              console.log("JSON Parse failed, attempting aggressive backslash fix", e);
              cleanStr = cleanStr.replace(/\\/g, "\\\\");
              parsed = JSON.parse(cleanStr);
            }"""

content = content.replace("parsed = JSON.parse(parsed.replace(/```json/g, '').replace(/```/g, ''));", new_str)

with open("src/pages/PrepMode.jsx", "w", encoding="utf-8") as f:
    f.write(content)
print("done")
