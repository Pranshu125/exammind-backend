import re
with open("src/components/SettingsView.jsx", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update Theme destructuring
content = content.replace(
    "const { theme, setTheme, fontSize, setFontSize } = useTheme();",
    "const { theme, setTheme, fontSize, setFontSize, accentColor, setAccentColor, layoutDensity, setLayoutDensity } = useTheme();"
)

# 2. Add extra options arrays
options_injection = """
  const accentOptions = [
    { value: 'blue', label: 'Blue (Default)' },
    { value: 'purple', label: 'Purple' },
    { value: 'green', label: 'Green' },
    { value: 'orange', label: 'Orange' }
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
"""
content = content.replace("const focusOptions = [", options_injection + "\n  const focusOptions = [")

# 3. Add email address to Profile basic details
old_name_field = """<div className="space-y-2 max-w-md">
              <label className="text-sm font-semibold text-gray-700 flex items-center gap-2">Display Name</label>
              <input type="text" value={displayName} onChange={(e) => setDisplayName(e.target.value)} placeholder="Enter your name" className="w-full p-3 bg-gray-50 border border-gray-200 rounded-lg focus:ring-2 focus:ring-black outline-none transition-all" />
            </div>"""
new_name_field = """<div className="grid grid-cols-1 md:grid-cols-2 gap-6 max-w-2xl">
              <div className="space-y-2">
                <label className="text-sm font-semibold text-gray-700 flex items-center gap-2">Display Name</label>
                <input type="text" value={displayName} onChange={(e) => setDisplayName(e.target.value)} placeholder="Enter your name" className="w-full p-3 bg-gray-50 border border-gray-200 rounded-lg focus:ring-2 focus:ring-black outline-none transition-all" />
              </div>
              <div className="space-y-2">
                <label className="text-sm font-semibold text-gray-700 flex items-center gap-2">Email Address</label>
                <input type="email" value={currentUser?.email || ''} disabled className="w-full p-3 bg-gray-100 border border-gray-200 rounded-lg text-gray-500 outline-none cursor-not-allowed" />
                <p className="text-[10px] text-gray-400">Email cannot be changed directly.</p>
              </div>
            </div>"""
content = content.replace(old_name_field, new_name_field)

# 4. Add timeZone to Profile Personal Details
old_location = """<div className="relative md:col-span-2">
                  <MapPin className="absolute left-3 top-3 text-gray-400" size={16} />
                  <input type="text" name="location" value={formData.location || ''} onChange={handleChange} placeholder="Location & Time Zone (e.g., NY, EST)" className="w-full bg-gray-50 border border-gray-200 rounded-lg pl-10 p-3 focus:ring-2 focus:ring-black outline-none transition-all text-sm" />
                </div>"""
new_location = """<div className="relative">
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
                </div>"""
content = content.replace(old_location, new_location)

# 5. Appearance Additions (Accent Color & Layout Density)
old_appearance_textsize = """<div className="border-t border-gray-100 pt-6">
              <h2 className="text-xl font-bold text-gray-900 mb-6 flex items-center gap-2">
                <BookText size={20} className="text-purple-600" /> Text Size
              </h2>
              <div className="space-y-4 max-w-md">
                <label className="text-sm font-semibold text-gray-700 block">Adjust Global Font Size</label>
                <CustomSelect 
                  value={fontSize}
                  onChange={(e) => setFontSize(e.target.value)}
                  options={fontSizeOptions}
                  className="w-full bg-gray-50"
                />
                <p className="text-xs text-gray-500">Increases or decreases the size of all text across the dashboard for better readability.</p>
              </div>
            </div>"""
new_appearance_textsize = """<div className="border-t border-gray-100 pt-6">
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
            </div>"""
content = content.replace(old_appearance_textsize, new_appearance_textsize)

# 6. Account section additions (Export, Linked Accounts, Delete Account)
old_danger_zone = """<div className="bg-white p-8 rounded-2xl shadow-sm border border-red-100">
            <h2 className="text-xl font-bold text-red-600 mb-2 flex items-center gap-2">
              Danger Zone
            </h2>
            <p className="text-gray-500 text-sm mb-6">Log out of your account on this device. You will need to sign in again to access your exams.</p>
            <button onClick={logout} className="bg-red-50 text-red-600 px-6 py-3 rounded-lg font-medium hover:bg-red-100 flex items-center gap-2 transition-colors">
              <LogOut size={18} /> Sign Out
            </button>
          </div>"""
new_account_extras = """
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
                <button type="button" className="text-sm font-bold text-blue-600 hover:underline">Link</button>
              </div>
              <div className="flex items-center justify-between p-4 border border-gray-200 rounded-xl">
                <div className="flex items-center gap-3">
                  <Code size={20} className="text-gray-400" />
                  <span className="font-semibold text-gray-900">GitHub</span>
                </div>
                <button type="button" className="text-sm font-bold text-blue-600 hover:underline">Link</button>
              </div>
            </div>
          </div>

          <div className="bg-white border border-gray-200 p-8 rounded-2xl shadow-sm">
            <h2 className="text-xl font-bold text-gray-900 mb-6 flex items-center gap-2">
              <BookText size={20} className="text-indigo-600" /> Data & Privacy
            </h2>
            <div className="space-y-4 max-w-md">
              <p className="text-sm text-gray-600 mb-4">Download a complete backup of your user data, uploaded syllabi, and study history.</p>
              <button type="button" onClick={() => alert('Exporting data...')} className="bg-gray-100 text-gray-800 px-6 py-3 rounded-xl font-bold shadow-sm hover:bg-gray-200 transition-colors flex items-center gap-2">
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
              <button onClick={() => alert('Delete account triggered. Require confirmation modal.')} className="bg-red-600 text-white px-6 py-3 rounded-xl font-bold hover:bg-red-700 flex items-center gap-2 transition-colors shadow-sm">
                Delete Account
              </button>
            </div>
          </div>
"""
content = content.replace(old_danger_zone, new_account_extras)


with open("src/components/SettingsView.jsx", "w", encoding="utf-8") as f:
    f.write(content)

print("done")
