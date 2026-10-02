import React, { useState, useEffect } from 'react';
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

  
  // Local Date Sync logic
  const todayDateObj = new Date();
  const todayStr = todayDateObj.toISOString().split('T')[0];
  
  let totalTasks = 0;
  let completedTasks = 0;
  let nextExamName = "No Upcoming Exams";
  let nextExamDays = "-";
  let nextExamTopicsRemaining = 0;
  let topicsBehindToday = 0;
  let todaysTasksList = [];
  let nextExamId = null;

  if (exams.length > 0) {
    exams.forEach(exam => {
        let isExamBehind = 0;
        
        exam.schedule?.forEach(day => {
            const isToday = (day.date === todayStr);
            
            day.tasks?.forEach(task => {
                totalTasks++;
                if (task.completed) {
                    completedTasks++;
                } else if (isToday) {
                    topicsBehindToday++;
                }
                
                if (isToday) {
                    todaysTasksList.push({
                       ...task,
                       examName: exam.exam_name,
                       examId: exam.id
                    });
                }
            });
        });
        
        if (!nextExamId) {
            nextExamId = exam.id;
            nextExamName = exam.exam_name || "Exam";
            nextExamTopicsRemaining = exam.schedule?.reduce((acc, day) => acc + (day.tasks?.filter(t => !t.completed).length || 0), 0) || 0;
            nextExamDays = exam.schedule?.length || 0; 
        }
    });
  }


  const data = [
    { name: 'Completed', value: completedTasks },
    { name: 'Remaining', value: totalTasks - completedTasks },
  ];
  const COLORS = ['var(--matte-primary)', 'var(--matte-primary-light)'];

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
                            <div className="flex items-center gap-1"><div className="w-3 h-3 rounded-full" style={{ backgroundColor: 'var(--matte-primary)' }}></div> {completedTasks} Completed</div>
                            <div className="flex items-center gap-1"><div className="w-3 h-3 rounded-full" style={{ backgroundColor: 'var(--matte-primary-light)' }}></div> {totalTasks - completedTasks} Remaining</div>
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
                    You have <span className="font-bold">{topicsBehindToday} task(s)</span> scheduled for today that need your attention!
                    </p>
                </div>
            )}
            
            {/* Today's Tasks Section */}
            {todaysTasksList.length > 0 ? (
              <div className="bg-white p-6 rounded-xl border border-gray-200 shadow-sm">
                <h3 className="text-lg font-bold text-gray-900 mb-4 flex items-center gap-2"><CalendarIcon size={20} className="text-[var(--matte-primary)]"/> Today's Scheduled Tasks</h3>
                <div className="space-y-3">
                  {todaysTasksList.map((task, idx) => (
                    <div key={idx} className={`p-4 rounded-xl border flex items-center justify-between transition-all ${task.completed ? 'bg-gray-50 border-gray-100' : 'bg-white border-gray-200 hover:border-blue-300'}`}>
                      <div>
                        <div className="flex items-center gap-2 mb-1">
                          <span className="text-xs font-bold text-gray-500 uppercase">{task.examName}</span>
                          <span className="w-1 h-1 rounded-full bg-gray-300"></span>
                          <span className="text-xs font-bold text-blue-600 uppercase">{task.task_type}</span>
                        </div>
                        <p className={`font-semibold ${task.completed ? 'text-gray-400 line-through' : 'text-gray-900'}`}>{task.topic}</p>
                      </div>
                      <button onClick={() => navigate(`/exam/${task.examId}`)} className="text-sm font-medium text-blue-600 hover:text-blue-700 bg-blue-50 hover:bg-blue-100 px-4 py-2 rounded-lg transition-colors">
                        View
                      </button>
                    </div>
                  ))}
                </div>
              </div>
            ) : (
              <div className="bg-gray-50 p-6 rounded-xl border border-gray-200 flex flex-col items-center justify-center text-center">
                <CalendarIcon size={32} className="text-gray-300 mb-2" />
                <h3 className="text-gray-900 font-bold mb-1">No tasks for today!</h3>
                <p className="text-gray-500 text-sm">You are all caught up on your scheduled local time ({todayStr}).</p>
              </div>
            )}

        </>
      )}

    </div>
  );
};

export default HomeDashboard;
