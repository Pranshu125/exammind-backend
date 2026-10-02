with open("src/contexts/ThemeContext.jsx", "w", encoding="utf-8") as f:
    f.write("""import { createContext, useContext, useEffect, useState } from 'react';

const ThemeContext = createContext();

export function useTheme() {
  return useContext(ThemeContext);
}

export function ThemeProvider({ children }) {
  const [theme, setTheme] = useState(() => localStorage.getItem('theme') || 'light');
  const [fontSize, setFontSize] = useState(() => localStorage.getItem('fontSize') || 'medium');
  const [accentColor, setAccentColor] = useState(() => localStorage.getItem('accentColor') || 'blue');
  const [layoutDensity, setLayoutDensity] = useState(() => localStorage.getItem('layoutDensity') || 'comfortable');

  useEffect(() => {
    const root = window.document.documentElement;
    if (theme === 'dark') {
      root.classList.add('dark');
    } else {
      root.classList.remove('dark');
    }
    localStorage.setItem('theme', theme);
  }, [theme]);

  useEffect(() => {
    const root = window.document.documentElement;
    let size = '16px';
    if (fontSize === 'small') size = '14px';
    if (fontSize === 'large') size = '18px';
    if (fontSize === 'xlarge') size = '20px';
    
    root.style.fontSize = size;
    localStorage.setItem('fontSize', fontSize);
  }, [fontSize]);

  useEffect(() => {
    window.document.documentElement.setAttribute('data-accent', accentColor);
    localStorage.setItem('accentColor', accentColor);
  }, [accentColor]);

  useEffect(() => {
    window.document.documentElement.setAttribute('data-density', layoutDensity);
    localStorage.setItem('layoutDensity', layoutDensity);
  }, [layoutDensity]);

  return (
    <ThemeContext.Provider value={{ 
      theme, setTheme, 
      fontSize, setFontSize, 
      accentColor, setAccentColor, 
      layoutDensity, setLayoutDensity 
    }}>
      {children}
    </ThemeContext.Provider>
  );
}
""")
print("done")
