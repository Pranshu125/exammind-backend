content = """import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { doc, getDoc } from 'firebase/firestore';
import { db } from '../lib/firebase';
import { useAuth } from '../contexts/AuthContext';
import { Calendar, CheckCircle, Clock, BookOpen, AlertCircle } from 'lucide-react';

export default function ExamDashboard() {
  const { id } = useParams();
  const { currentUser } = useAuth();
  const [examData, setExamData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!currentUser || !id) return;
    
    const fetchExam = async () => {
      try {
        const docRef = doc(db, `users/${currentUser.uid}/exams`, id);
        const docSnap = await getDoc(docRef);
        if (docSnap.exists()) {
          setExamData(docSnap.data());
        } else {
          console.log("No such exam!");
        }
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    
    fetchExam();
  }, [currentUser, id]);

  if (loading) return <div className="p-8 flex justify-center"><div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div></div>;
  if (!examData) return <div className="p-8 text-center text-gray-500">Exam not found.</div>;

  return (
    <div className="space-y-6 max-w-6xl mx-auto pb-12">
      <div className="bg-white border border-gray-200 p-8 rounded-2xl shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-black mb-2">{examData.exam_name}</h1>
          <p className="text-gray-500 flex items-center gap-2">
            <Calendar size={16} /> Daily Study Schedule & Checklist
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 gap-6">
        {examData.schedule?.map((day, index) => (
          <div key={index} className="bg-white border border-gray-200 rounded-xl overflow-hidden shadow-sm">
            <div className="bg-gray-50 border-b border-gray-200 px-6 py-4 flex items-center justify-between">
              <h3 className="font-bold text-lg text-gray-900">{day.day_of_week}, {day.date}</h3>
            </div>
            
            <div className="divide-y divide-gray-100">
              {day.tasks?.map((task, i) => (
                <div key={i} className="p-6 flex flex-col sm:flex-row sm:items-center gap-4 hover:bg-gray-50 transition-colors">
                  <div className="flex items-start gap-4 flex-1">
                    <button className={`mt-1 flex-shrink-0 w-6 h-6 rounded-full border-2 flex items-center justify-center transition-colors ${task.completed ? 'bg-green-500 border-green-500' : 'border-gray-300 hover:border-gray-400'}`}>
                      {task.completed && <CheckCircle size={14} className="text-white" />}
                    </button>
                    <div>
                      <div className="flex items-center gap-2 mb-1">
                        <span className="text-xs font-bold uppercase tracking-wider text-blue-600 bg-blue-50 px-2 py-0.5 rounded">{task.subject}</span>
                        <span className="text-xs font-bold uppercase tracking-wider text-purple-600 bg-purple-50 px-2 py-0.5 rounded">{task.task_type}</span>
                      </div>
                      <h4 className="text-gray-900 font-medium text-lg leading-tight">{task.topic}</h4>
                    </div>
                  </div>
                  
                  <div className="flex items-center gap-4 sm:border-l sm:border-gray-200 sm:pl-6">
                    <div className="flex items-center gap-1.5 text-gray-500 text-sm font-medium">
                      <Clock size={16} /> {task.duration_minutes} min
                    </div>
                    <Link to="/notes" className="btn-base border border-gray-200 bg-white shadow-sm hover:bg-gray-50 px-3 py-1.5 text-sm rounded-lg flex items-center gap-1.5 text-gray-700">
                      <BookOpen size={14} /> AI Notes
                    </Link>
                  </div>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
"""
with open("src/pages/ExamDashboard.jsx", "w", encoding="utf-8") as f:
    f.write(content)

with open("src/App.jsx", "r", encoding="utf-8") as f:
    app_jsx = f.read()

if "ExamDashboard" not in app_jsx:
    app_jsx = app_jsx.replace("import Dashboard from './pages/Dashboard';", "import Dashboard from './pages/Dashboard';\nimport ExamDashboard from './pages/ExamDashboard';")
    app_jsx = app_jsx.replace("<Route path=\"/timetable\" element={<Timetable />} />", "<Route path=\"/timetable\" element={<Timetable />} />\n                <Route path=\"/exam/:id\" element={<ExamDashboard />} />")
    with open("src/App.jsx", "w", encoding="utf-8") as f:
        f.write(app_jsx)

print("done")
