import re

with open("src/components/UploadComponent.jsx", "r", encoding="utf-8") as f:
    content = f.read()

# Add imports for Firestore
add_imports = """import { doc, setDoc } from 'firebase/firestore';
import { db } from '../lib/firebase';"""
if "doc, setDoc" not in content:
    content = content.replace("import { ref, uploadBytes, getDownloadURL } from 'firebase/storage';", "import { ref, uploadBytes, getDownloadURL } from 'firebase/storage';\n" + add_imports)

# Add state for extracted topics and generating plan
state_hooks = """  const [extractedTopics, setExtractedTopics] = useState({});
  const [generatingPlan, setGeneratingPlan] = useState(false);"""
if "extractedTopics" not in content:
    content = content.replace("const [processingSubjectId, setProcessingSubjectId] = useState(null);", "const [processingSubjectId, setProcessingSubjectId] = useState(null);\n" + state_hooks)

# Modify handleProcessSubjectSyllabus
old_process = """        const data = await response.json();
        setSyllabusData(data);
        alert(`Syllabus for subject successfully processed!`);"""

new_process = """        const data = await response.json();
        setExtractedTopics(prev => ({ ...prev, [subjectId]: data.topics || [] }));
        alert(`Syllabus for subject successfully processed!`);"""
content = content.replace(old_process, new_process)

# Add Generate Master Plan function
gen_plan_func = """
  const handleGenerateMasterPlan = async () => {
    if (Object.keys(extractedTopics).length === 0) return alert("Please extract topics for at least one subject.");
    
    setGeneratingPlan(true);
    try {
      // Build request payload
      const payload = {
        exam_name: manualData.examName || "My Exam",
        engine: engine,
        subjects: extractedSubjects.filter(s => extractedTopics[s.id]).map(s => ({
          name: s.name,
          date: s.date,
          time: s.time,
          topics: extractedTopics[s.id]
        }))
      };

      const isLocalhost = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
      const API_BASE = isLocalhost ? 'http://localhost:8000' : (import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000');
      
      const response = await fetch(`${API_BASE}/api/generate-master-schedule`, {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'Bypass-Tunnel-Reminder': 'true' 
        },
        body: JSON.stringify(payload)
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || "Failed to generate schedule.");
      }

      const scheduleData = await response.json();
      
      // Save to Firestore
      const examId = Date.now().toString();
      await setDoc(doc(db, `users/${currentUser.uid}/exams`, examId), {
        ...scheduleData,
        createdAt: new Date().toISOString()
      });

      alert("Master schedule generated successfully!");
      navigate(`/exam/${examId}`);
      
    } catch (error) {
      console.error(error);
      alert(`Generation failed: ${error.message}`);
    } finally {
      setGeneratingPlan(false);
    }
  };
"""
if "handleGenerateMasterPlan" not in content:
    content = content.replace("return (", gen_plan_func + "\n  return (")


# Add visual checkmark and Generate Master Plan button in Step 2
# Add checkmark
old_extract_btn = """                            <button 
                              onClick={() => handleProcessSubjectSyllabus(subject.id)}"""
new_extract_btn = """                            {extractedTopics[subject.id] ? (
                               <div className="flex items-center gap-2 text-green-600 font-medium py-2 px-4 bg-green-50 rounded-lg border border-green-200">
                                 <CheckCircle size={18} /> Topics Extracted
                               </div>
                            ) : (
                            <button 
                              onClick={() => handleProcessSubjectSyllabus(subject.id)}"""

content = content.replace(old_extract_btn, new_extract_btn)
content = content.replace("</button>\n                          </div>", "</button>\n                            )}\n                          </div>")

# Add Generate button at the bottom of Syllabus section
old_end = """           </div>
        </div>
      )}
    </div>"""

new_end = """           </div>
             
             {Object.keys(extractedTopics).length > 0 && (
               <div className="mt-10 pt-6 border-t border-gray-200 flex justify-end">
                 <button 
                   onClick={handleGenerateMasterPlan}
                   disabled={generatingPlan}
                   className="btn-primary py-3 px-8 text-base shadow-md disabled:opacity-50 flex items-center"
                 >
                   {generatingPlan ? <><Loader2 className="animate-spin mr-2" size={20}/> Generating AI Schedule...</> : <><Sparkles className="mr-2" size={20}/> Generate Master Schedule</>}
                 </button>
               </div>
             )}
        </div>
      )}
    </div>"""
content = content.replace(old_end, new_end)


with open("src/components/UploadComponent.jsx", "w", encoding="utf-8") as f:
    f.write(content)
print("done")
