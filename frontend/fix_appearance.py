with open("src/components/SettingsView.jsx", "r", encoding="utf-8") as f:
    content = f.read()

# Add fontSize, setFontSize to useTheme destructuring
content = content.replace(
    "const { theme, setTheme } = useTheme();",
    "const { theme, setTheme, fontSize, setFontSize } = useTheme();"
)

# Add fontSizeOptions array
options_code = """  const themeOptions = [
    { value: 'light', label: 'Light Mode' },
    { value: 'dark', label: 'Dark Mode' }
  ];"""
new_options = """  const themeOptions = [
    { value: 'light', label: 'Light Mode' },
    { value: 'dark', label: 'Dark Mode' }
  ];
  
  const fontSizeOptions = [
    { value: 'small', label: 'Small' },
    { value: 'medium', label: 'Medium (Default)' },
    { value: 'large', label: 'Large' },
    { value: 'xlarge', label: 'Extra Large' }
  ];"""
content = content.replace(options_code, new_options)

# Update Appearance tab JSX
old_app_tab = """      {/* TAB: APPEARANCE */}
      {activeTab === 'appearance' && (
        <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
          <div className="bg-white border border-gray-200 p-8 rounded-2xl shadow-sm">
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
        </div>
      )}"""

new_app_tab = """      {/* TAB: APPEARANCE */}
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
            </div>
          </div>
        </div>
      )}"""

content = content.replace(old_app_tab, new_app_tab)

with open("src/components/SettingsView.jsx", "w", encoding="utf-8") as f:
    f.write(content)

print("done")
