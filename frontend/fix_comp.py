import urllib.request
content = """import { useState } from 'react';
import { UploadCloud, FileText, Loader2, Lock, CheckCircle, Plus, Trash2, Edit3, ArrowRight, Sparkles } from 'lucide-react';
import { doc, setDoc } from 'firebase/firestore';
import { db } from '../lib/firebase';
import { useAuth } from '../contexts/AuthContext';
import { useAI } from '../contexts/AIContext';
import { useNavigate } from 'react-router-dom';

export default function UploadComponent() {
  const [step, setStep] = useState(1);
  const [inputMode, setInputMode] = useState('upload');
  const [timetableFile, setTimetableFile] = useState(null);
  const [manualData, setManualData] = useState({
    examName: '',
    subjects: [{ id: Date.now(), name: '', date: '', time: '' }]
  });
  const [extractedSubjects, setExtractedSubjects] = useState([]);
  const [extractingTimetable, setExtractingTimetable] = useState(false);
  const [subjectSyllabi, setSubjectSyllabi] = useState({});
  const [processingSubjectId, setProcessingSubjectId] = useState(null);
  const [extractedTopics, setExtractedTopics] = useState({});
  const [generatingPlan, setGeneratingPlan] = useState(false);
  
  const { currentUser } = useAuth();
  const { engine } = useAI();
  const navigate = useNavigate();

  const handleExtractTimetable = async () => {
    if (inputMode === 'upload' && !timetableFile) return;
    if (inputMode === 'manual') {
      if (!manualData.examName.trim()) return alert("Please enter an Exam Name.");
      if (manualData.subjects.some(s => !s.name.trim() || !s.date || !s.time)) return alert("Please fill in all subject details.");
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
        const isLocalhost = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
        const API_BASE = isLocalhost ? 'http://localhost:8000' : (import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000');
        const response = await fetch(`${API_BASE}/api/upload-timetable`, {
          method: 'POST',
          headers: { 'Bypass-Tunnel-Reminder': 'true' },
          body: formData,
        });
        if (!response.ok) throw new Error("Backend parsing failed");
        const data = await response.json();
        const subjectsWithIds = (data.subjects || []).map((s, i) => ({ ...s, id: s.id || Date.now() + i }));
        setExtractedSubjects(subjectsWithIds);
        setManualData(prev => ({ ...prev, examName: data.exam_name || "Extracted Exam" }));
        setStep(2);
      } catch (err) {
        alert(`Extraction failed: ${err.message}`);
      } finally {
        setExtractingTimetable(false);
      }
    }
  };

  const handleAddSubject = () => setManualData(prev => ({ ...prev, subjects: [...prev.subjects, { id: Date.now(), name: '', date: '', time: '' }] }));
  const handleRemoveSubject = (id) => setManualData(prev => ({ ...prev, subjects: prev.subjects.filter(s => s.id !== id) }));
  const handleSubjectChange = (id, field, value) => setManualData(prev => ({ ...prev, subjects: prev.subjects.map(s => s.id === id ? { ...s, [field]: value } : s) }));
  const handleSyllabusAction = (subjectId, type, fileOrText) => setSubjectSyllabi(prev => ({ ...prev, [subjectId]: { type, content: fileOrText } }));

  const handleProcessSubjectSyllabus = async (subjectId) => {
    const syllabusInfo = subjectSyllabi[subjectId];
    if (!syllabusInfo || !syllabusInfo.content || !currentUser) return;
    setProcessingSubjectId(subjectId);
    try {
      const formData = new FormData();
      formData.append('engine', engine);
      if (syllabusInfo.type === 'file') formData.append('file', syllabusInfo.content);
      else formData.append('text', syllabusInfo.content);
      const isLocalhost = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
      const API_BASE = isLocalhost ? 'http://localhost:8000' : (import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000');
      const response = await fetch(`${API_BASE}/api/upload`, {
        method: 'POST',
        headers: { 'Bypass-Tunnel-Reminder': 'true' },
        body: formData,
      });
      if (!response.ok) throw new Error("Backend parsing failed");
      const data = await response.json();
      setExtractedTopics(prev => ({ ...prev, [subjectId]: data.topics || [] }));
      alert(`Syllabus successfully processed!`);
    } catch (err) {
      alert(`Upload failed: ${err.message}`);
    } finally {
      setProcessingSubjectId(null);
    }
  };

  const handleGenerateMasterPlan = async () => {
    if (Object.keys(extractedTopics).length === 0) return alert("Please extract topics for at least one subject.");
    setGeneratingPlan(true);
    try {
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
        headers: { 'Content-Type': 'application/json', 'Bypass-Tunnel-Reminder': 'true' },
        body: JSON.stringify(payload)
      });
      if (!response.ok) throw new Error("Failed to generate schedule.");
      const scheduleData = await response.json();
      const examId = Date.now().toString();
      await setDoc(doc(db, `users/${currentUser.uid}/exams`, examId), {
        ...scheduleData,
        createdAt: new Date().toISOString()
      });
      alert("Master schedule generated successfully!");
      navigate(`/exam/${examId}`);
    } catch (error) {
      alert(`Generation failed: ${error.message}`);
    } finally {
      setGeneratingPlan(false);
    }
  };

  return (
    <div className="space-y-6 max-w-5xl mx-auto pb-12">
      <div className="mb-4">
        <h1 className="text-3xl font-bold tracking-tight text-black mb-2">Create New Schedule</h1>
        <p className="text-gray-500">
          {step === 1 ? "Upload or manually enter your exam timetable." : "Upload a syllabus for each subject in your timetable."}
        </p>
      </div>

      {step === 1 && (
        <div className="bg-white border border-gray-200 rounded-2xl p-8 shadow-sm flex flex-col w-full">
          <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between mb-8 gap-4">
            <h3 className="text-xl font-bold">Timetable Data</h3>
            <div className="flex bg-gray-100 p-1 rounded-lg">
              <button onClick={() => setInputMode('upload')} className={`px-4 py-2 text-sm font-medium rounded-md ${inputMode === 'upload' ? 'bg-white text-blue-600 shadow-sm' : 'text-gray-500'}`}>Upload File</button>
              <button onClick={() => setInputMode('manual')} className={`px-4 py-2 text-sm font-medium rounded-md ${inputMode === 'manual' ? 'bg-white text-blue-600 shadow-sm' : 'text-gray-500'}`}>Enter Manually</button>
            </div>
          </div>
          
          <div className="border-2 border-dashed border-gray-300 bg-gray-50/50 p-8 rounded-xl flex flex-col items-center">
            {inputMode === 'upload' ? (
              <div className="flex flex-col items-center justify-center w-full py-12">
                <UploadCloud size={32} className="text-gray-600 mb-4" />
                <label className="cursor-pointer btn-base mb-3 border border-gray-300 px-6 py-2 rounded-lg bg-white shadow-sm hover:bg-gray-50">
                  Choose PDF/Image
                  <input type="file" accept="application/pdf,image/*" className="hidden" onChange={e => setTimetableFile(e.target.files[0])} />
                </label>
                {timetableFile && <div className="mt-4 flex items-center gap-2 text-sm font-medium bg-white px-4 py-2 rounded-lg border border-gray-200 shadow-sm"><FileText size={16} className="text-gray-400" />{timetableFile.name}</div>}
              </div>
            ) : (
              <div className="flex flex-col w-full max-w-3xl mx-auto text-left">
                <div className="mb-6">
                  <label className="block text-sm font-medium text-gray-700 mb-2">Exam Name (e.g. CAT 2)</label>
                  <input type="text" className="w-full border border-gray-300 rounded-lg px-4 py-2.5 focus:ring-2 focus:ring-blue-500 outline-none" placeholder="Enter exam name..." value={manualData.examName} onChange={e => setManualData({...manualData, examName: e.target.value})} />
                </div>
                <div className="space-y-4 w-full">
                  <div className="flex items-center justify-between border-b border-gray-200 pb-3">
                    <label className="text-sm font-medium text-gray-700">Subjects</label>
                    <button onClick={handleAddSubject} className="text-sm flex items-center gap-1 text-blue-600 font-medium bg-blue-50 px-3 py-1.5 rounded-lg"><Plus size={14}/> Add Subject</button>
                  </div>
                  {manualData.subjects.map((subject) => (
                    <div key={subject.id} className="bg-white p-4 rounded-xl border border-gray-200 shadow-sm relative group">
                      {manualData.subjects.length > 1 && <button onClick={() => handleRemoveSubject(subject.id)} className="absolute -top-3 -right-3 bg-red-100 text-red-600 p-1.5 rounded-full shadow-sm"><Trash2 size={14} /></button>}
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div className="md:col-span-2">
                           <input type="text" placeholder="Subject Name" className="w-full border border-gray-300 rounded-lg px-3 py-2 outline-none focus:ring-2 focus:ring-blue-500" value={subject.name} onChange={e => handleSubjectChange(subject.id, 'name', e.target.value)} />
                        </div>
                        <div className="flex gap-4">
                          <input type="date" className="w-full border border-gray-300 rounded-lg px-3 py-2 outline-none focus:ring-2 focus:ring-blue-500" value={subject.date} onChange={e => handleSubjectChange(subject.id, 'date', e.target.value)} />
                          <input type="time" className="w-full border border-gray-300 rounded-lg px-3 py-2 outline-none focus:ring-2 focus:ring-blue-500" value={subject.time} onChange={e => handleSubjectChange(subject.id, 'time', e.target.value)} />
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
            <div className="mt-8 w-full max-w-sm mx-auto pt-4 border-t border-gray-200">
              <button onClick={handleExtractTimetable} disabled={extractingTimetable || (inputMode === 'upload' && !timetableFile)} className="w-full btn-primary py-3 disabled:opacity-50 text-base">
                {extractingTimetable ? <><Loader2 className="animate-spin mr-2" size={20}/> Processing...</> : (inputMode === 'upload' ? 'Extract Data' : 'Save Timetable')}
              </button>
            </div>
          </div>
        </div>
      )}

      {step === 2 && (
        <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4">
          <div className="bg-white border border-gray-200 p-6 rounded-2xl flex items-center justify-between shadow-sm">
             <div className="flex items-center gap-3">
               <CheckCircle className="text-green-500" size={24} />
               <div><h3 className="text-lg font-bold text-gray-900">Timetable Uploaded</h3><p className="text-sm text-gray-500">{manualData.examName || "Extracted Exam"}</p></div>
             </div>
             <button onClick={() => setStep(1)} className="text-sm font-medium text-blue-600 bg-blue-50 px-4 py-2 rounded-lg">Edit Timetable</button>
          </div>

          <div className="bg-white border border-gray-200 p-6 sm:p-8 rounded-2xl shadow-sm">
             <h3 className="text-xl font-bold mb-6 text-gray-900">Syllabus</h3>
             <div className="space-y-6">
                {extractedSubjects.map((subject) => {
                  const hasFile = subjectSyllabi[subject.id]?.type === 'file';
                  const hasText = subjectSyllabi[subject.id]?.type === 'text';
                  
                  return (
                   <div key={subject.id} className="flex flex-col border border-gray-200 p-4 rounded-xl shadow-sm bg-white">
                      <div className="flex flex-col lg:flex-row items-center gap-4">
                        <div className="flex-1 grid grid-cols-1 sm:grid-cols-2 bg-gray-50 p-4 rounded-lg border border-gray-200 w-full">
                           <div className="font-semibold text-gray-900">{subject.name}</div>
                           <div className="text-gray-500 text-sm mt-1 sm:mt-0 sm:text-right">{subject.date} &nbsp;•&nbsp; {subject.time}</div>
                        </div>
                        <div className="flex gap-2 w-full lg:w-auto">
                           <label className="flex-1 lg:flex-none cursor-pointer btn-base bg-white border border-gray-300 shadow-sm text-sm py-2 px-4 hover:bg-gray-50 text-center text-gray-700">
                             {hasFile ? 'Change File' : 'Upload File'}
                             <input type="file" accept="application/pdf,image/*" className="hidden" onChange={e => handleSyllabusAction(subject.id, 'file', e.target.files[0])} />
                           </label>
                           <button onClick={() => handleSyllabusAction(subject.id, 'text', '')} className={`flex-1 lg:flex-none btn-base border shadow-sm text-sm py-2 px-4 transition-colors ${hasText ? 'bg-blue-50 border-blue-200 text-blue-700' : 'bg-white border-gray-300 text-gray-700 hover:bg-gray-50'}`}>Type Manually</button>
                        </div>
                      </div>

                      {(hasFile || hasText) && (
                        <div className="mt-4 pt-4 border-t border-gray-100 flex flex-col md:flex-row gap-4 items-start md:items-center w-full animate-in fade-in zoom-in-95 duration-200">
                          <div className="flex-1 w-full">
                            {hasFile ? (
                              <div className="flex items-center gap-2 text-sm font-medium bg-blue-50/50 px-4 py-3 rounded-lg text-blue-800 border border-blue-100"><FileText size={18} className="text-blue-500" />{subjectSyllabi[subject.id].content.name}</div>
                            ) : (
                              <textarea className="w-full border border-gray-300 rounded-lg p-3 text-sm focus:ring-2 focus:ring-blue-500 outline-none" rows="3" placeholder="Paste the syllabus topics here..." value={subjectSyllabi[subject.id].content} onChange={e => handleSyllabusAction(subject.id, 'text', e.target.value)}></textarea>
                            )}
                          </div>
                          <div className="w-full md:w-auto">
                            {extractedTopics[subject.id] ? (
                               <div className="flex items-center justify-center w-full md:w-auto gap-2 text-green-600 font-medium py-2.5 px-6 bg-green-50 rounded-lg border border-green-200 shadow-sm">
                                 <CheckCircle size={18} /> Topics Extracted
                               </div>
                            ) : (
                               <button onClick={() => handleProcessSubjectSyllabus(subject.id)} disabled={processingSubjectId === subject.id || (hasText && !subjectSyllabi[subject.id].content.trim())} className="btn-primary py-2.5 px-6 whitespace-nowrap w-full md:w-auto">
                                 {processingSubjectId === subject.id ? <><Loader2 className="animate-spin mr-2" size={16}/> Processing...</> : 'Extract Topics'}
                               </button>
                            )}
                          </div>
                        </div>
                      )}
                   </div>
                  );
                })}
             </div>
             
             <div className="mt-10 pt-6 border-t border-gray-200 flex flex-col items-end">
                 {Object.keys(extractedTopics).length === 0 && (
                     <p className="text-sm text-gray-500 mb-2">Extract topics for at least one subject above to generate your plan.</p>
                 )}
                 <button 
                   onClick={handleGenerateMasterPlan}
                   disabled={generatingPlan || Object.keys(extractedTopics).length === 0}
                   className="btn-primary py-3 px-8 text-base shadow-md disabled:opacity-50 flex items-center transition-all"
                 >
                   {generatingPlan ? <><Loader2 className="animate-spin mr-2" size={20}/> Generating AI Schedule...</> : <><Sparkles className="mr-2" size={20}/> Generate Master Schedule</>}
                 </button>
             </div>
             
          </div>
        </div>
      )}
    </div>
  );
}
"""
with open("src/components/UploadComponent.jsx", "w", encoding="utf-8") as f:
    f.write(content)
print("done")
