import { useState, useEffect } from 'react';
import { Routes, Route, useLocation, useNavigate } from 'react-router-dom';
import { useAI } from '../contexts/AIContext';
import { Menu, PanelRight, Cpu, Settings } from 'lucide-react';
import Sidebar from '../components/Sidebar';
import UploadComponent from '../components/UploadComponent';
import Timetable from '../components/Timetable';
import SyllabusTracker from '../components/SyllabusTracker';
import NotesView from '../components/NotesView';
import ProfileView from '../components/ProfileView';
import SettingsView from '../components/SettingsView';
import QuizView from '../components/QuizView';
import HomeDashboard from '../components/HomeDashboard';
import ExamDashboard from './ExamDashboard';
import PrepMode from './PrepMode';

export default function Dashboard() {
  const location = useLocation();
  const navigate = useNavigate();
  const [mobileSidebarOpen, setMobileSidebarOpen] = useState(false);
  const [desktopSidebarOpen, setDesktopSidebarOpen] = useState(true);
  const { engine, setEngine } = useAI();
  const [showEngineDropdown, setShowEngineDropdown] = useState(false);

  // Auto-collapse sidebar on deep routes to save space
  useEffect(() => {
    if (location.pathname.includes('/prep/')) {
      setDesktopSidebarOpen(false);
    } else {
      setDesktopSidebarOpen(true);
    }
  }, [location.pathname]);


  return (
    <div className="flex h-screen bg-transparent font-sans w-full overflow-hidden text-gray-900">
      
      {/* Mobile Sidebar Overlay */}
      {mobileSidebarOpen && (
        <div 
          className="fixed inset-0 bg-black/20 backdrop-blur-sm z-40 lg:hidden transition-opacity"
          onClick={() => setMobileSidebarOpen(false)}
        />
      )}

      {/* Sidebar - Off-canvas on mobile */}
      <div className={`fixed inset-y-0 left-0 z-50 transform transition-all duration-500 ease-[cubic-bezier(0.2,0.8,0.2,1)] lg:relative lg:w-64 ${desktopSidebarOpen ? 'lg:translate-x-0 lg:ml-0' : 'lg:-translate-x-full lg:-ml-64'} ${mobileSidebarOpen ? 'translate-x-0' : '-translate-x-full'}`}>
        <div className="w-64 h-full"><Sidebar onClose={() => setMobileSidebarOpen(false)} onToggleDesktop={() => setDesktopSidebarOpen(!desktopSidebarOpen)} /></div>
      </div>

      <div className="flex-1 flex flex-col min-w-0 w-full h-full relative">
        {/* Desktop Sidebar Toggle (Only visible when sidebar is closed on lg screens) */}
        {/* Mini Sidebar */}
        <div className={`hidden lg:flex flex-col justify-between absolute inset-y-0 left-0 w-20 z-40 bg-[#141A21] border-r border-gray-800 shadow-sm py-6 items-center transform transition-all duration-500 ease-[cubic-bezier(0.2,0.8,0.2,1)] ${desktopSidebarOpen ? '-translate-x-full opacity-0 pointer-events-none' : 'translate-x-0 opacity-100 delay-100'}`}>
            
            {/* Top section: Logo & Toggle */}
            <div className="flex flex-col items-center gap-6">
              <div className="w-10 h-10 rounded-full overflow-hidden shrink-0 border border-gray-700 shadow-sm flex items-center justify-center">
                <img src="/logo.jpg" alt="Logo" className="w-full h-full object-cover" />
              </div>
              <button 
                onClick={() => setDesktopSidebarOpen(true)}
                className="p-2 text-gray-400 hover:text-white transition-colors rounded-lg hover:bg-white/10"
                title="Expand Menu"
              >
                <PanelRight size={20} />
              </button>
            </div>

            {/* Bottom section: Settings & AI Provider */}
            <div className="flex flex-col items-center gap-6">
              <div className="relative">
                <button 
                  onClick={() => setShowEngineDropdown(!showEngineDropdown)}
                  className="p-2 text-gray-400 hover:text-white transition-colors rounded-lg hover:bg-white/10"
                  title="Select AI Engine"
                >
                  <Cpu size={20} />
                </button>
                {showEngineDropdown && (
                  <div className="absolute bottom-0 left-12 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-xl shadow-lg w-40 overflow-hidden z-50 animate-in fade-in slide-in-from-left-2 duration-200">
                    <div className="p-2 text-[10px] font-bold text-gray-500 uppercase tracking-wider bg-gray-50 dark:bg-gray-900 border-b border-gray-100 dark:border-gray-700">Provider</div>
                    <button onClick={() => { setEngine('groq'); setShowEngineDropdown(false); }} className={`w-full text-left px-4 py-3 text-sm font-medium hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors ${engine === 'groq' ? 'text-[var(--matte-primary)]' : 'text-gray-700 dark:text-gray-300'}`}>Groq (Fast)</button>
                    <button onClick={() => { setEngine('gemini'); setShowEngineDropdown(false); }} className={`w-full text-left px-4 py-3 text-sm font-medium hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors ${engine === 'gemini' ? 'text-[var(--matte-primary)]' : 'text-gray-700 dark:text-gray-300'}`}>Gemini</button>
                  </div>
                )}
              </div>
              <button 
                onClick={() => navigate('/settings')}
                className="p-2 text-gray-400 hover:text-white transition-colors rounded-lg hover:bg-white/10"
                title="Settings"
              >
                <Settings size={20} />
              </button>
            </div>
          </div>

        {/* Mobile Top Bar */}
        <header className="lg:hidden bg-white border-b border-gray-200 p-4 flex items-center justify-between z-30">
          <h1 className="text-xl font-bold tracking-tight text-black">EXAMMIND</h1>
          <button 
            onClick={() => setMobileSidebarOpen(true)}
            className="p-2 text-gray-600 hover:text-black transition-colors rounded-lg hover:bg-gray-100"
          >
            <Menu size={20} />
          </button>
        </header>

        {/* Main Content Area */}
        <main className={`flex-1 overflow-y-auto w-full relative z-10 p-4 md:p-8 lg:p-12 transition-all duration-500 ease-[cubic-bezier(0.2,0.8,0.2,1)] ${!desktopSidebarOpen ? 'lg:pl-24' : ''}`}>
          <div key={location.pathname} className="w-full h-full max-w-5xl mx-auto animate-in fade-in zoom-in-[0.98] slide-in-from-bottom-2 duration-500 ease-[cubic-bezier(0.2,0.8,0.2,1)]">
            <Routes>
              <Route path="/" element={<HomeDashboard />} />
              <Route path="/new-exam" element={<UploadComponent />} />
              <Route path="/timetable" element={<Timetable />} />
              <Route path="/tracker" element={<SyllabusTracker />} />
              <Route path="/notes" element={<NotesView />} />
              <Route path="/profile" element={<ProfileView />} />
              <Route path="/settings" element={<SettingsView />} />
              <Route path="/quiz" element={<QuizView />} />
              <Route path="/exam/:id" element={<ExamDashboard />} />
              <Route path="/exam/:id/prep/:topic" element={<PrepMode />} />
            </Routes>
          </div>
        </main>
      </div>
    </div>
  );
}
