with open("src/components/Timetable.jsx", "w", encoding="utf-8") as f:
    f.write("""import { useState, useEffect } from 'react';
import { collection, onSnapshot } from 'firebase/firestore';
import { db } from '../lib/firebase';
import { useAuth } from '../contexts/AuthContext';
import { Calendar, CheckCircle, Clock, BookOpen, AlertCircle } from 'lucide-react';
import { Link } from 'react-router-dom';

export default function Timetable() {
  const { currentUser } = useAuth();
  const [exams, setExams] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!currentUser) return;
    const unsub = onSnapshot(collection(db, `users/${currentUser.uid}/exams`), (snap) => {
      const examsData = snap.docs.map(doc => ({ id: doc.id, ...doc.data() }));
      // Sort by creation date descending
      examsData.sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt));
      setExams(examsData);
      setLoading(false);
    });
    return () => unsub();
  }, [currentUser]);

  if (loading) return <div className="p-8 flex justify-center"><div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div></div>;

  if (exams.length === 0) {
    return (
      <div className="max-w-5xl mx-auto space-y-6 pb-12">
        <h2 className="text-3xl font-bold tracking-tight text-black mb-2">Master Timetable</h2>
        <div className="bg-white border border-gray-200 rounded-2xl p-12 text-center shadow-sm">
          <h3 className="text-xl font-bold mb-4 text-gray-900">No Timetable Yet</h3>
          <p className="text-gray-500 mb-8 max-w-md mx-auto">
            Click 'Dashboard' -> 'Create New Schedule' to get started.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-5xl mx-auto space-y-12 pb-12">
      <div className="mb-4">
        <h2 className="text-3xl font-bold tracking-tight text-black mb-2">Master Timetable</h2>
        <p className="text-gray-500">All your generated schedules.</p>
      </div>

      {exams.map((exam) => (
        <div key={exam.id} className="space-y-6">
          <div className="flex items-center gap-3 border-b border-gray-200 pb-2">
            <Calendar className="text-blue-600" size={24} />
            <h3 className="text-2xl font-bold text-gray-900">{exam.exam_name}</h3>
          </div>
          
          <div className="grid grid-cols-1 gap-6">
            {exam.schedule?.map((day, index) => (
              <div key={index} className="bg-white border border-gray-200 rounded-xl overflow-hidden shadow-sm">
                <div className="bg-gray-50 border-b border-gray-200 px-6 py-4 flex items-center justify-between">
                  <h3 className="font-bold text-lg text-gray-900">{day.day_of_week}, {day.date}</h3>
                </div>
                
                <div className="divide-y divide-gray-100">
                  {day.tasks?.length > 0 ? day.tasks.map((task, i) => (
                    <div key={i} className="p-6 flex flex-col sm:flex-row sm:items-center gap-4 hover:bg-gray-50 transition-colors">
                      <div className="flex items-start gap-4 flex-1">
                        <button className={`mt-1 flex-shrink-0 w-6 h-6 rounded-full border-2 flex items-center justify-center transition-colors ${task.completed ? 'bg-green-500 border-green-500' : 'border-gray-300'}`}>
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
                  )) : (
                    <div className="p-6 text-gray-500 text-sm flex items-center gap-2">
                       <CheckCircle size={16} className="text-gray-400" /> Rest day / No topics assigned.
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}
""")
print("done")
