import { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { doc, getDoc } from 'firebase/firestore';
import { db } from '../lib/firebase';
import { Link } from 'react-router-dom';
import { User, Mail, Shield, Calendar, Loader2, GraduationCap, MapPin, Phone, Code, Briefcase, Globe, BookText, Settings, ExternalLink } from 'lucide-react';

export default function ProfileView() {
  const { currentUser } = useAuth();
  const [loading, setLoading] = useState(true);
  
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

  const creationDate = currentUser?.metadata?.creationTime 
    ? new Date(currentUser.metadata.creationTime).toLocaleDateString() 
    : 'Unknown';

  if (loading) return <div className="p-8 flex justify-center"><Loader2 className="animate-spin text-blue-600" size={32} /></div>;

  return (
    <div className="max-w-4xl mx-auto space-y-6 pb-12">
      {/* Top Banner */}
      <div className="bg-white border border-gray-200 p-8 rounded-2xl shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-6 relative overflow-hidden">
        <div className="absolute top-0 left-0 w-full h-32 bg-gradient-to-r from-blue-50 to-purple-50"></div>
        <div className="flex items-end gap-6 relative z-10 pt-12">
          <div className="h-28 w-28 bg-white text-blue-600 rounded-full flex items-center justify-center text-4xl font-bold overflow-hidden border-4 border-white shadow-md flex-shrink-0">
            {currentUser?.photoURL ? (
              <img src={currentUser.photoURL} alt="Profile" className="h-full w-full object-cover" />
            ) : currentUser?.displayName ? (
              currentUser.displayName.charAt(0).toUpperCase()
            ) : (
              <User size={48} />
            )}
          </div>
          <div className="pb-2">
            <h1 className="text-3xl font-extrabold tracking-tight text-gray-900 mb-1">{currentUser?.displayName || 'Student Profile'}</h1>
            <p className="text-gray-600 flex items-center gap-2 font-medium">
              <Mail size={16} /> {currentUser?.email}
            </p>
          </div>
        </div>
        
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Left Column (Personal & Links) */}
        <div className="lg:col-span-1 space-y-6">
          <div className="bg-white border border-gray-200 rounded-2xl shadow-sm p-6 space-y-4">
            <h3 className="font-bold text-gray-900 flex items-center gap-2 border-b border-gray-100 pb-3">
              <User className="text-purple-600" size={18} /> Personal Details
            </h3>
            <div className="space-y-3">
              <div>
                <span className="text-xs font-semibold text-gray-400 uppercase tracking-wider block mb-1">Phone</span>
                <div className="flex items-center gap-2 text-gray-700 text-sm font-medium">
                  <Phone size={14} className="text-gray-400" /> {formData.phone || 'Not provided'}
                </div>
              </div>
              <div>
                <span className="text-xs font-semibold text-gray-400 uppercase tracking-wider block mb-1">Date of Birth</span>
                <div className="flex items-center gap-2 text-gray-700 text-sm font-medium">
                  <Calendar size={14} className="text-gray-400" /> {formData.dob || 'Not provided'}
                </div>
              </div>
              <div>
                <span className="text-xs font-semibold text-gray-400 uppercase tracking-wider block mb-1">Location</span>
                <div className="flex items-center gap-2 text-gray-700 text-sm font-medium">
                  <MapPin size={14} className="text-gray-400" /> {formData.location || 'Not provided'}
                </div>
              </div>
            </div>
          </div>

          <div className="bg-white border border-gray-200 rounded-2xl shadow-sm p-6 space-y-4">
            <h3 className="font-bold text-gray-900 flex items-center gap-2 border-b border-gray-100 pb-3">
              <Globe className="text-green-600" size={18} /> Social & Links
            </h3>
            <div className="space-y-3">
              {formData.github ? (
                <a href={formData.github} target="_blank" rel="noopener noreferrer" className="flex items-center gap-2 text-blue-600 hover:underline text-sm font-medium">
                  <Code size={16} /> GitHub Profile <ExternalLink size={12} />
                </a>
              ) : (
                <div className="flex items-center gap-2 text-gray-400 text-sm"><Code size={16}/> No GitHub linked</div>
              )}
              {formData.linkedin ? (
                <a href={formData.linkedin} target="_blank" rel="noopener noreferrer" className="flex items-center gap-2 text-blue-600 hover:underline text-sm font-medium">
                  <Briefcase size={16} /> LinkedIn Profile <ExternalLink size={12} />
                </a>
              ) : (
                <div className="flex items-center gap-2 text-gray-400 text-sm"><Briefcase size={16}/> No LinkedIn linked</div>
              )}
              {formData.portfolio ? (
                <a href={formData.portfolio} target="_blank" rel="noopener noreferrer" className="flex items-center gap-2 text-blue-600 hover:underline text-sm font-medium">
                  <Globe size={16} /> Portfolio Website <ExternalLink size={12} />
                </a>
              ) : (
                <div className="flex items-center gap-2 text-gray-400 text-sm"><Globe size={16}/> No Portfolio linked</div>
              )}
            </div>
          </div>
        </div>

        {/* Right Column (Academic & Bio) */}
        <div className="lg:col-span-2 space-y-6">
          <div className="bg-white border border-gray-200 rounded-2xl shadow-sm p-6">
            <h3 className="font-bold text-gray-900 flex items-center gap-2 border-b border-gray-100 pb-3 mb-4">
              <GraduationCap className="text-blue-600" size={20} /> Academic Information
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <span className="text-xs font-semibold text-gray-400 uppercase tracking-wider block mb-1">Institution</span>
                <p className="text-gray-900 font-medium">{formData.institution || '—'}</p>
              </div>
              <div>
                <span className="text-xs font-semibold text-gray-400 uppercase tracking-wider block mb-1">Degree & Major</span>
                <p className="text-gray-900 font-medium">{formData.degree || '—'}</p>
              </div>
              <div>
                <span className="text-xs font-semibold text-gray-400 uppercase tracking-wider block mb-1">Academic Standing</span>
                <p className="text-gray-900 font-medium">{formData.standing || '—'}</p>
              </div>
              <div>
                <span className="text-xs font-semibold text-gray-400 uppercase tracking-wider block mb-1">Student ID</span>
                <p className="text-gray-900 font-medium">{formData.studentId || '—'}</p>
              </div>
            </div>
          </div>

          <div className="bg-white border border-gray-200 rounded-2xl shadow-sm p-6">
            <h3 className="font-bold text-gray-900 flex items-center gap-2 border-b border-gray-100 pb-3 mb-4">
              <BookText className="text-orange-500" size={20} /> Bio & Academic Goals
            </h3>
            {formData.bio ? (
              <p className="text-gray-700 leading-relaxed text-sm md:text-base whitespace-pre-wrap">
                {formData.bio}
              </p>
            ) : (
              <p className="text-gray-400 italic text-sm">No bio or goals provided yet.</p>
            )}
          </div>
          
          <div className="bg-gray-50 border border-gray-200 rounded-2xl p-6 flex flex-col sm:flex-row items-center justify-between gap-4">
             <div className="flex items-center gap-2 text-gray-500 text-sm font-medium">
               <Shield size={16} /> Account ID: <span className="font-mono text-xs bg-white px-2 py-1 rounded border border-gray-200">{currentUser?.uid}</span>
             </div>
             <div className="flex items-center gap-2 text-gray-500 text-sm font-medium">
               <Calendar size={16} /> Member Since: <span className="text-gray-700 font-bold">{creationDate}</span>
             </div>
          </div>
        </div>

      </div>
    </div>
  );
}
