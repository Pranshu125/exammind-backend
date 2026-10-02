with open("src/components/HomeDashboard.jsx", "r", encoding="utf-8") as f:
    content = f.read()

new_content = """import React, { useState, useEffect } from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from 'recharts';
import { Clock, BookOpen, AlertCircle, Plus, Calendar as CalendarIcon } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { db } from '../lib/firebase';
import { collection, query, getDocs, onSnapshot } from 'firebase/firestore';

const HomeDashboard = () => {
  const navigate = useNavigate();
  const { currentUser } = useAuth();
  const [exams, setExams] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!currentUser) return;
    const q = query(collection(db, `users/${currentUser.uid}/exams`));
    const unsubscribe = onSnapshot(q, (snapshot) => {
      const examList = [];
      snapshot.forEach(doc => examList.push({ id: doc.id, ...doc.data() }));
      setExams(examList);
      setLoading(false);
    });
    return () => unsubscribe();
  }, [currentUser]);

  if (loading) {
    return <div className="p-8 flex justify-center"><div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div></div>;
  }

  // Calculate real metrics
  let totalTasks = 0;
  let completedTasks = 0;
  let nextExamName = "No Upcoming Exams";
  let nextExamDays = "-";
  let nextExamTopicsRemaining = 0;
  let topicsBehindToday = 0;

  if (exams.length > 0) {
    // Find closest exam date
    let closestDate = null;
    let closestExam = null;
    
    exams.forEach(exam => {
        let isExamBehind = 0;
        let examTotal = 0;
        let examCompleted = 0;
        
        exam.schedule?.forEach(day => {
            day.tasks?.forEach(task => {
                totalTasks++;
                if (task.completed) {
                    completedTasks++;
                    examCompleted++;
                }
            });
        });
        
        // Very basic logic for next exam just taking the first one for now
        if (!closestExam) {
            closestExam = exam;
            nextExamName = exam.exam_name || "Exam";
            nextExamTopicsRemaining = exam.schedule?.reduce((acc, day) => acc + (day.tasks?.filter(t => !t.completed).length || 0), 0) || 0;
            // Fake days to go for now unless we parse real dates
            nextExamDays = exam.schedule?.length || 0; 
        }
    });
  }

  const data = [
    { name: 'Completed', value: completedTasks },
    { name: 'Remaining', value: totalTasks - completedTasks },
  ];
  const COLORS = ['#22c55e', '#e5e7eb'];

  return (
    <div className="flex flex-col h-full space-y-6">
      
      {/* Header */}
      <div className="flex justify-between items-center mb-4">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">Dashboard</h2>
          <p className="text-sm text-gray-500">Track your exam preparation progress</p>
        </div>
        <button 
          onClick={() => navigate('/new-exam')}
          className="flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors"
        >
          <Plus size={16} />
          Create New Schedule
        </button>
      </div>

      {exams.length === 0 ? (
        <div className="bg-white border-2 border-dashed border-gray-300 rounded-2xl p-12 flex flex-col items-center justify-center text-center">
            <div className="bg-blue-50 p-4 rounded-full mb-4">
                <CalendarIcon size={32} className="text-blue-500" />
            </div>
            <h3 className="text-xl font-bold text-gray-900 mb-2">No Timetable Set</h3>
            <p className="text-gray-500 mb-6 max-w-md">You haven't generated any study schedules yet. Upload your timetable and syllabus to let AI build your perfect plan!</p>
            <button 
                onClick={() => navigate('/new-exam')}
                className="btn-primary py-2.5 px-6"
            >
                Start New Schedule
            </button>
        </div>
      ) : (
        <>
            {/* Main Stats Row */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                
                {/* Progress Pie Chart */}
                <div className="bg-white p-6 rounded-xl border border-gray-200 shadow-sm flex flex-col items-center justify-center">
                <h3 className="text-lg font-semibold mb-4 w-full text-left">Overall Progress</h3>
                {totalTasks > 0 ? (
                    <>
                        <div className="h-48 w-full relative">
                            <ResponsiveContainer width="100%" height="100%">
                            <PieChart>
                                <Pie
                                data={data}
                                cx="50%"
                                cy="50%"
                                innerRadius={60}
                                outerRadius={80}
                                fill="#8884d8"
                                paddingAngle={5}
                                dataKey="value"
                                >
                                {data.map((entry, index) => (
                                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                                ))}
                                </Pie>
                                <Tooltip />
                            </PieChart>
                            </ResponsiveContainer>
                            <div className="absolute inset-0 flex items-center justify-center flex-col pointer-events-none">
                                <span className="text-2xl font-bold text-gray-800">{Math.round((completedTasks/totalTasks)*100)}%</span>
                            </div>
                        </div>
                        <div className="flex gap-4 text-sm mt-2">
                            <div className="flex items-center gap-1"><div className="w-3 h-3 rounded-full bg-green-500"></div> {completedTasks} Completed</div>
                            <div className="flex items-center gap-1"><div className="w-3 h-3 rounded-full bg-gray-200"></div> {totalTasks - completedTasks} Remaining</div>
                        </div>
                    </>
                ) : (
                    <div className="h-48 flex items-center justify-center text-gray-400">No tasks found.</div>
                )}
                </div>

                {/* Subject Card */}
                <div className="bg-white p-6 rounded-xl border border-gray-200 shadow-sm flex flex-col">
                <div className="border-b border-gray-100 pb-4 mb-4">
                    <h3 className="text-lg font-semibold truncate">{nextExamName}</h3>
                    <p className="text-sm text-gray-500">Next Upcoming Exam</p>
                </div>
                
                <div className="flex-1 flex flex-col justify-center space-y-4">
                    <div className="flex items-center gap-3">
                    <div className="p-3 bg-blue-50 text-blue-600 rounded-lg">
                        <Clock size={24} />
                    </div>
                    <div>
                        <p className="text-2xl font-bold">{nextExamDays} Days</p>
                        <p className="text-sm text-gray-500">Duration</p>
                    </div>
                    </div>
                    
                    <div className="flex items-center gap-3">
                    <div className="p-3 bg-orange-50 text-orange-600 rounded-lg">
                        <BookOpen size={24} />
                    </div>
                    <div>
                        <p className="text-2xl font-bold">{nextExamTopicsRemaining} Topics</p>
                        <p className="text-sm text-gray-500">Remaining</p>
                    </div>
                    </div>
                </div>
                </div>
            </div>

            {/* Alert Banner */}
            {topicsBehindToday > 0 && (
                <div className="bg-red-50 border border-red-200 rounded-xl p-4 flex items-start sm:items-center gap-3">
                    <AlertCircle className="text-red-500 shrink-0 mt-0.5 sm:mt-0" size={20} />
                    <p className="text-red-800 text-sm font-medium">
                    You are behind the timeline! <span className="font-bold">{topicsBehindToday} topic(s) remain</span> for today.
                    </p>
                </div>
            )}
        </>
      )}

    </div>
  );
};

export default HomeDashboard;
"""

with open("src/components/HomeDashboard.jsx", "w", encoding="utf-8") as f:
    f.write(new_content)

print("done")
