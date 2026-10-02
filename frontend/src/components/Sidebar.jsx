import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { useAI } from '../contexts/AIContext';
import { LayoutDashboard, Calendar, CheckSquare, BookOpen, HelpCircle, Settings, Cpu, User, X, Zap, Bot, BrainCircuit, Sparkles, Folder } from 'lucide-react';
import { useState, useEffect } from 'react';
import { db } from '../lib/firebase';
import { collection, query, onSnapshot } from 'firebase/firestore';

import CustomSelect from './CustomSelect';

import { PanelLeftClose } from 'lucide-react';

export default function Sidebar({ onClose, onToggleDesktop }) {
  const { currentUser } = useAuth();
  const { engine, setEngine } = useAI();
  const location = useLocation();
  const [exams, setExams] = useState([]);

  useEffect(() => {
    if (!currentUser) return;
    const q = query(collection(db, `users/${currentUser.uid}/exams`));
    const unsubscribe = onSnapshot(q, (snapshot) => {
      const examList = [];
      snapshot.forEach(doc => examList.push({ id: doc.id, ...doc.data() }));
      setExams(examList);
    });
    return () => unsubscribe();
  }, [currentUser]);

  const navItems = [
    { name: 'Dashboard', path: '/', icon: LayoutDashboard },
    { name: 'Timetable', path: '/timetable', icon: Calendar },
    { name: 'Tracker', path: '/tracker', icon: CheckSquare },
    { name: 'Notes', path: '/notes', icon: BookOpen },
    { name: 'Quizzes', path: '/quiz', icon: HelpCircle },
    
  ];

  const engineOptions = [
    { value: 'groq', label: 'Groq (Fast)', icon: <Zap size={14} /> },
    { value: 'gemini', label: 'Gemini', icon: <Sparkles size={14} /> }
  ];

  return (
    <div className="sidebar-container w-64 h-full flex flex-col relative z-50 -mr-[1px] shrink-0">
      {/* Mobile Close Button */}
      {onClose && (
        <button onClick={onClose} className="lg:hidden absolute top-4 right-4 p-2 text-gray-500 hover:text-black rounded-lg ">
          <X size={20} />
        </button>
      )}
      
      <div className="pl-4 pr-0 pt-6 pb-0">
        <div className="sidebar-title mb-8 flex items-center justify-between pr-4">
          <h1 className="text-xl font-bold tracking-tight flex items-center gap-2">
            <div className="w-8 h-8 rounded-full overflow-hidden shrink-0 border border-gray-700 shadow-sm flex items-center justify-center">
              <img src="/logo.jpg" alt="Logo" className="w-full h-full object-cover" />
            </div>
            EXAMMIND
          </h1>
          <button onClick={onToggleDesktop} className="hidden lg:flex p-1.5 text-gray-500 hover:text-white rounded-lg transition-colors" title="Close Sidebar">
            <PanelLeftClose size={20} />
          </button>
        </div>
        
        <Link 
          to="/profile"
          onClick={onClose}
          className="flex items-center gap-3 p-2 -ml-2 rounded-xl transition-all hover:bg-white/10"
        >
          <div className="h-10 w-10 rounded-full bg-white shadow-sm border border-gray-200 flex items-center justify-center text-gray-700 font-bold text-lg shrink-0 overflow-hidden">
            {currentUser?.photoURL ? (
              <img src={currentUser.photoURL} alt="Avatar" className="h-full w-full object-cover" />
            ) : currentUser?.displayName ? (
              <span className="text-blue-600">{currentUser.displayName.charAt(0).toUpperCase()}</span>
            ) : (
              <User size={16} className="text-gray-400" />
            )}
          </div>
          <div className="overflow-hidden flex flex-col justify-center">
            <p className="sidebar-title text-sm font-bold truncate">
              {currentUser?.displayName || 'User'}
            </p>
            
          </div>
        </Link>
      </div>
      
      <nav className="flex-1 pl-4 pr-0 space-y-1 pt-12 overflow-y-auto pb-12 custom-scrollbar">
                {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = location.pathname === item.path;
          return (
            <Link
              key={item.name}
              to={item.path}
              onClick={onClose}
              className={`sidebar-link flex items-center gap-3 px-3 py-2  text-sm font-medium ${isActive ? 'active' : ''}`}
            >
              <Icon size={18} className="sidebar-icon " />
              <span>{item.name}</span>
            </Link>
          );
        })}

        {exams.length > 0 && (
          <div className="pt-4 pb-1">
             <div className="sidebar-title px-0 text-[10px] font-bold uppercase tracking-wider mb-2 opacity-70">My Exams</div>
             {exams.map(exam => {
               const isActive = location.pathname === `/exam/${exam.id}`;
               return (
                 <Link
                    key={exam.id}
                    to={`/exam/${exam.id}`}
                    onClick={onClose}
                    className={`sidebar-link flex items-center gap-3 px-3 py-2  text-sm font-medium ${isActive ? 'active' : ''}`}
                  >
                    <Folder size={18} className="sidebar-icon " />
                    <span>{exam.exam_name || "Exam"}</span>
                  </Link>
               )
             })}
          </div>
        )}
      </nav>
      
      <div className="sidebar-footer pl-4 pr-0 pt-4 pb-12 mt-auto">
        <div className="pr-4 mb-6">
            <label className="sidebar-title flex items-center gap-2 text-[10px] font-semibold uppercase tracking-wider mb-2 opacity-70">
            <Cpu size={12} /> Provider
          </label>
          <CustomSelect 
            value={engine}
            onChange={(e) => setEngine(e.target.value)}
            options={engineOptions}
            className="w-full bg-white border border-gray-200 rounded-lg text-xs shadow-sm"
            direction="up"
          />
        </div>
        <Link
          to="/settings"
          onClick={onClose}
          className={`sidebar-link flex w-full items-center gap-3 px-3 py-2  text-sm font-medium ${location.pathname === '/settings' ? 'active' : ''}`}
        >
          <Settings size={18} className="sidebar-icon " />
          <span>Settings</span>
        </Link>
      </div>
    </div>
  );
}
