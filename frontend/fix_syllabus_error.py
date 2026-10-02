with open("src/components/UploadComponent.jsx", "r", encoding="utf-8") as f:
    content = f.read()

old_catch = """      } catch (err) {
      console.error(err);
      alert('Upload failed. Please verify backend connection.');
    } finally {
      setProcessingSubjectId(null);
    }"""

# Actually let's just do a regex replace to catch any variant of the catch block in handleProcessSubjectSyllabus
import re
new_catch = """      } catch (err) {
      console.error("Syllabus extraction error:", err);
      alert(`Extraction failed: ${err.message || 'Please verify backend connection.'}`);
    } finally {
      setProcessingSubjectId(null);
    }"""

# Wait, let's just manually replace it safely.
