with open("src/components/UploadComponent.jsx", "r", encoding="utf-8") as f:
    c = f.read()

import re
old = r"if \(!response\.ok\) throw new Error\(\"Backend parsing failed\"\);\s*const data = await response\.json\(\);\s*// Update context[^\n]*\s*setSyllabusData\(data\);\s*alert\(`Syllabus for subject successfully processed!`\);\s*} catch \(err\) {\s*console\.error\(err\);\s*alert\('Upload failed\. Please verify backend connection\.'\);\s*} finally {\s*setProcessingSubjectId\(null\);\s*}"

new = """if (!response.ok) {
          const errorData = await response.json().catch(() => ({}));
          throw new Error(errorData.detail || "Backend parsing failed");
        }
        const data = await response.json();
        setSyllabusData(data);
        alert(`Syllabus for subject successfully processed!`);
      } catch (err) {
        console.error(err);
        alert(`Upload failed: ${err.message || 'Please verify backend connection.'}`);
      } finally {
        setProcessingSubjectId(null);
      }"""

c_new = re.sub(old, new, c)
with open("src/components/UploadComponent.jsx", "w", encoding="utf-8") as f:
    f.write(c_new)
print("done")
