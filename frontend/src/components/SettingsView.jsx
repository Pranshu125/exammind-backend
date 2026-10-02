import { useState, useRef, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { useTheme } from '../contexts/ThemeContext';
import { updateProfile, updatePassword, deleteUser, linkWithPopup, GoogleAuthProvider, GithubAuthProvider } from 'firebase/auth';
import { ref, uploadBytes, getDownloadURL } from 'firebase/storage';
import { doc, getDoc, setDoc, collection, getDocs } from 'firebase/firestore';
import { storage, db } from '../lib/firebase';
import { LogOut, Copy, Check, X, User, Shield, Loader2, Palette, Camera, GraduationCap, MapPin, Phone, Code, Briefcase, Globe, BookText, Settings as SettingsIcon, ChevronRight, ArrowLeft, Bell, BookOpen, Bot, Calendar, Clock, ToggleLeft, ToggleRight, CheckSquare } from 'lucide-react';
import CustomSelect from './CustomSelect';

export default function SettingsView() {
  const { currentUser, logout } = useAuth();
  const { theme, setTheme, fontSize, setFontSize, accentColor, setAccentColor, layoutDensity, setLayoutDensity } = useTheme();
  
  const [activeTab, setActiveTab] = useState('menu');
    const [showWebcalModal, setShowWebcalModal] = useState(false);
  const [webcalUrl, setWebcalUrl] = useState('');
  const [syncingWebcal, setSyncingWebcal] = useState(false);

  useEffect(() => {
    if (showWebcalModal) {
      import('../lib/syncCalendar').then(({ generateAndUploadWebcal }) => {
        setSyncingWebcal(true);
        generateAndUploadWebcal(currentUser).then(url => {
          if (url) setWebcalUrl(url);
          setSyncingWebcal(false);
        });
      });
    }
  }, [showWebcalModal]);
  const [copiedLink, setCopiedLink] = useState(false);
  const [selectedCalendarPlatform, setSelectedCalendarPlatform] = useState('google');
  const [displayName, setDisplayName] = useState(currentUser?.displayName || '');
  const [newPassword, setNewPassword] = useState('');
  
  const [formData, setFormData] = useState({
    // Profile
    institution: '', degree: '', standing: '', studentId: '',
    phone: '', dob: '', location: '', github: '', linkedin: '', portfolio: '', bio: '',
    // Notifications
    emailNotifications: true, pushNotifications: false,
    alertUpcoming: true, alertRecap: true, alertMissed: true, alertCountdown: true,
    // Study
    studyStart: '18:00', studyEnd: '21:00',
    breakDays: [], focusMethod: '25/5',
    // Integrations
    calendarProvider: 'none', aiProvider: 'groq', customApiKey: ''
  });

  const [loading, setLoading] = useState(false);
  const [imageLoading, setImageLoading] = useState(false);
  const [message, setMessage] = useState({ text: '', type: '' });
  const fileInputRef = useRef(null);

  const themeOptions = [
    { value: 'light', label: 'Light Mode' },
    { value: 'dark', label: 'Dark Mode' }
  ];
  
  const fontSizeOptions = [
    { value: 'small', label: 'Small' },
    { value: 'medium', label: 'Medium (Default)' },
    { value: 'large', label: 'Large' },
    { value: 'xlarge', label: 'Extra Large' }
  ];

  
  const accentOptions = [
    { value: 'white', label: 'Monochrome (White/Black)' },
    { value: 'blue', label: 'Deep Blue' },
    { value: 'purple', label: 'Deep Purple' },
    { value: 'green', label: 'Deep Green' },
    { value: 'orange', label: 'Deep Orange' }
  ];

  const densityOptions = [
    { value: 'comfortable', label: 'Comfortable (Default)' },
    { value: 'compact', label: 'Compact' }
  ];

  const timeZoneOptions = [
    { value: 'UTC', label: 'UTC' },
    { value: 'EST', label: 'Eastern Time (EST/EDT)' },
    { value: 'CST', label: 'Central Time (CST/CDT)' },
    { value: 'PST', label: 'Pacific Time (PST/PDT)' },
    { value: 'IST', label: 'India Standard Time (IST)' },
    { value: 'GMT', label: 'Greenwich Mean Time (GMT)' }
  ];

  const focusOptions = [
    { value: 'none', label: 'Disabled' },
    { value: '25/5', label: '25 mins work / 5 mins break' },
    { value: '50/10', label: '50 mins work / 10 mins break' }
  ];

  const calendarOptions = [
    { value: 'none', label: 'Not Connected' },
    { value: 'google', label: 'Google Calendar' },
    { value: 'apple', label: 'Apple Calendar' },
    { value: 'outlook', label: 'Outlook' }
  ];

  const aiOptions = [
    { value: 'groq', label: 'Groq (Fast)' },
    { value: 'gemini', label: 'Google Gemini (Accurate)' }
  ];

  const daysOfWeek = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];

  useEffect(() => {
    if (!currentUser) return;
    const fetchProfile = async () => {
      try {
        const docRef = doc(db, `users`, currentUser.uid);
        const docSnap = await getDoc(docRef);
        if (docSnap.exists() && docSnap.data().profile) {
          setFormData(prev => ({ ...prev, ...docSnap.data().profile }));
        }
      } catch (err) {
        console.error("Error fetching profile:", err);
      }
    };
    fetchProfile();
  }, [currentUser]);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({ ...prev, [name]: type === 'checkbox' ? checked : value }));
  };

  const handleToggleDay = (day) => {
    setFormData(prev => {
      const days = prev.breakDays || [];
      if (days.includes(day)) {
        return { ...prev, breakDays: days.filter(d => d !== day) };
      } else {
        return { ...prev, breakDays: [...days, day] };
      }
    });
  };

  const handleExportData = async () => {
    try {
      const docRef = doc(db, 'users', currentUser.uid);
      const snap = await getDoc(docRef);
      const data = snap.exists() ? snap.data() : { profile: formData };
      const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `exammind_backup_${currentUser.uid}.json`;
      a.click();
      URL.revokeObjectURL(url);
    } catch (err) {
      alert('Error exporting data: ' + err.message);
    }
  };

  const handleDeleteAccount = async () => {
    if (window.confirm("WARNING: This will permanently delete your account and all associated data. This action CANNOT be undone. Are you absolutely sure?")) {
      try {
        await deleteUser(currentUser);
      } catch (err) {
        alert("Failed to delete account. For security reasons, you may need to sign out and sign back in before deleting your account.\n\nError: " + err.message);
      }
    }
  };

  const handleLinkAccount = async (providerName) => {
    try {
      let provider;
      if (providerName === 'google') provider = new GoogleAuthProvider();
      if (providerName === 'github') provider = new GithubAuthProvider();
      
      await linkWithPopup(currentUser, provider);
      alert(`Successfully linked ${providerName} account!`);
      await currentUser.reload();
    } catch (err) {
      alert(`Failed to link ${providerName} account: ` + err.message);
    }
  };

  const handleImageUpload = async (e) => {
    const file = e.target.files[0];
    if (!file || !currentUser) return;

    setImageLoading(true);
    setMessage({ text: '', type: '' });
    try {
      const storageRef = ref(storage, `profiles/${currentUser.uid}`);
      await uploadBytes(storageRef, file);
      const downloadURL = await getDownloadURL(storageRef);
      
      await updateProfile(currentUser, { photoURL: downloadURL });
      await currentUser.reload();
      
      setMessage({ text: 'Profile picture updated successfully!', type: 'success' });
    } catch (error) {
      console.error(error);
      setMessage({ text: "Failed to upload image.", type: 'error' });
    } finally {
      setImageLoading(false);
    }
  };

  const handleUpdateProfile = async (e) => {
    if (e) e.preventDefault();
    if (!currentUser) return;
    
    setLoading(true);
    setMessage({ text: '', type: '' });
    
    try {
      const promises = [];
      if (displayName !== currentUser.displayName) {
        promises.push(updateProfile(currentUser, { displayName }));
      }
      if (newPassword) {
        promises.push(updatePassword(currentUser, newPassword));
      }

      const docRef = doc(db, `users`, currentUser.uid);
      promises.push(setDoc(docRef, { profile: formData }, { merge: true }));

      await Promise.all(promises);
      await currentUser.reload();
      
      setMessage({ text: 'Settings updated successfully!', type: 'success' });
      setNewPassword(''); 
    } catch (error) {
      setMessage({ text: error.message, type: 'error' });
    } finally {
      setLoading(false);
    }
  };

  const MenuItem = ({ id, icon: Icon, title, colorClass, bgClass }) => (
    <button onClick={() => { setActiveTab(id); setMessage({text:'', type:''}); }} className="flex items-center justify-between p-6 bg-white hover:bg-gray-50 border-b border-gray-100 transition-colors text-left group">
      <div className="flex items-center gap-4">
        <div className={`${bgClass} ${colorClass} p-2.5 rounded-xl group-hover:scale-110 transition-transform`}><Icon size={20} /></div>
        <span className="font-semibold text-gray-900 text-lg">{title}</span>
      </div>
      <ChevronRight className={`text-gray-400 group-hover:${colorClass} transition-colors`} />
    </button>
  );

  return (
    <div className="max-w-4xl mx-auto space-y-6 pb-12">
      
      {activeTab === 'menu' ? (
        <div className="max-w-2xl mx-auto space-y-6">
          <div className="mb-6">
            <h2 className="text-3xl font-bold tracking-tight text-gray-900 mb-2">Settings</h2>
            <p className="text-gray-500">Manage your account preferences and profile information.</p>
          </div>
          <div className="bg-white border border-gray-200 rounded-2xl shadow-sm overflow-hidden flex flex-col">
            <MenuItem id="profile" icon={User} title="Profile Edit" colorClass="text-blue-600" bgClass="bg-blue-100" />
            <MenuItem id="study" icon={BookOpen} title="Study Preferences" colorClass="text-emerald-600" bgClass="bg-emerald-100" />
            <MenuItem id="notifications" icon={Bell} title="Notifications & Reminders" colorClass="text-amber-600" bgClass="bg-amber-100" />
            <MenuItem id="integrations" icon={Bot} title="AI & Integrations" colorClass="text-indigo-600" bgClass="bg-indigo-100" />
            <MenuItem id="appearance" icon={Palette} title="Appearance" colorClass="text-purple-600" bgClass="bg-purple-100" />
            <MenuItem id="account" icon={Shield} title="Account & Security" colorClass="text-red-600" bgClass="bg-red-100" />
          </div>
        </div>
      ) : (
        <div className="mb-6 flex items-center justify-between">
          <button onClick={() => setActiveTab('menu')} className="flex items-center gap-2 text-gray-500 hover:text-black font-semibold transition-colors bg-white px-4 py-2 rounded-xl border border-gray-200 shadow-sm hover:shadow-md">
            <ArrowLeft size={18} /> Back to Settings
          </button>
          
          {/* Global Save Button for forms */}
          {['profile', 'study', 'notifications', 'integrations'].includes(activeTab) && (
            <button onClick={handleUpdateProfile} disabled={loading} className="btn-primary px-6 py-2 rounded-xl flex items-center gap-2 font-bold shadow-sm transition-all disabled:opacity-50">
              {loading && <Loader2 size={16} className="animate-spin" />} Save Changes
            </button>
          )}
        </div>
      )}

      {message.text && activeTab !== 'menu' && (
        <div className={`p-4 rounded-xl text-sm font-medium border ${message.type === 'error' ? 'bg-red-50 text-red-600 border-red-100' : 'bg-green-50 text-green-700 border-green-200'}`}>
          {message.text}
        </div>
      )}

      {/* TAB: PROFILE */}
      {activeTab === 'profile' && (
        <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
          <div className="bg-white border border-gray-200 p-8 rounded-2xl shadow-sm">
            <h2 className="text-xl font-bold text-gray-900 mb-6 flex items-center gap-2">
              <User size={20} className="text-blue-600" /> Basic Details
            </h2>
            <div className="mb-8 flex flex-col items-center sm:items-start sm:flex-row gap-6">
              <div className="relative group cursor-pointer shrink-0" onClick={() => fileInputRef.current?.click()}>
                <div className="h-24 w-24 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center text-3xl font-bold overflow-hidden border-4 border-white shadow-md transition-transform group-hover:scale-105">
                  {currentUser?.photoURL ? (
                    <img src={currentUser.photoURL} alt="Profile" className="h-full w-full object-cover" />
                  ) : currentUser?.displayName ? (
                    currentUser.displayName.charAt(0).toUpperCase()
                  ) : (
                    <User size={40} />
                  )}
                </div>
                <div className="absolute inset-0 bg-black/40 rounded-full opacity-0 group-hover:opacity-100 flex items-center justify-center transition-opacity">
                  {imageLoading ? <Loader2 size={24} className="text-white animate-spin" /> : <Camera size={24} className="text-white" />}
                </div>
                <input type="file" ref={fileInputRef} onChange={handleImageUpload} accept="image/*" className="hidden" />
              </div>
              <div className="flex flex-col justify-center">
                <h3 className="font-semibold text-gray-900 mb-1">Profile Picture</h3>
                <p className="text-sm text-gray-500 mb-2">Click the image to upload a new avatar.</p>
                <button type="button" onClick={() => fileInputRef.current?.click()} className="text-sm text-blue-600 font-medium hover:underline self-start">Change Image</button>
              </div>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 max-w-2xl">
              <div className="space-y-2">
                <label className="text-sm font-semibold text-gray-700 flex items-center gap-2">Display Name</label>
                <input type="text" value={displayName} onChange={(e) => setDisplayName(e.target.value)} placeholder="Enter your name" className="w-full p-3 bg-gray-50 border border-gray-200 rounded-lg focus:ring-2 focus:ring-black outline-none transition-all" />
              </div>
              <div className="space-y-2">
                <label className="text-sm font-semibold text-gray-700 flex items-center gap-2">Email Address</label>
                <input type="email" value={currentUser?.email || ''} disabled className="w-full p-3 bg-gray-100 border border-gray-200 rounded-lg text-gray-500 outline-none cursor-not-allowed" />
                <p className="text-[10px] text-gray-400">Email cannot be changed directly.</p>
              </div>
            </div>
          </div>

          <div className="bg-white border border-gray-200 p-8 rounded-2xl shadow-sm space-y-8">
            <div>
              <h3 className="text-lg font-bold text-gray-900 flex items-center gap-2 mb-4">
                <GraduationCap className="text-blue-600" size={20}/> Academic Information
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <input type="text" name="institution" value={formData.institution || ''} onChange={handleChange} placeholder="Institution Name (e.g., VIT Bhopal)" className="w-full bg-gray-50 border border-gray-200 rounded-lg p-3 focus:ring-2 focus:ring-black outline-none transition-all text-sm" />
                <input type="text" name="degree" value={formData.degree || ''} onChange={handleChange} placeholder="Degree & Major (e.g., B.Tech in CS)" className="w-full bg-gray-50 border border-gray-200 rounded-lg p-3 focus:ring-2 focus:ring-black outline-none transition-all text-sm" />
                <input type="text" name="standing" value={formData.standing || ''} onChange={handleChange} placeholder="Academic Standing (e.g., Semester 4)" className="w-full bg-gray-50 border border-gray-200 rounded-lg p-3 focus:ring-2 focus:ring-black outline-none transition-all text-sm" />
                <input type="text" name="studentId" value={formData.studentId || ''} onChange={handleChange} placeholder="Student ID / Roll Number" className="w-full bg-gray-50 border border-gray-200 rounded-lg p-3 focus:ring-2 focus:ring-black outline-none transition-all text-sm" />
              </div>
            </div>

            <div className="border-t border-gray-100 pt-6">
              <h3 className="text-lg font-bold text-gray-900 flex items-center gap-2 mb-4">
                <User className="text-purple-600" size={20}/> Personal Details
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="relative">
                  <Phone className="absolute left-3 top-3 text-gray-400" size={16} />
                  <input type="tel" name="phone" value={formData.phone || ''} onChange={handleChange} placeholder="Phone Number" className="w-full bg-gray-50 border border-gray-200 rounded-lg pl-10 p-3 focus:ring-2 focus:ring-black outline-none transition-all text-sm" />
                </div>
                <input type="date" name="dob" value={formData.dob || ''} onChange={handleChange} className="w-full bg-gray-50 border border-gray-200 rounded-lg p-3 focus:ring-2 focus:ring-black outline-none transition-all text-sm text-gray-700" />
                <div className="relative">
                  <MapPin className="absolute left-3 top-3 text-gray-400" size={16} />
                  <input type="text" name="location" value={formData.location || ''} onChange={handleChange} placeholder="City / Location" className="w-full bg-gray-50 border border-gray-200 rounded-lg pl-10 p-3 focus:ring-2 focus:ring-black outline-none transition-all text-sm" />
                </div>
                <div className="space-y-1">
                  <CustomSelect 
                    value={formData.timeZone || 'UTC'}
                    onChange={(e) => setFormData(prev => ({...prev, timeZone: e.target.value}))}
                    options={timeZoneOptions}
                    className="w-full bg-gray-50 p-3"
                  />
                </div>
              </div>
            </div>

            <div className="border-t border-gray-100 pt-6">
              <h3 className="text-lg font-bold text-gray-900 flex items-center gap-2 mb-4">
                <Globe className="text-green-600" size={20}/> Professional Links & Bio
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="relative">
                  <Code className="absolute left-3 top-3 text-gray-400" size={16} />
                  <input type="url" name="github" value={formData.github || ''} onChange={handleChange} placeholder="GitHub Profile URL" className="w-full bg-gray-50 border border-gray-200 rounded-lg pl-10 p-3 focus:ring-2 focus:ring-black outline-none transition-all text-sm" />
                </div>
                <div className="relative">
                  <Briefcase className="absolute left-3 top-3 text-gray-400" size={16} />
                  <input type="url" name="linkedin" value={formData.linkedin || ''} onChange={handleChange} placeholder="LinkedIn Profile URL" className="w-full bg-gray-50 border border-gray-200 rounded-lg pl-10 p-3 focus:ring-2 focus:ring-black outline-none transition-all text-sm" />
                </div>
                <div className="relative md:col-span-2">
                  <Globe className="absolute left-3 top-3 text-gray-400" size={16} />
                  <input type="url" name="portfolio" value={formData.portfolio || ''} onChange={handleChange} placeholder="Personal Portfolio URL" className="w-full bg-gray-50 border border-gray-200 rounded-lg pl-10 p-3 focus:ring-2 focus:ring-black outline-none transition-all text-sm" />
                </div>
                <div className="relative md:col-span-2">
                  <BookText className="absolute left-3 top-3 text-gray-400" size={16} />
                  <textarea name="bio" value={formData.bio || ''} onChange={handleChange} rows="3" placeholder="Bio / Academic Goals..." className="w-full bg-gray-50 border border-gray-200 rounded-lg pl-10 p-3 focus:ring-2 focus:ring-black outline-none transition-all text-sm resize-none"></textarea>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* TAB: STUDY PREFERENCES */}
      {activeTab === 'study' && (
        <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
          <div className="bg-white border border-gray-200 p-8 rounded-2xl shadow-sm space-y-8">
            <div>
              <h2 className="text-xl font-bold text-gray-900 mb-6 flex items-center gap-2">
                <Clock size={20} className="text-emerald-600" /> Default Availability
              </h2>
              <div className="flex flex-col sm:flex-row items-center gap-4 max-w-md">
                <div className="w-full space-y-2">
                  <label className="text-sm font-semibold text-gray-700">Start Time</label>
                  <input type="time" name="studyStart" value={formData.studyStart} onChange={handleChange} className="w-full p-3 bg-gray-50 border border-gray-200 rounded-lg outline-none" />
                </div>
                <span className="text-gray-400 font-bold hidden sm:block mt-6">to</span>
                <div className="w-full space-y-2">
                  <label className="text-sm font-semibold text-gray-700">End Time</label>
                  <input type="time" name="studyEnd" value={formData.studyEnd} onChange={handleChange} className="w-full p-3 bg-gray-50 border border-gray-200 rounded-lg outline-none" />
                </div>
              </div>
              <p className="text-xs text-gray-500 mt-4">Set your standard daily study hours. AI will try to schedule blocks within this window.</p>
            </div>

            <div className="border-t border-gray-100 pt-6">
              <h2 className="text-xl font-bold text-gray-900 mb-6 flex items-center gap-2">
                <Calendar size={20} className="text-blue-600" /> Break Days
              </h2>
              <div className="flex flex-wrap gap-3">
                {daysOfWeek.map(day => (
                  <button 
                    key={day} 
                    type="button" 
                    onClick={() => handleToggleDay(day)}
                    className={`px-4 py-2 rounded-xl text-sm font-bold border transition-all ${
                      (formData.breakDays || []).includes(day) 
                        ? 'bg-blue-50 border-blue-200 text-blue-700 shadow-sm' 
                        : 'bg-white border-gray-200 text-gray-500 hover:bg-gray-50'
                    }`}
                  >
                    {day}
                  </button>
                ))}
              </div>
              <p className="text-xs text-gray-500 mt-4">Select days you usually take off. The AI scheduler will avoid these days.</p>
            </div>

            <div className="border-t border-gray-100 pt-6">
              <h2 className="text-xl font-bold text-gray-900 mb-6 flex items-center gap-2">
                <CheckSquare size={20} className="text-purple-600" /> Focus Method
              </h2>
              <div className="space-y-4 max-w-md">
                <CustomSelect 
                  value={formData.focusMethod}
                  onChange={(e) => setFormData(prev => ({...prev, focusMethod: e.target.value}))}
                  options={focusOptions}
                  className="w-full bg-gray-50"
                />
                <p className="text-xs text-gray-500">Enable a built-in Pomodoro timer to help pace your study blocks.</p>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* TAB: NOTIFICATIONS */}
      {activeTab === 'notifications' && (
        <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
          <div className="bg-white border border-gray-200 p-8 rounded-2xl shadow-sm space-y-8">
            <div>
              <h2 className="text-xl font-bold text-gray-900 mb-6 flex items-center gap-2">
                <Bell size={20} className="text-amber-600" /> Delivery Methods
              </h2>
              <div className="space-y-4">
                <label className="flex items-center justify-between p-4 border border-gray-200 rounded-xl cursor-pointer hover:bg-gray-50 transition-colors">
                  <div>
                    <div className="font-bold text-gray-900">Email Notifications</div>
                    <div className="text-sm text-gray-500">Receive alerts directly to {currentUser?.email}</div>
                  </div>
                  <input type="checkbox" name="emailNotifications" checked={formData.emailNotifications} onChange={handleChange} className="w-5 h-5 rounded text-blue-600 focus:ring-blue-500" />
                </label>
                <label className="flex items-center justify-between p-4 border border-gray-200 rounded-xl cursor-pointer hover:bg-gray-50 transition-colors">
                  <div>
                    <div className="font-bold text-gray-900">Push Notifications</div>
                    <div className="text-sm text-gray-500">Receive alerts on your device</div>
                  </div>
                  <input type="checkbox" name="pushNotifications" checked={formData.pushNotifications} onChange={handleChange} className="w-5 h-5 rounded text-blue-600 focus:ring-blue-500" />
                </label>
              </div>
            </div>

            <div className="border-t border-gray-100 pt-6">
              <h2 className="text-xl font-bold text-gray-900 mb-6 flex items-center gap-2">
                <Bell size={20} className="text-red-500" /> Specific Alerts
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {[
                  { name: 'alertUpcoming', label: 'Upcoming Study Block', desc: '15 mins before a block starts' },
                  { name: 'alertRecap', label: 'Daily Recap', desc: 'Summary of what you achieved today' },
                  { name: 'alertMissed', label: 'Missed Task Reminder', desc: 'If tasks pile up past midnight' },
                  { name: 'alertCountdown', label: 'Exam Countdown', desc: 'Weekly checks as exam approaches' }
                ].map(alert => (
                  <label key={alert.name} className="flex items-start gap-4 p-4 border border-gray-200 rounded-xl cursor-pointer hover:bg-gray-50 transition-colors">
                    <input type="checkbox" name={alert.name} checked={formData[alert.name]} onChange={handleChange} className="mt-1 w-5 h-5 rounded text-blue-600 focus:ring-blue-500" />
                    <div>
                      <div className="font-bold text-gray-900">{alert.label}</div>
                      <div className="text-xs text-gray-500">{alert.desc}</div>
                    </div>
                  </label>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* TAB: AI & INTEGRATIONS */}
      {activeTab === 'integrations' && (
        <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
          <div className="bg-white border border-gray-200 p-8 rounded-2xl shadow-sm space-y-8">
            <div>
                <h2 className="text-xl font-bold text-gray-900 mb-6 flex items-center gap-2">
                  <Calendar size={20} className="text-indigo-600" /> Calendar Integrations
                </h2>
                
                <div className="space-y-4 max-w-3xl">
                  <div className="border border-gray-200 rounded-xl p-5 bg-white flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
                    <div className="flex items-start gap-4">
                      <div className="p-3 bg-blue-50 text-blue-600 rounded-lg shrink-0 mt-1">
                        <Calendar size={24} />
                      </div>
                      <div>
                        <h3 className="font-bold text-gray-900 text-lg flex items-center gap-2">
                          Universal Auto-Sync (WebCal)
                          {formData.webcalConnected && <span className="text-[10px] font-bold text-green-700 bg-green-100 px-2 py-0.5 rounded-full uppercase tracking-wider">Active</span>}
                        </h3>
                        <p className="text-sm text-gray-500 max-w-md mt-1">Automatically sync your timetables in the background. Works universally with Google Calendar, Apple Calendar, and Outlook.</p>
                      </div>
                    </div>
                    <div className="w-full md:w-auto shrink-0">
                        {formData.webcalConnected ? (
                          <div className="flex flex-col items-end gap-2 w-full">
                            <button onClick={() => setShowWebcalModal(true)} className="w-full md:w-auto px-4 py-2 bg-gray-100 text-gray-700 font-semibold rounded-lg hover:bg-gray-200 transition-colors border border-gray-200 text-sm flex items-center justify-center gap-2">
                              Configure & Sync
                            </button>
                            <button onClick={() => setFormData(p => ({...p, webcalConnected: false}))} className="text-xs text-red-500 font-medium hover:underline w-full text-right">Disconnect</button>
                          </div>
                        ) : (
                          <button onClick={() => setShowWebcalModal(true)} className="w-full md:w-auto px-5 py-2.5 bg-blue-50 text-blue-700 font-semibold rounded-lg hover:bg-blue-100 transition-colors border border-blue-200 text-sm shadow-sm">
                            Connect Calendar
                          </button>
                        )}
                    </div>
                  </div>
                  
                  <div className="bg-gray-50 p-4 rounded-xl border border-gray-100">
                    <p className="text-sm text-gray-600">
                      <strong>How it works:</strong> Once connected, you never have to manually export again. Any exams you create, modify, or delete in Exammind will automatically update across all your linked calendar accounts in the background.
                    </p>
                  </div>
                </div>
              </div>
              
              {/* WebCal Configuration Modal */}
              {showWebcalModal && (
                <div className="fixed inset-0 bg-black/50 z-[100] flex items-center justify-center p-4 backdrop-blur-sm">
                  <div className="bg-white rounded-3xl w-full max-w-2xl overflow-hidden shadow-2xl flex flex-col max-h-[90vh]">
                    <div className="p-6 border-b border-gray-100 flex items-center justify-between bg-gray-50">
                      <h3 className="text-xl font-bold text-gray-900 flex items-center gap-2"><Calendar className="text-blue-600" /> Connect Calendar</h3>
                      <button onClick={() => setShowWebcalModal(false)} className="text-gray-400 hover:text-gray-900 bg-white hover:bg-gray-100 p-2 rounded-full transition-colors"><X size={20}/></button>
                    </div>
                    
                    <div className="p-6 overflow-y-auto">
                      <p className="text-gray-600 mb-6 font-medium">To securely auto-sync your timetables, copy your private WebCal link below and paste it into your preferred calendar app.</p>
                      
                      <div className="mb-8">
                        <label className="block text-sm font-bold text-gray-700 mb-2 uppercase tracking-wide">Your Private Subscription URL</label>
                        <div className="flex items-center gap-2">
                                                      <input 
                              readOnly 
                              value={syncingWebcal ? "Generating secure link..." : webcalUrl}
                              className="w-full bg-gray-100 border border-gray-200 text-gray-800 p-3 rounded-xl font-mono text-sm focus:outline-none"
                            />
                            <button 
                              disabled={syncingWebcal}
                              onClick={() => {
                                navigator.clipboard.writeText(webcalUrl);
                                setCopiedLink(true);
                                setTimeout(() => setCopiedLink(false), 3000);
                              }}
                            className={`flex items-center gap-2 px-4 py-3 rounded-xl font-bold transition-all ${copiedLink ? 'bg-green-100 text-green-700' : 'bg-blue-600 text-white hover:bg-blue-700'}`}
                          >
                            {copiedLink ? <><Check size={18}/> Copied</> : <><Copy size={18}/> Copy</>}
                          </button>
                        </div>
                        <p className="text-xs text-orange-500 mt-2 font-medium flex items-center gap-1"><Bell size={12}/> Do not share this link with anyone.</p>
                      </div>
                      
                      <div className="mb-4">
                        <div className="flex space-x-2 border-b border-gray-200 mb-4">
                          <button onClick={() => setSelectedCalendarPlatform('google')} className={`px-4 py-2 font-semibold text-sm transition-colors border-b-2 ${selectedCalendarPlatform === 'google' ? 'border-blue-600 text-blue-600' : 'border-transparent text-gray-500 hover:text-gray-700'}`}>Google Calendar</button>
                          <button onClick={() => setSelectedCalendarPlatform('apple')} className={`px-4 py-2 font-semibold text-sm transition-colors border-b-2 ${selectedCalendarPlatform === 'apple' ? 'border-gray-900 text-gray-900' : 'border-transparent text-gray-500 hover:text-gray-700'}`}>Apple Calendar</button>
                          <button onClick={() => setSelectedCalendarPlatform('outlook')} className={`px-4 py-2 font-semibold text-sm transition-colors border-b-2 ${selectedCalendarPlatform === 'outlook' ? 'border-blue-500 text-blue-500' : 'border-transparent text-gray-500 hover:text-gray-700'}`}>Outlook</button>
                        </div>
                        
                        <div className="bg-gray-50 rounded-xl p-5 border border-gray-100">
                          {selectedCalendarPlatform === 'google' && (
                            <ol className="list-decimal list-inside space-y-2 text-gray-700 text-sm">
                              <li>Open <a href="https://calendar.google.com" target="_blank" rel="noreferrer" className="text-blue-600 hover:underline font-medium">Google Calendar</a> on a desktop browser.</li>
                              <li>On the left sidebar, click the <strong>+</strong> next to "Other calendars".</li>
                              <li>Select <strong>"From URL"</strong>.</li>
                              <li>Paste the copied URL into the field and click <strong>Add calendar</strong>.</li>
                            </ol>
                          )}
                          {selectedCalendarPlatform === 'apple' && (
                            <ol className="list-decimal list-inside space-y-2 text-gray-700 text-sm">
                              <li>Open the <strong>Calendar</strong> app on your Mac.</li>
                              <li>Click <strong>File</strong> in the top menu bar, then select <strong>New Calendar Subscription...</strong></li>
                              <li>Paste the copied URL and click <strong>Subscribe</strong>.</li>
                              <li>Set Auto-refresh to <strong>Every hour</strong> and click OK.</li>
                              <p className="mt-2 text-xs text-gray-500 bg-white p-2 rounded border">On iPhone: Go to Settings &gt; Calendar &gt; Accounts &gt; Add Account &gt; Other &gt; Add Subscribed Calendar.</p>
                            </ol>
                          )}
                          {selectedCalendarPlatform === 'outlook' && (
                            <ol className="list-decimal list-inside space-y-2 text-gray-700 text-sm">
                              <li>Open <a href="https://outlook.live.com/calendar" target="_blank" rel="noreferrer" className="text-blue-600 hover:underline font-medium">Outlook Calendar</a>.</li>
                              <li>Click <strong>Add calendar</strong> in the left pane.</li>
                              <li>Select <strong>Subscribe from web</strong>.</li>
                              <li>Paste the copied URL, give it a name (e.g. "Exammind"), and click <strong>Import</strong>.</li>
                            </ol>
                          )}
                        </div>
                      </div>
                    </div>
                    
                    <div className="p-6 border-t border-gray-100 bg-gray-50 flex justify-end gap-3">
                      <button onClick={() => setShowWebcalModal(false)} className="px-6 py-2.5 rounded-xl font-bold text-gray-600 hover:bg-gray-200 transition-colors">Close</button>
                      <button onClick={() => {
                        setFormData(p => ({...p, webcalConnected: true}));
                        setShowWebcalModal(false);
                      }} className="px-6 py-2.5 rounded-xl font-bold bg-blue-600 text-white hover:bg-blue-700 shadow-sm transition-all flex items-center gap-2">
                        <Check size={18} /> I've Added It to My Calendar
                      </button>
                    </div>
                  </div>
                </div>
              )}
            <div className="border-t border-gray-100 pt-6">
              <h2 className="text-xl font-bold text-gray-900 mb-6 flex items-center gap-2">
                <Bot size={20} className="text-teal-600" /> AI Provider Settings
              </h2>
              <div className="space-y-6 max-w-md">
                <div className="space-y-2">
                  <label className="text-sm font-semibold text-gray-700 block">Default AI Model</label>
                  <CustomSelect 
                    value={formData.aiProvider}
                    onChange={(e) => setFormData(prev => ({...prev, aiProvider: e.target.value}))}
                    options={aiOptions}
                    className="w-full bg-gray-50"
                  />
                  <p className="text-xs text-gray-500">Groq is significantly faster, but Gemini may handle highly complex multi-month schedules better.</p>
                </div>
                <div className="space-y-2">
                  <label className="text-sm font-semibold text-gray-700 block">Custom API Key (Optional)</label>
                  <input type="password" name="customApiKey" value={formData.customApiKey || ''} onChange={handleChange} placeholder="sk-..." className="w-full p-3 bg-gray-50 border border-gray-200 rounded-lg outline-none text-sm" />
                  <p className="text-xs text-gray-500">Use your own API key to bypass default platform token limits.</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* TAB: ACCOUNT */}
      {activeTab === 'account' && (
        <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
          <form onSubmit={handleUpdateProfile} className="bg-white border border-gray-200 p-8 rounded-2xl shadow-sm">
            <h2 className="text-xl font-bold text-gray-900 mb-6 flex items-center gap-2">
              <Shield size={20} className="text-blue-600" /> Security
            </h2>
            <div className="space-y-2 max-w-md">
              <label className="text-sm font-semibold text-gray-700 flex items-center gap-2">
                New Password
              </label>
              <input type="password" value={newPassword} onChange={(e) => setNewPassword(e.target.value)} placeholder="Enter new password" className="w-full p-3 bg-gray-50 border border-gray-200 rounded-lg focus:ring-2 focus:ring-black outline-none transition-all" />
              <p className="text-xs text-gray-500 mt-1">Leave blank if you do not want to change your password.</p>
            </div>
            <div className="mt-6 flex justify-start">
              <button type="submit" disabled={loading || !newPassword} className="btn-primary px-8 py-3 rounded-xl flex items-center gap-2 font-bold shadow-md hover:shadow-lg transition-all disabled:opacity-50">
                {loading && <Loader2 size={18} className="animate-spin" />} Update Password
              </button>
            </div>
          </form>
          
          
          <div className="bg-white border border-gray-200 p-8 rounded-2xl shadow-sm">
            <h2 className="text-xl font-bold text-gray-900 mb-6 flex items-center gap-2">
              <Globe size={20} className="text-teal-600" /> Linked Accounts
            </h2>
            <div className="space-y-4 max-w-md">
              <div className="flex items-center justify-between p-4 border border-gray-200 rounded-xl">
                <div className="flex items-center gap-3">
                  <Globe size={20} className="text-gray-400" />
                  <span className="font-semibold text-gray-900">Google</span>
                </div>
                <button type="button" onClick={() => handleLinkAccount('google')} className="text-sm font-bold text-blue-600 hover:underline">Link</button>
              </div>
              <div className="flex items-center justify-between p-4 border border-gray-200 rounded-xl">
                <div className="flex items-center gap-3">
                  <Code size={20} className="text-gray-400" />
                  <span className="font-semibold text-gray-900">GitHub</span>
                </div>
                <button type="button" onClick={() => handleLinkAccount('github')} className="text-sm font-bold text-blue-600 hover:underline">Link</button>
              </div>
            </div>
          </div>

          <div className="bg-white border border-gray-200 p-8 rounded-2xl shadow-sm">
            <h2 className="text-xl font-bold text-gray-900 mb-6 flex items-center gap-2">
              <BookText size={20} className="text-indigo-600" /> Data & Privacy
            </h2>
            <div className="space-y-4 max-w-md">
              <p className="text-sm text-gray-600 mb-4">Download a complete backup of your user data, uploaded syllabi, and study history.</p>
              <button type="button" onClick={handleExportData} className="bg-gray-100 text-gray-800 px-6 py-3 rounded-xl font-bold shadow-sm hover:bg-gray-200 transition-colors flex items-center gap-2">
                Download Backup
              </button>
            </div>
          </div>

          <div className="bg-white p-8 rounded-2xl shadow-sm border border-red-100 space-y-8">
            <div>
              <h2 className="text-xl font-bold text-red-600 mb-2 flex items-center gap-2">
                Session Actions
              </h2>
              <p className="text-gray-500 text-sm mb-6">Log out of your account on this device. You will need to sign in again to access your exams.</p>
              <button onClick={logout} className="bg-red-50 text-red-600 px-6 py-3 rounded-xl font-bold hover:bg-red-100 flex items-center gap-2 transition-colors">
                <LogOut size={18} /> Sign Out
              </button>
            </div>
            
            <div className="border-t border-red-100 pt-6">
              <h2 className="text-xl font-bold text-red-700 mb-2 flex items-center gap-2">
                Danger Zone
              </h2>
              <p className="text-gray-500 text-sm mb-6">Permanently delete your account and all associated data. This action cannot be undone.</p>
              <button onClick={handleDeleteAccount} className="bg-red-600 text-white px-6 py-3 rounded-xl font-bold hover:bg-red-700 flex items-center gap-2 transition-colors shadow-sm">
                Delete Account
              </button>
            </div>
          </div>

        </div>
      )}

      {/* TAB: APPEARANCE */}
      {activeTab === 'appearance' && (
        <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
          <div className="bg-white border border-gray-200 p-8 rounded-2xl shadow-sm space-y-8">
            <div>
              <h2 className="text-xl font-bold text-gray-900 mb-6 flex items-center gap-2">
                <Palette size={20} className="text-blue-600" /> App Theme
              </h2>
              <div className="space-y-4 max-w-md">
                <label className="text-sm font-semibold text-gray-700 block">Select Mode</label>
                <CustomSelect 
                  value={theme}
                  onChange={(e) => setTheme(e.target.value)}
                  options={themeOptions}
                  className="w-full bg-gray-50"
                />
                <p className="text-xs text-gray-500">Changes will be applied immediately across the application.</p>
              </div>
            </div>
            
            <div className="border-t border-gray-100 pt-6">
              <h2 className="text-xl font-bold text-gray-900 mb-6 flex items-center gap-2">
                <BookText size={20} className="text-purple-600" /> Typography & Layout
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6 max-w-2xl">
                <div className="space-y-4">
                  <label className="text-sm font-semibold text-gray-700 block">Text Size</label>
                  <CustomSelect 
                    value={fontSize}
                    onChange={(e) => setFontSize(e.target.value)}
                    options={fontSizeOptions}
                    className="w-full bg-gray-50"
                  />
                  <p className="text-xs text-gray-500">Scales all text up or down.</p>
                </div>
                <div className="space-y-4">
                  <label className="text-sm font-semibold text-gray-700 block">Layout Density</label>
                  <CustomSelect 
                    value={layoutDensity}
                    onChange={(e) => setLayoutDensity(e.target.value)}
                    options={densityOptions}
                    className="w-full bg-gray-50"
                  />
                  <p className="text-xs text-gray-500">Compact reduces spacing in timetables.</p>
                </div>
              </div>
            </div>
            
            <div className="border-t border-gray-100 pt-6">
              <h2 className="text-xl font-bold text-gray-900 mb-6 flex items-center gap-2">
                <Palette size={20} className="text-pink-600" /> Accent Color
              </h2>
              <div className="space-y-4 max-w-md">
                <CustomSelect 
                  value={accentColor}
                  onChange={(e) => setAccentColor(e.target.value)}
                  options={accentOptions}
                  className="w-full bg-gray-50"
                />
                <p className="text-xs text-gray-500">Pick a primary theme color for buttons and highlights.</p>
              </div>
            </div>
          </div>
        </div>
      )}

    </div>
  );
}

