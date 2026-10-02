with open("src/components/Timetable.jsx", "w", encoding="utf-8") as f:
    f.write("""import { useState, useEffect } from 'react';
import { collection, onSnapshot } from 'firebase/firestore';
import { db } from '../lib/firebase';
import { useAuth } from '../contexts/AuthContext';
import { Calendar, Clock, Book } from 'lucide-react';

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
      <div className="max-w-6xl mx-auto space-y-6 pb-12">
        <h2 className="text-3xl font-bold tracking-tight text-black mb-2">Master Timetable</h2>
        <div className="bg-white border border-gray-200 rounded-2xl p-12 text-center shadow-sm">
          <h3 className="text-xl font-bold mb-4 text-gray-900">No Timetable Yet</h3>
          <p className="text-gray-500 mb-8 max-w-md mx-auto">
            Click Dashboard and Create New Schedule to get started.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto space-y-12 pb-12">
      <div className="mb-4">
        <h2 className="text-3xl font-bold tracking-tight text-black mb-2">Master Timetable</h2>
        <p className="text-gray-500">A clean overview of all your generated schedules.</p>
      </div>

      {exams.map((exam) => (
        <div key={exam.id} className="bg-white border border-gray-200 rounded-2xl shadow-sm overflow-hidden">
          <div className="bg-gray-50 border-b border-gray-200 px-6 py-4 flex items-center justify-between">
            <h3 className="text-xl font-bold text-gray-900 flex items-center gap-2">
              <Calendar className="text-blue-600" size={20} /> {exam.exam_name}
            </h3>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="bg-white text-gray-500 text-xs uppercase tracking-wider border-b border-gray-200">
                  <th className="px-6 py-4 font-semibold w-40 border-r border-gray-100">Date & Day</th>
                  <th className="px-6 py-4 font-semibold">Subject</th>
                  <th className="px-6 py-4 font-semibold">Topic to Study</th>
                  <th className="px-6 py-4 font-semibold">Activity Type</th>
                  <th className="px-6 py-4 font-semibold text-right">Duration</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200 text-sm">
                {exam.schedule?.map((day, dayIndex) => (
                  day.tasks?.length > 0 ? day.tasks.map((task, i) => (
                    <tr key={`${day.date}-${i}`} className="hover:bg-gray-50 transition-colors group">
                      {i === 0 && (
                        <td className="px-6 py-4 whitespace-nowrap text-gray-900 font-medium border-r border-gray-100 align-top" rowSpan={day.tasks.length}>
                          <div className="flex flex-col">
                            <span className="text-sm font-bold">{day.day_of_week}</span>
                            <span className="text-xs text-gray-500 font-normal">{day.date}</span>
                          </div>
                        </td>
                      )}
                      <td className="px-6 py-4 font-medium text-gray-900">
                        <span className="text-xs font-bold uppercase tracking-wider text-blue-600 bg-blue-50 px-2 py-1 rounded-md border border-blue-100">
                          {task.subject}
                        </span>
                      </td>
                      <td className="px-6 py-4 text-gray-700 font-medium">
                        {task.topic}
                      </td>
                      <td className="px-6 py-4">
                        <span className="text-xs font-bold uppercase tracking-wider text-purple-600 bg-purple-50 px-2 py-1 rounded-md border border-purple-100">
                          {task.task_type}
                        </span>
                      </td>
                      <td className="px-6 py-4 text-gray-500 whitespace-nowrap text-right">
                        <div className="flex items-center justify-end gap-1.5 font-medium">
                          <Clock size={14} className="text-gray-400" /> {task.duration_minutes} min
                        </div>
                      </td>
                    </tr>
                  )) : (
                    <tr key={`${day.date}-rest`} className="bg-gray-50/50 hover:bg-gray-50 transition-colors">
                      <td className="px-6 py-4 whitespace-nowrap text-gray-900 font-medium border-r border-gray-100">
                        <div className="flex flex-col">
                          <span className="text-sm font-bold">{day.day_of_week}</span>
                          <span className="text-xs text-gray-500 font-normal">{day.date}</span>
                        </div>
                      </td>
                      <td colSpan="4" className="px-6 py-6 text-gray-400 italic text-center">
                        Rest day / No topics assigned
                      </td>
                    </tr>
                  )
                ))}
              </tbody>
            </table>
          </div>
        </div>
      ))}
    </div>
  );
}
""")
print("done")
