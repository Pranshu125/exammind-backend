with open("src/components/ProfileView.jsx", "w", encoding="utf-8") as f:
    f.write("""import { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { doc, getDoc, setDoc } from 'firebase/firestore';
import { db } from '../lib/firebase';
import { User, Mail, Shield, Calendar, Loader2, Save, GraduationCap, MapPin, Phone, Github, Linkedin, Globe, BookText } from 'lucide-react';

export default function ProfileView() {
  const { currentUser } = useAuth();
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState({ type: '', text: '' });

  const [formData, setFormData] = useState({
    institution: '',
    degree: '',
    standing: '',
    studentId: '',
    phone: '',
    dob: '',
    location: '',
    github: '',
    linkedin: '',
    portfolio: '',
    bio: ''
  });

  useEffect(() => {
    if (!currentUser) return;
    const fetchProfile = async () => {
      try {
        const docRef = doc(db, `users`, currentUser.uid);
        const docSnap = await getDoc(docRef);
        if (docSnap.exists() && docSnap.data().profile) {
          setFormData(docSnap.data().profile);
        }
      } catch (err) {
        console.error("Error fetching profile:", err);
      } finally {
        setLoading(false);
      }
    };
    fetchProfile();
  }, [currentUser]);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSave = async (e) => {
    e.preventDefault();
    setSaving(true);
    setMessage({ type: '', text: '' });
    
    try {
      const docRef = doc(db, `users`, currentUser.uid);
      await setDoc(docRef, { profile: formData }, { merge: true });
      setMessage({ type: 'success', text: 'Profile updated successfully!' });
      setTimeout(() => setMessage({ type: '', text: '' }), 3000);
    } catch (err) {
      console.error(err);
      setMessage({ type: 'error', text: 'Failed to update profile.' });
    } finally {
      setSaving(false);
    }
  };

  const creationDate = currentUser?.metadata?.creationTime 
    ? new Date(currentUser.metadata.creationTime).toLocaleDateString() 
    : 'Unknown';

  if (loading) return <div className="p-8 flex justify-center"><Loader2 className="animate-spin text-blue-600" size={32} /></div>;

  return (
    <div className="max-w-4xl mx-auto space-y-6 pb-12">
      <div className="bg-white border border-gray-200 p-8 rounded-2xl shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-6">
        <div className="flex items-center gap-6">
          <div className="h-24 w-24 bg-gray-100 text-blue-600 rounded-full flex items-center justify-center text-3xl font-bold overflow-hidden border-4 border-white shadow-md flex-shrink-0">
            {currentUser?.photoURL ? (
              <img src={currentUser.photoURL} alt="Profile" className="h-full w-full object-cover" />
            ) : currentUser?.displayName ? (
              currentUser.displayName.charAt(0).toUpperCase()
            ) : (
              <User size={40} />
            )}
          </div>
          <div>
            <h1 className="text-3xl font-bold tracking-tight text-black mb-1">{currentUser?.displayName || 'Student Profile'}</h1>
            <p className="text-gray-500 flex items-center gap-2 font-medium">
              <Mail size={16} /> {currentUser?.email}
            </p>
          </div>
        </div>
      </div>

      <form onSubmit={handleSave} className="space-y-6">
        
        {/* Academic Information */}
        <div className="bg-white border border-gray-200 rounded-2xl shadow-sm overflow-hidden">
          <div className="bg-gray-50 border-b border-gray-200 px-6 py-4 flex items-center gap-2">
            <GraduationCap className="text-blue-600" size={20} />
            <h3 className="font-bold text-gray-900">Academic Information</h3>
          </div>
          <div className="p-6 grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="space-y-1">
              <label className="text-sm font-semibold text-gray-700">Institution Name</label>
              <input type="text" name="institution" value={formData.institution} onChange={handleChange} placeholder="e.g., VIT Bhopal University" className="w-full bg-gray-50 border border-gray-200 rounded-lg px-4 py-2 focus:ring-2 focus:ring-black focus:outline-none transition-all" />
            </div>
            <div className="space-y-1">
              <label className="text-sm font-semibold text-gray-700">Degree & Major</label>
              <input type="text" name="degree" value={formData.degree} onChange={handleChange} placeholder="e.g., B.Tech in Computer Science" className="w-full bg-gray-50 border border-gray-200 rounded-lg px-4 py-2 focus:ring-2 focus:ring-black focus:outline-none transition-all" />
            </div>
            <div className="space-y-1">
              <label className="text-sm font-semibold text-gray-700">Current Academic Standing</label>
              <input type="text" name="standing" value={formData.standing} onChange={handleChange} placeholder="e.g., 2nd Year, Semester 4" className="w-full bg-gray-50 border border-gray-200 rounded-lg px-4 py-2 focus:ring-2 focus:ring-black focus:outline-none transition-all" />
            </div>
            <div className="space-y-1">
              <label className="text-sm font-semibold text-gray-700">Student ID / Roll Number</label>
              <input type="text" name="studentId" value={formData.studentId} onChange={handleChange} placeholder="e.g., 21BCE10234" className="w-full bg-gray-50 border border-gray-200 rounded-lg px-4 py-2 focus:ring-2 focus:ring-black focus:outline-none transition-all" />
            </div>
          </div>
        </div>

        {/* Basic Personal Details */}
        <div className="bg-white border border-gray-200 rounded-2xl shadow-sm overflow-hidden">
          <div className="bg-gray-50 border-b border-gray-200 px-6 py-4 flex items-center gap-2">
            <User className="text-purple-600" size={20} />
            <h3 className="font-bold text-gray-900">Basic Personal Details</h3>
          </div>
          <div className="p-6 grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="space-y-1">
              <label className="text-sm font-semibold text-gray-700">Phone Number</label>
              <div className="relative">
                <Phone className="absolute left-3 top-2.5 text-gray-400" size={18} />
                <input type="tel" name="phone" value={formData.phone} onChange={handleChange} placeholder="+1 234 567 8900" className="w-full bg-gray-50 border border-gray-200 rounded-lg pl-10 pr-4 py-2 focus:ring-2 focus:ring-black focus:outline-none transition-all" />
              </div>
            </div>
            <div className="space-y-1">
              <label className="text-sm font-semibold text-gray-700">Date of Birth</label>
              <div className="relative">
                <Calendar className="absolute left-3 top-2.5 text-gray-400" size={18} />
                <input type="date" name="dob" value={formData.dob} onChange={handleChange} className="w-full bg-gray-50 border border-gray-200 rounded-lg pl-10 pr-4 py-2 focus:ring-2 focus:ring-black focus:outline-none transition-all text-gray-700" />
              </div>
            </div>
            <div className="space-y-1 md:col-span-2">
              <label className="text-sm font-semibold text-gray-700">Location & Time Zone</label>
              <div className="relative">
                <MapPin className="absolute left-3 top-2.5 text-gray-400" size={18} />
                <input type="text" name="location" value={formData.location} onChange={handleChange} placeholder="e.g., New York, NY (EST)" className="w-full bg-gray-50 border border-gray-200 rounded-lg pl-10 pr-4 py-2 focus:ring-2 focus:ring-black focus:outline-none transition-all" />
              </div>
            </div>
          </div>
        </div>

        {/* Professional & Social Links */}
        <div className="bg-white border border-gray-200 rounded-2xl shadow-sm overflow-hidden">
          <div className="bg-gray-50 border-b border-gray-200 px-6 py-4 flex items-center gap-2">
            <Globe className="text-green-600" size={20} />
            <h3 className="font-bold text-gray-900">Professional Links & Goals</h3>
          </div>
          <div className="p-6 grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="space-y-1">
              <label className="text-sm font-semibold text-gray-700">GitHub Profile</label>
              <div className="relative">
                <Github className="absolute left-3 top-2.5 text-gray-400" size={18} />
                <input type="url" name="github" value={formData.github} onChange={handleChange} placeholder="https://github.com/username" className="w-full bg-gray-50 border border-gray-200 rounded-lg pl-10 pr-4 py-2 focus:ring-2 focus:ring-black focus:outline-none transition-all" />
              </div>
            </div>
            <div className="space-y-1">
              <label className="text-sm font-semibold text-gray-700">LinkedIn Profile</label>
              <div className="relative">
                <Linkedin className="absolute left-3 top-2.5 text-gray-400" size={18} />
                <input type="url" name="linkedin" value={formData.linkedin} onChange={handleChange} placeholder="https://linkedin.com/in/username" className="w-full bg-gray-50 border border-gray-200 rounded-lg pl-10 pr-4 py-2 focus:ring-2 focus:ring-black focus:outline-none transition-all" />
              </div>
            </div>
            <div className="space-y-1 md:col-span-2">
              <label className="text-sm font-semibold text-gray-700">Personal Portfolio</label>
              <div className="relative">
                <Globe className="absolute left-3 top-2.5 text-gray-400" size={18} />
                <input type="url" name="portfolio" value={formData.portfolio} onChange={handleChange} placeholder="https://yourwebsite.com" className="w-full bg-gray-50 border border-gray-200 rounded-lg pl-10 pr-4 py-2 focus:ring-2 focus:ring-black focus:outline-none transition-all" />
              </div>
            </div>
            <div className="space-y-1 md:col-span-2">
              <label className="text-sm font-semibold text-gray-700">Bio / Academic Goals</label>
              <div className="relative">
                <BookText className="absolute left-3 top-3 text-gray-400" size={18} />
                <textarea name="bio" value={formData.bio} onChange={handleChange} rows="3" placeholder="e.g., Aiming to maintain a 9.0 GPA while building full-stack projects..." className="w-full bg-gray-50 border border-gray-200 rounded-lg pl-10 pr-4 py-2 focus:ring-2 focus:ring-black focus:outline-none transition-all resize-none"></textarea>
              </div>
            </div>
          </div>
        </div>

        {/* System Details (Read Only) & Save Button */}
        <div className="flex flex-col sm:flex-row items-center justify-between gap-4 pt-4">
          <div className="text-xs text-gray-400 font-mono flex flex-col gap-1">
            <span className="flex items-center gap-1"><Shield size={12} /> ID: {currentUser?.uid}</span>
            <span className="flex items-center gap-1"><Calendar size={12} /> Joined: {creationDate}</span>
          </div>
          
          <div className="flex items-center gap-4 w-full sm:w-auto">
            {message.text && (
              <span className={`text-sm font-medium ${message.type === 'success' ? 'text-green-600' : 'text-red-600'}`}>
                {message.text}
              </span>
            )}
            <button 
              type="submit" 
              disabled={saving}
              className="w-full sm:w-auto btn-primary px-8 py-3 rounded-xl flex items-center justify-center gap-2 font-bold shadow-md hover:shadow-lg transition-all"
            >
              {saving ? <Loader2 className="animate-spin" size={20} /> : <Save size={20} />}
              {saving ? 'Saving...' : 'Save Profile Details'}
            </button>
          </div>
        </div>

      </form>
    </div>
  );
}
""")
print("done")
