with open("src/components/UploadComponent.jsx", "r", encoding="utf-8") as f:
    content = f.read()

import re

old_block = """        if (syllabusInfo.type === 'file') {
          const file = syllabusInfo.content;
          const storageRef = ref(storage, `syllabuses/${currentUser.uid}/${file.name}`);
          await uploadBytes(storageRef, file);
          formData.append('file', file);
        } else {"""

new_block = """        if (syllabusInfo.type === 'file') {
          const file = syllabusInfo.content;
          formData.append('file', file);
        } else {"""

content = content.replace(old_block, new_block)

with open("src/components/UploadComponent.jsx", "w", encoding="utf-8") as f:
    f.write(content)
print("done")
