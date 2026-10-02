import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { doc, getDoc, updateDoc } from 'firebase/firestore';
import { db } from '../lib/firebase';
import { useAuth } from '../contexts/AuthContext';
import { Calendar, BookOpen, Clock, Brain, Target, PlayCircle, CheckCircle2, ChevronRight, BarChart } from 'lucide-react';

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
        }
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchExam();
  }, [currentUser, id]);

  const toggleTaskCompletion = async (dayIndex, taskIndex, currentStatus) => {
    try {
      const newSchedule = JSON.parse(JSON.stringify(examData.schedule));
      newSchedule[dayIndex].tasks[taskIndex].completed = !currentStatus;
      setExamData({ ...examData, schedule: newSchedule });
      const docRef = doc(db, `users/${currentUser.uid}/exams`, id);
            await updateDoc(docRef, { schedule: newSchedule });
      try {
        const { generateAndUploadWebcal } = await import("../lib/syncCalendar");
        await generateAndUploadWebcal(currentUser);
      } catch (e) {
        console.error("Auto-sync failed:", e);
      }
    } catch (err) {
      console.error(err);
    }
  };

  if (loading) return <div className="p-8 flex justify-center"><div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div></div>;
  if (!examData) return <div className="p-8 text-center text-gray-500">Exam not found.</div>;

  // Calculate overall progress
  let totalTasks = 0;
  let completedTasks = 0;
  let totalMinutes = 0;
  
  examData.schedule?.forEach(day => {
    day.tasks?.forEach(task => {
      totalTasks++;
      if (task.completed) completedTasks++;
      totalMinutes += (task.duration_minutes || 0);
    });
  });

  const progressPercent = totalTasks === 0 ? 0 : Math.round((completedTasks / totalTasks) * 100);
  const totalHours = Math.round(totalMinutes / 60);

  
  const exportToCalendar = () => {
    let icsContent = "BEGIN:VCALENDAR\nVERSION:2.0\nPRODID:-//Exammind//Study Planner//EN\n";
    
    examData.schedule?.forEach((day, dIdx) => {
      if(!day.date) return;
      const dateParts = day.date.split('-');
      if(dateParts.length !== 3) return;
      const year = dateParts[0];
      const month = dateParts[1].padStart(2, '0');
      const date = dateParts[2].padStart(2, '0');
      
      let currentHour = 9; // default start time 9 AM
      
      day.tasks?.forEach((task, tIdx) => {
        const startHour = String(currentHour).padStart(2, '0');
        const duration = task.duration_minutes || 60;
        const endHourVal = currentHour + Math.floor(duration / 60);
        const endHour = String(endHourVal).padStart(2, '0');
        const startMin = "00";
        const endMin = String(duration % 60).padStart(2, '0');

        icsContent += "BEGIN:VEVENT\n";
        icsContent += `DTSTART:${year}${month}${date}T${startHour}${startMin}00\n`;
        icsContent += `DTEND:${year}${month}${date}T${endHour}${endMin}00\n`;
        icsContent += `SUMMARY:[${task.task_type}] ${task.subject}: ${task.topic}\n`;
        icsContent += `DESCRIPTION:Exammind AI Generated Study Session\n`;
        icsContent += "END:VEVENT\n";
        
        currentHour = endHourVal + 1; // 1 hr break/gap
      });
    });
    icsContent += "END:VCALENDAR";

    const blob = new Blob([icsContent], { type: 'text/calendar;charset=utf-8' });
    const link = document.createElement('a');
    link.href = window.URL.createObjectURL(blob);
    link.download = `${examData.exam_name.replace(/\s+/g, '_')}_Schedule.ics`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const localDateObj = new Date();
  const offset = localDateObj.getTimezoneOffset() * 60000;
  const todayStr = (new Date(localDateObj - offset)).toISOString().split('T')[0];

  const getTaskIcon = (type) => {
    switch(type?.toLowerCase()) {
      case 'revision': return <Brain className="text-purple-500" size={20} />;
      case 'practice': return <Target className="text-orange-500" size={20} />;
      default: return <BookOpen className="text-blue-500" size={20} />;
    }
  };

  return (
    <div className="space-y-8 max-w-5xl mx-auto pb-16">
      {/* Course Hero Banner */}
      <div className="bg-gradient-to-br from-gray-900 to-black text-white p-8 md:p-10 rounded-3xl shadow-lg relative overflow-hidden">
        <div className="absolute top-0 right-0 w-64 h-64 bg-white opacity-5 rounded-full blur-3xl -translate-y-1/2 translate-x-1/4"></div>
        <div className="relative z-10 flex flex-col md:flex-row md:items-end justify-between gap-6">
          <div className="space-y-4">
            <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-blue-500/20 text-blue-300 text-xs font-bold uppercase tracking-wider border border-blue-500/30">
              <BarChart size={14} /> Exam Prep Curriculum
            </span>
            <h1 className="text-4xl font-extrabold tracking-tight">{examData.exam_name}</h1>
            <p className="text-gray-400 max-w-xl text-sm md:text-base leading-relaxed">
              Your personalized AI study pathway. Complete the modules day-by-day to ensure full coverage of your syllabus before the exam.
            </p>
            <div className="pt-2">
              <button onClick={exportToCalendar} className="inline-flex items-center gap-2 px-4 py-2 bg-white text-black font-semibold rounded-xl hover:bg-gray-100 transition-colors shadow-sm">
                <Calendar size={18} /> Export to Calendar
              </button>
            </div>
          </div>
          
          <div className="bg-white/10 backdrop-blur-md border border-white/10 rounded-2xl p-5 min-w-[200px]">
            <div className="flex justify-between items-end mb-2">
              <span className="text-gray-300 text-sm font-medium">Overall Progress</span>
              <span className="text-2xl font-bold">{progressPercent}%</span>
            </div>
            <div className="w-full rounded-full h-2 mb-4" style={{ backgroundColor: 'var(--matte-primary-light)' }}>
              <div className="h-2 rounded-full transition-all duration-1000" style={{ width: `${progressPercent}%`, backgroundColor: 'var(--matte-primary)' }}></div>
            </div>
            <div className="flex justify-between text-xs text-gray-400">
              <span className="flex items-center gap-1"><BookOpen size={12}/> {totalTasks} Modules</span>
              <span className="flex items-center gap-1"><Clock size={12}/> ~{totalHours} hrs</span>
            </div>
          </div>
        </div>
      </div>

      {/* Curriculum Modules */}
      <div className="space-y-8">
        <h2 className="text-2xl font-bold tracking-tight text-gray-900 px-2">Course Curriculum</h2>
        
        <div className="space-y-6">
            {examData.schedule?.map((day, dayIndex) => {
            const hasTasks = day.tasks && day.tasks.length > 0;
            const dayCompleted = hasTasks && day.tasks.every(t => t.completed);
            const isToday = (day.date === todayStr);
            
            return (
              <div key={dayIndex} className={`bg-white border ${isToday ? 'border-blue-400 ring-2 ring-blue-100' : 'border-gray-200'} rounded-2xl overflow-hidden shadow-sm hover:shadow-md transition-shadow`}>
                {/* Module Header */}
                <div className={`p-6 flex flex-col sm:flex-row sm:items-center justify-between gap-4 ${isToday ? 'bg-blue-50/50 border-b border-blue-100' : 'bg-gray-50 border-b border-gray-200'}`}>
                  <div className="flex items-center gap-4">
                    <div className={`w-12 h-12 rounded-2xl flex items-center justify-center font-bold text-lg border-2 ${dayCompleted ? 'bg-green-500 border-green-500 text-white' : isToday ? 'bg-blue-600 border-blue-600 text-white' : 'bg-white border-gray-200 text-gray-400'}`}>
                      {dayCompleted ? <CheckCircle2 size={24} /> : dayIndex + 1}
                    </div>
                    <div>
                      <h3 className="font-bold text-xl text-gray-900 flex items-center gap-2">
                        Module {dayIndex + 1}
                        {isToday && <span className="bg-blue-100 text-blue-700 text-[10px] uppercase tracking-wider px-2 py-0.5 rounded-full">Today</span>}
                      </h3>
                      <p className="text-sm text-gray-500 font-medium">{day.day_of_week}, {day.date}</p>
                    </div>
                  </div>
                  <div className="flex items-center gap-4">
                    <div className={`w-12 h-12 rounded-2xl flex items-center justify-center font-bold text-lg border-2 ${dayCompleted ? 'bg-green-500 border-green-500 text-white' : 'bg-white border-gray-200 text-gray-400'}`}>
                      {dayCompleted ? <CheckCircle2 size={24} /> : dayIndex + 1}
                    </div>
                    <div>
                      <h3 className="font-bold text-xl text-gray-900">Module {dayIndex + 1}</h3>
                      <p className="text-sm text-gray-500 font-medium">{day.day_of_week}, {day.date}</p>
                    </div>
                  </div>
                  {hasTasks && (
                    <div className="text-sm font-semibold text-gray-400 bg-white px-3 py-1 rounded-full border border-gray-200">
                      {day.tasks.filter(t => t.completed).length} / {day.tasks.length} Lessons
                    </div>
                  )}
                </div>
                
                {/* Module Lessons */}
                <div className="p-2">
                  {!hasTasks ? (
                    <div className="p-8 text-center text-gray-400 italic font-medium">Rest Day - No lessons scheduled.</div>
                  ) : (
                    <div className="flex flex-col space-y-2">
                      {day.tasks.map((task, taskIndex) => (
                        <div key={taskIndex} className={`group flex flex-col sm:flex-row sm:items-center justify-between p-4 rounded-xl transition-all ${task.completed ? 'bg-gray-50' : 'hover:bg-blue-50/50 border border-transparent hover:border-blue-100'}`}>
                          
                          <div className="flex items-start gap-4 mb-4 sm:mb-0">
                            <div className={`mt-1 w-10 h-10 rounded-full flex items-center justify-center flex-shrink-0 ${task.completed ? 'bg-green-100 text-green-600' : 'bg-gray-100 text-gray-500 group-hover:bg-blue-100 group-hover:text-blue-600'}`}>
                              {task.completed ? <CheckCircle2 size={20} /> : getTaskIcon(task.task_type)}
                            </div>
                            
                            <div>
                              <div className="flex items-center gap-2 mb-1.5">
                                <span className="text-xs font-bold uppercase tracking-wider text-gray-500">{task.subject}</span>
                                <span className="w-1 h-1 rounded-full bg-gray-300"></span>
                                <span className={`text-xs font-bold uppercase tracking-wider ${task.completed ? 'text-gray-400' : 'text-blue-600'}`}>{task.task_type}</span>
                              </div>
                              <h4 className={`font-semibold text-lg ${task.completed ? 'text-gray-400 line-through' : 'text-gray-900'}`}>{task.topic}</h4>
                              <div className="flex items-center gap-1.5 text-sm text-gray-500 mt-1 font-medium">
                                <Clock size={14} /> {task.duration_minutes} min
                              </div>
                            </div>
                          </div>
                          
                          <div className="flex flex-wrap items-center gap-2 sm:gap-3 sm:ml-4 pl-14 sm:pl-0">
                              <Link to={`/exam/${id}/prep/${encodeURIComponent(task.topic)}`} className={`btn-base px-6 py-2.5 text-sm rounded-xl flex items-center gap-2 font-bold shadow-md transition-all ${task.completed ? 'bg-gray-100 text-gray-500 hover:bg-gray-200 dark:bg-gray-800 dark:text-gray-400' : 'bg-[var(--matte-primary)] text-white hover:opacity-90 hover:scale-105'}`}>
                                <Brain size={18} /> Enter Prep Mode
                              </Link>
                              
                              <button 
                                onClick={() => toggleTaskCompletion(dayIndex, taskIndex, task.completed)}
                                className={`p-2.5 rounded-xl flex items-center justify-center transition-colors ${task.completed ? 'bg-green-100 text-green-600 hover:bg-green-200 dark:bg-green-900/30 dark:text-green-500' : 'bg-gray-100 text-gray-400 hover:bg-gray-200 hover:text-gray-600 dark:bg-gray-800 dark:hover:bg-gray-700'}`}
                                title={task.completed ? "Mark as incomplete" : "Mark as complete"}
                              >
                                <CheckCircle2 size={20} />
                              </button>
                            </div>
                          
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
