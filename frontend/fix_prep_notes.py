import re

with open("src/pages/PrepMode.jsx", "r", encoding="utf-8") as f:
    content = f.read()

# Add Bypass-Tunnel-Reminder to all fetch calls
content = content.replace("headers: { 'Content-Type': 'application/json' }", "headers: { 'Content-Type': 'application/json', 'Bypass-Tunnel-Reminder': 'true' }")

# Fix generating notes processing
old_notes_processing = """const res = await fetch(`${API_BASE}/api/generate-notes`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', 'Bypass-Tunnel-Reminder': 'true' },
          body: JSON.stringify({ topic_name: decodedTopic, engine })
        });
        const data = await res.json();
        setContent(prev => ({ ...prev, [tabId]: data.notes }));"""

new_notes_processing = """const res = await fetch(`${API_BASE}/api/generate-notes`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', 'Bypass-Tunnel-Reminder': 'true' },
          body: JSON.stringify({ topic_name: decodedTopic, engine })
        });
        const data = await res.json();
        let markdownText = "";
        if (data.sections) {
           markdownText = data.sections.map(s => `## ${s.heading}\n${s.content}`).join('\\n\\n');
           markdownText += `\\n\\n### Summary\\n${data.summary}`;
        } else if (data.detail) {
           throw new Error(data.detail);
        } else {
           markdownText = data.notes || JSON.stringify(data);
        }
        setContent(prev => ({ ...prev, [tabId]: markdownText }));"""

content = content.replace(old_notes_processing, new_notes_processing)

with open("src/pages/PrepMode.jsx", "w", encoding="utf-8") as f:
    f.write(content)

print("done")
