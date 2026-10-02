with open("src/components/UploadComponent.jsx", "r", encoding="utf-8") as f:
    content = f.read()

old_func = """  const handleExtractTimetable = () => {
    if (inputMode === 'upload' && !timetableFile) return;
    
    if (inputMode === 'manual') {
      if (!manualData.examName.trim()) return alert("Please enter an Exam Name.");
      const hasEmptySubject = manualData.subjects.some(s => !s.name.trim() || !s.date || !s.time);
      if (hasEmptySubject) return alert("Please fill in all subject details.");
    }

    setExtractingTimetable(true);
    
    // Mock extraction process
    setTimeout(() => {
      setExtractingTimetable(false);
      
      if (inputMode === 'manual') {
        setExtractedSubjects(manualData.subjects);
      } else {
        // Mock extracted data from a PDF
        setExtractedSubjects([
          { id: 1, name: "Database Management Systems", date: "2026-10-15", time: "10:00" },
          { id: 2, name: "Operating Systems", date: "2026-10-17", time: "14:00" }
        ]);
        setManualData(prev => ({ ...prev, examName: "Extracted Exam (Mock)" }));
      }
      
      setStep(2);
    }, 1500);
  };"""

new_func = """  const handleExtractTimetable = async () => {
    if (inputMode === 'upload' && !timetableFile) return;
    
    if (inputMode === 'manual') {
      if (!manualData.examName.trim()) return alert("Please enter an Exam Name.");
      const hasEmptySubject = manualData.subjects.some(s => !s.name.trim() || !s.date || !s.time);
      if (hasEmptySubject) return alert("Please fill in all subject details.");
    }

    setExtractingTimetable(true);
    
    if (inputMode === 'manual') {
      setTimeout(() => {
        setExtractingTimetable(false);
        setExtractedSubjects(manualData.subjects);
        setStep(2);
      }, 500);
    } else {
      try {
        const formData = new FormData();
        formData.append('file', timetableFile);
        formData.append('engine', engine);

        const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
        const response = await fetch(`${API_BASE}/api/upload-timetable`, {
          method: 'POST',
          headers: { 'Bypass-Tunnel-Reminder': 'true' },
          body: formData,
        });

        if (!response.ok) throw new Error("Backend parsing failed");
        
        const data = await response.json();
        // Fallback IDs if backend doesn't provide them
        const subjectsWithIds = (data.subjects || []).map((s, i) => ({ ...s, id: s.id || Date.now() + i }));
        
        setExtractedSubjects(subjectsWithIds);
        setManualData(prev => ({ ...prev, examName: data.exam_name || "Extracted Exam" }));
        setStep(2);
      } catch (err) {
        console.error(err);
        alert('Extraction failed. Please verify the file and connection.');
      } finally {
        setExtractingTimetable(false);
      }
    }
  };"""

content = content.replace(old_func, new_func)

# Remove the Go To Checklist button
checklist_code = """             {/* Final Proceed Button */}
             <div className="mt-8 pt-6 border-t border-gray-200 flex justify-end">
               <button 
                 onClick={() => navigate('/timetable')}
                 className="flex items-center gap-2 text-blue-600 hover:text-blue-700 font-semibold px-4 py-2 hover:bg-blue-50 rounded-lg transition-colors"
               >
                 Go to Checklist <ArrowRight size={18} />
               </button>
             </div>"""

content = content.replace(checklist_code, "")

with open("src/components/UploadComponent.jsx", "w", encoding="utf-8") as f:
    f.write(content)
print("done")
