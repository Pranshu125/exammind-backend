with open("src/components/SettingsView.jsx", "r", encoding="utf-8") as f:
    content = f.read()

import re

# We need to change the initial state from 'profile' to 'menu'
content = content.replace("useState('profile')", "useState('menu')")
content = content.replace("import { LogOut, User, Shield, Loader2, Palette, Camera, GraduationCap, MapPin, Phone, Code, Briefcase, Globe, BookText, Settings as SettingsIcon }", "import { LogOut, User, Shield, Loader2, Palette, Camera, GraduationCap, MapPin, Phone, Code, Briefcase, Globe, BookText, Settings as SettingsIcon, ChevronRight, ArrowLeft }")

# Replace the header and tabs with the new menu layout
old_tabs = """      <div className="mb-6">
        <h2 className="text-3xl font-bold tracking-tight text-gray-900 mb-2">Settings</h2>
        <p className="text-gray-500">Manage your account preferences and profile information.</p>
      </div>

      {/* Tabs */}
      <div className="flex space-x-2 bg-gray-100 p-1.5 rounded-xl mb-6 overflow-x-auto">
        <button 
          className={`flex-1 py-2.5 px-4 text-sm font-bold rounded-lg transition-all whitespace-nowrap flex items-center justify-center gap-2 ${activeTab === 'profile' ? 'bg-white shadow-sm text-blue-600' : 'text-gray-500 hover:text-gray-700 hover:bg-gray-200/50'}`} 
          onClick={() => { setActiveTab('profile'); setMessage({text:'', type:''}); }}
        >
          <User size={16} /> Edit Profile
        </button>
        <button 
          className={`flex-1 py-2.5 px-4 text-sm font-bold rounded-lg transition-all whitespace-nowrap flex items-center justify-center gap-2 ${activeTab === 'account' ? 'bg-white shadow-sm text-blue-600' : 'text-gray-500 hover:text-gray-700 hover:bg-gray-200/50'}`} 
          onClick={() => { setActiveTab('account'); setMessage({text:'', type:''}); }}
        >
          <Shield size={16} /> Account & Security
        </button>
        <button 
          className={`flex-1 py-2.5 px-4 text-sm font-bold rounded-lg transition-all whitespace-nowrap flex items-center justify-center gap-2 ${activeTab === 'appearance' ? 'bg-white shadow-sm text-blue-600' : 'text-gray-500 hover:text-gray-700 hover:bg-gray-200/50'}`} 
          onClick={() => { setActiveTab('appearance'); setMessage({text:'', type:''}); }}
        >
          <Palette size={16} /> Appearance
        </button>
      </div>"""

new_tabs = """      {activeTab === 'menu' ? (
        <div className="max-w-2xl mx-auto space-y-6">
          <div className="mb-6">
            <h2 className="text-3xl font-bold tracking-tight text-gray-900 mb-2">Settings</h2>
            <p className="text-gray-500">Manage your account preferences and profile information.</p>
          </div>
          <div className="bg-white border border-gray-200 rounded-2xl shadow-sm overflow-hidden flex flex-col">
            <div className="px-6 py-4 bg-gray-50 border-b border-gray-200 font-bold text-gray-900 text-lg uppercase tracking-wider">
              Settings Menu
            </div>
            
            <button onClick={() => { setActiveTab('profile'); setMessage({text:'', type:''}); }} className="flex items-center justify-between p-6 bg-white hover:bg-gray-50 border-b border-gray-100 transition-colors text-left group">
              <div className="flex items-center gap-4">
                <div className="bg-blue-100 text-blue-600 p-2.5 rounded-xl group-hover:scale-110 transition-transform"><User size={20} /></div>
                <span className="font-semibold text-gray-900 text-lg">Profile Edit</span>
              </div>
              <ChevronRight className="text-gray-400 group-hover:text-blue-600 transition-colors" />
            </button>
            
            <button onClick={() => { setActiveTab('appearance'); setMessage({text:'', type:''}); }} className="flex items-center justify-between p-6 bg-white hover:bg-gray-50 border-b border-gray-100 transition-colors text-left group">
              <div className="flex items-center gap-4">
                <div className="bg-purple-100 text-purple-600 p-2.5 rounded-xl group-hover:scale-110 transition-transform"><Palette size={20} /></div>
                <span className="font-semibold text-gray-900 text-lg">Appearance</span>
              </div>
              <ChevronRight className="text-gray-400 group-hover:text-purple-600 transition-colors" />
            </button>
            
            <button onClick={() => { setActiveTab('account'); setMessage({text:'', type:''}); }} className="flex items-center justify-between p-6 bg-white hover:bg-gray-50 transition-colors text-left group">
              <div className="flex items-center gap-4">
                <div className="bg-red-100 text-red-600 p-2.5 rounded-xl group-hover:scale-110 transition-transform"><Shield size={20} /></div>
                <span className="font-semibold text-gray-900 text-lg">Account</span>
              </div>
              <ChevronRight className="text-gray-400 group-hover:text-red-600 transition-colors" />
            </button>
          </div>
        </div>
      ) : (
        <div className="mb-6 flex items-center justify-between">
          <button onClick={() => setActiveTab('menu')} className="flex items-center gap-2 text-gray-500 hover:text-black font-semibold transition-colors bg-white px-4 py-2 rounded-xl border border-gray-200 shadow-sm hover:shadow-md">
            <ArrowLeft size={18} /> Back to Settings
          </button>
        </div>
      )}"""

content = content.replace(old_tabs, new_tabs)

with open("src/components/SettingsView.jsx", "w", encoding="utf-8") as f:
    f.write(content)

print("done")
