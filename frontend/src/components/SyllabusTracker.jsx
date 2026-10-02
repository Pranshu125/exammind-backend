import { useState, useEffect } from 'react';
import { CheckCircle2, Circle, Clock } from 'lucide-react';
import { collection, onSnapshot, doc, updateDoc } from 'firebase/firestore';
import { db } from '../lib/firebase';
import { useAuth } from '../contexts/AuthContext';

export default function SyllabusTracker() {
  const { currentUser } = useAuth();
  const [todaysTasks, setTodaysTasks] = useState([]);
  const [examsData, setExamsData] = useState([]);
  const [loading, setLoading] = useState(true);

  // For testing, let's just get today's date in YYYY-MM-DD
  const today = new Date().toISOString().split('T')[0];

  useEffect(() => {
    if (!currentUser) return;
    const unsub = onSnapshot(collection(db, `users/${currentUser.uid}/exams`), (snap) => {
      const exams = snap.docs.map(doc => ({ id: doc.id, ...doc.data() }));
      setExamsData(exams);
      
      let tasksForToday = [];
      exams.forEach(exam => {
        if (exam.schedule) {
          exam.schedule.forEach((day, dayIndex) => {
            // Find tasks that match today's date, or if it's the first day (fallback for testing)
            if (day.date === today || (tasksForToday.length === 0 && dayIndex === 0)) {
              day.tasks.forEach((task, taskIdx) => {
                tasksForToday.push({
                  ...task,
                  examId: exam.id,
                  examName: exam.exam_name,
                  dayIndex,
                  taskIdx
                });
              });
            }
          });
        }
      });
      setTodaysTasks(tasksForToday);
      setLoading(false);
    });
    return () => unsub();
  }, [currentUser, today]);

  const toggleTask = async (examId, dayIndex, taskIdx, currentStatus) => {
    try {
      const exam = examsData.find(e => e.id === examId);
      if (!exam) return;
      
      // Deep clone schedule to update
      const newSchedule = JSON.parse(JSON.stringify(exam.schedule));
      newSchedule[dayIndex].tasks[taskIdx].completed = !currentStatus;
      
      const docRef = doc(db, `users/${currentUser.uid}/exams`, examId);
      await updateDoc(docRef, { schedule: newSchedule });
    } catch (err) {
      console.error("Error updating task", err);
    }
  };

  if (loading) return <div className="p-8 flex justify-center"><div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div></div>;

  return (
    <div className="max-w-4xl mx-auto space-y-6 pb-12">
      <div className="mb-8">
        <h2 className="text-3xl font-bold tracking-tight text-black mb-2">Today's Checklist</h2>
        <p className="text-gray-500">Your daily tasks across all upcoming exams.</p>
      </div>

      {todaysTasks.length === 0 ? (
        <div className="bg-white border border-gray-200 rounded-2xl p-12 text-center shadow-sm">
          <h3 className="text-xl font-bold mb-2 text-gray-900">No tasks for today!</h3>
          <p className="text-gray-500">You're all caught up, or you haven't generated a master schedule yet.</p>
        </div>
      ) : (
        <div className="bg-white rounded-2xl shadow-sm border border-gray-200 overflow-hidden">
          <div className="bg-gray-50 px-6 py-4 border-b border-gray-200 flex justify-between items-center">
             <h3 className="font-bold text-gray-900">Tasks for {new Date().toLocaleDateString()}</h3>
             <span className="text-sm font-medium bg-blue-100 text-blue-700 px-3 py-1 rounded-full">
               {todaysTasks.filter(t => t.completed).length} / {todaysTasks.length} Completed
             </span>
          </div>
          <div className="divide-y divide-gray-100">
            {todaysTasks.map((task, index) => (
              <div 
                key={`${task.examId}-${index}`} 
                onClick={() => toggleTask(task.examId, task.dayIndex, task.taskIdx, task.completed)}
                className={`flex flex-col sm:flex-row sm:items-center gap-4 p-6 cursor-pointer transition-colors hover:bg-gray-50`}
              >
                <div className="flex items-start gap-4 flex-1">
                  {task.completed ? (
                    <CheckCircle2 className="text-green-500 flex-shrink-0 mt-0.5" size={24} />
                  ) : (
                    <Circle className="text-gray-300 flex-shrink-0 mt-0.5" size={24} />
                  )}
                  <div>
                    <div className="flex flex-wrap items-center gap-2 mb-1.5">
                      <span className="inline-block text-xs font-bold uppercase tracking-wider text-blue-600 bg-blue-50 px-2 py-0.5 rounded leading-relaxed">{task.examName}</span>
                      <span className="inline-block text-xs font-bold uppercase tracking-wider text-purple-600 bg-purple-50 px-2 py-0.5 rounded leading-relaxed">{task.subject}</span>
                    </div>
                    <span className={`text-lg font-medium ${task.completed ? 'text-gray-400 line-through' : 'text-gray-900'}`}>
                      {task.topic} ({task.task_type})
                    </span>
                  </div>
                </div>
                
                <div className="flex items-center gap-2 text-gray-500 text-sm font-medium sm:border-l sm:border-gray-200 sm:pl-6">
                  <Clock size={16} /> {task.duration_minutes} min
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
