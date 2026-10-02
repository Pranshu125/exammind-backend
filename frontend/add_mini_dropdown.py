with open("src/pages/Dashboard.jsx", "r", encoding="utf-8") as f:
    content = f.read()

# Add useAI import
if "useAI" not in content:
    content = content.replace(
        "import { Routes, Route, useLocation, useNavigate } from 'react-router-dom';",
        "import { Routes, Route, useLocation, useNavigate } from 'react-router-dom';\nimport { useAI } from '../contexts/AIContext';"
    )

# Add state
if "const { engine, setEngine } = useAI();" not in content:
    content = content.replace(
        "const [desktopSidebarOpen, setDesktopSidebarOpen] = useState(true);",
        "const [desktopSidebarOpen, setDesktopSidebarOpen] = useState(true);\n  const { engine, setEngine } = useAI();\n  const [showEngineDropdown, setShowEngineDropdown] = useState(false);"
    )

# Replace the Cpu button block
old_cpu = """              <button 
                onClick={() => navigate('/settings')}
                className="p-2 text-gray-400 hover:text-white transition-colors rounded-lg hover:bg-white/10"
                title="AI Settings"
              >
                <Cpu size={20} />
              </button>"""

new_cpu = """              <div className="relative">
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
              </div>"""

content = content.replace(old_cpu, new_cpu)

with open("src/pages/Dashboard.jsx", "w", encoding="utf-8") as f:
    f.write(content)
print("done")
