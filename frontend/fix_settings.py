with open("src/components/SettingsView.jsx", "w", encoding="utf-8") as f:
    f.write("""import { useState, useRef, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { useTheme } from '../contexts/ThemeContext';
import { updateProfile, updatePassword } from 'firebase/auth';
import { ref, uploadBytes, getDownloadURL } from 'firebase/storage';
import { doc, getDoc, setDoc } from 'firebase/firestore';
import { storage, db } from '../lib/firebase';
import { LogOut, User, Shield, Loader2, Palette, Camera, GraduationCap, MapPin, Phone, Code, Briefcase, Globe, BookText } from 'lucide-react';
import CustomSelect from './CustomSelect';

export default function SettingsView() {
  const { currentUser, logout } = useAuth();
  const { theme, setTheme } = useTheme();
  
  const [displayName, setDisplayName] = useState(currentUser?.displayName || '');
  const [newPassword, setNewPassword] = useState('');
  
  // Extra Profile Fields
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

  const [loading, setLoading] = useState(false);
  const [imageLoading, setImageLoading] = useState(false);
  const [message, setMessage] = useState({ text: '', type: '' });
  const fileInputRef = useRef(null);

  const themeOptions = [
    { value: 'light', label: 'Light Mode' },
    { value: 'dark', label: 'Dark Mode' }
  ];

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
      }
    };
    fetchProfile();
  }, [currentUser]);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
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
    e.preventDefault();
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

      // Save Firestore fields
      const docRef = doc(db, `users`, currentUser.uid);
      promises.push(setDoc(docRef, { profile: formData }, { merge: true }));

      await Promise.all(promises);
      await currentUser.reload();
      
      setMessage({ text: 'All settings updated successfully!', type: 'success' });
      setNewPassword(''); 
    } catch (error) {
      setMessage({ text: error.message, type: 'error' });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6 pb-12">
      
      {/* Theme Settings */}
      <div className="bg-white border border-gray-200 p-8 rounded-xl shadow-sm">
        <h2 className="text-xl font-bold text-gray-900 mb-6 flex items-center gap-2">
          <Palette size={20} className="text-blue-600" /> Appearance
        </h2>
        <div className="space-y-4">
          <label className="text-sm font-semibold text-gray-700 block">App Theme</label>
          <CustomSelect 
            value={theme}
            onChange={(e) => setTheme(e.target.value)}
            options={themeOptions}
            className="w-full md:w-1/2 bg-gray-50"
          />
        </div>
      </div>

      <form onSubmit={handleUpdateProfile} className="space-y-6">
        {/* Core Account Edit */}
        <div className="bg-white border border-gray-200 p-8 rounded-xl shadow-sm">
          <h2 className="text-xl font-bold text-gray-900 mb-6 flex items-center gap-2">
            <User size={20} className="text-blue-600" /> Account Settings
          </h2>
          
          {message.text && (
            <div className={`p-4 rounded-lg mb-6 text-sm font-medium ${message.type === 'error' ? 'bg-red-50 text-red-600' : 'bg-green-50 text-green-600'}`}>
              {message.text}
            </div>
          )}

          {/* Profile Picture Upload */}
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

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="space-y-2">
              <label className="text-sm font-semibold text-gray-700 flex items-center gap-2">
                Display Name
              </label>
              <input type="text" value={displayName} onChange={(e) => setDisplayName(e.target.value)} placeholder="Enter your name" className="w-full p-3 bg-gray-50 border border-gray-200 rounded-lg focus:ring-2 focus:ring-black outline-none transition-all" />
            </div>
            <div className="space-y-2">
              <label className="text-sm font-semibold text-gray-700 flex items-center gap-2">
                New Password
              </label>
              <input type="password" value={newPassword} onChange={(e) => setNewPassword(e.target.value)} placeholder="Leave blank to keep current" className="w-full p-3 bg-gray-50 border border-gray-200 rounded-lg focus:ring-2 focus:ring-black outline-none transition-all" />
            </div>
          </div>
        </div>

        {/* Extended Settings (Academic & Personal) */}
        <div className="bg-white border border-gray-200 p-8 rounded-xl shadow-sm space-y-8">
          
          <div>
            <h3 className="text-lg font-bold text-gray-900 flex items-center gap-2 mb-4">
              <GraduationCap className="text-blue-600" size={20}/> Academic Information
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <input type="text" name="institution" value={formData.institution} onChange={handleChange} placeholder="Institution Name (e.g., VIT Bhopal)" className="w-full bg-gray-50 border border-gray-200 rounded-lg p-3 focus:ring-2 focus:ring-black outline-none transition-all text-sm" />
              <input type="text" name="degree" value={formData.degree} onChange={handleChange} placeholder="Degree & Major (e.g., B.Tech in CS)" className="w-full bg-gray-50 border border-gray-200 rounded-lg p-3 focus:ring-2 focus:ring-black outline-none transition-all text-sm" />
              <input type="text" name="standing" value={formData.standing} onChange={handleChange} placeholder="Academic Standing (e.g., Semester 4)" className="w-full bg-gray-50 border border-gray-200 rounded-lg p-3 focus:ring-2 focus:ring-black outline-none transition-all text-sm" />
              <input type="text" name="studentId" value={formData.studentId} onChange={handleChange} placeholder="Student ID / Roll Number" className="w-full bg-gray-50 border border-gray-200 rounded-lg p-3 focus:ring-2 focus:ring-black outline-none transition-all text-sm" />
            </div>
          </div>

          <div className="border-t border-gray-100 pt-6">
            <h3 className="text-lg font-bold text-gray-900 flex items-center gap-2 mb-4">
              <User className="text-purple-600" size={20}/> Basic Personal Details
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="relative">
                <Phone className="absolute left-3 top-3 text-gray-400" size={16} />
                <input type="tel" name="phone" value={formData.phone} onChange={handleChange} placeholder="Phone Number" className="w-full bg-gray-50 border border-gray-200 rounded-lg pl-10 p-3 focus:ring-2 focus:ring-black outline-none transition-all text-sm" />
              </div>
              <input type="date" name="dob" value={formData.dob} onChange={handleChange} className="w-full bg-gray-50 border border-gray-200 rounded-lg p-3 focus:ring-2 focus:ring-black outline-none transition-all text-sm text-gray-700" />
              <div className="relative md:col-span-2">
                <MapPin className="absolute left-3 top-3 text-gray-400" size={16} />
                <input type="text" name="location" value={formData.location} onChange={handleChange} placeholder="Location & Time Zone (e.g., NY, EST)" className="w-full bg-gray-50 border border-gray-200 rounded-lg pl-10 p-3 focus:ring-2 focus:ring-black outline-none transition-all text-sm" />
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
                <input type="url" name="github" value={formData.github} onChange={handleChange} placeholder="GitHub Profile URL" className="w-full bg-gray-50 border border-gray-200 rounded-lg pl-10 p-3 focus:ring-2 focus:ring-black outline-none transition-all text-sm" />
              </div>
              <div className="relative">
                <Briefcase className="absolute left-3 top-3 text-gray-400" size={16} />
                <input type="url" name="linkedin" value={formData.linkedin} onChange={handleChange} placeholder="LinkedIn Profile URL" className="w-full bg-gray-50 border border-gray-200 rounded-lg pl-10 p-3 focus:ring-2 focus:ring-black outline-none transition-all text-sm" />
              </div>
              <div className="relative md:col-span-2">
                <Globe className="absolute left-3 top-3 text-gray-400" size={16} />
                <input type="url" name="portfolio" value={formData.portfolio} onChange={handleChange} placeholder="Personal Portfolio URL" className="w-full bg-gray-50 border border-gray-200 rounded-lg pl-10 p-3 focus:ring-2 focus:ring-black outline-none transition-all text-sm" />
              </div>
              <div className="relative md:col-span-2">
                <BookText className="absolute left-3 top-3 text-gray-400" size={16} />
                <textarea name="bio" value={formData.bio} onChange={handleChange} rows="3" placeholder="Bio / Academic Goals..." className="w-full bg-gray-50 border border-gray-200 rounded-lg pl-10 p-3 focus:ring-2 focus:ring-black outline-none transition-all text-sm resize-none"></textarea>
              </div>
            </div>
          </div>

          <div className="border-t border-gray-100 pt-6 flex justify-end">
            <button type="submit" disabled={loading} className="btn-primary px-8 py-3 rounded-xl flex items-center gap-2 font-bold shadow-md hover:shadow-lg transition-all disabled:opacity-50">
              {loading && <Loader2 size={18} className="animate-spin" />}
              Save All Settings
            </button>
          </div>
        </div>
      </form>

      {/* Danger Zone */}
      <div className="bg-white p-8 rounded-xl shadow-sm border border-red-100">
        <h2 className="text-xl font-bold text-red-600 mb-2 flex items-center gap-2">
          Account Actions
        </h2>
        <p className="text-gray-500 text-sm mb-6">Log out of your account on this device.</p>
        <button onClick={logout} className="bg-red-50 text-red-600 px-6 py-3 rounded-lg font-medium hover:bg-red-100 flex items-center gap-2 transition-colors">
          <LogOut size={18} /> Sign Out
        </button>
      </div>

    </div>
  );
}
""")
print("done")
