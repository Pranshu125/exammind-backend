with open("src/contexts/ThemeContext.jsx", "r", encoding="utf-8") as f:
    content = f.read()

import re

# Remove the old accentColor effect block entirely
# We'll replace it with a comprehensive one that handles the "matte" look across the entire UI.

new_effect = """  useEffect(() => {
    window.document.documentElement.setAttribute('data-accent', accentColor);
    localStorage.setItem('accentColor', accentColor);
    
    window.document.documentElement.setAttribute('data-density', layoutDensity);
    localStorage.setItem('layoutDensity', layoutDensity);

    const styleId = 'exammind-dynamic-styles';
    let styleEl = document.getElementById(styleId);
    if (!styleEl) {
      styleEl = document.createElement('style');
      styleEl.id = styleId;
      document.head.appendChild(styleEl);
    }
    
    let vars = '';
    
    // Define Matte Palettes based on theme (Light vs Dark) and Accent Color
    if (theme !== 'dark') {
      if (accentColor === 'blue') {
        vars = `--matte-bg: #eceef2; --matte-surface: #f6f8fa; --matte-subtle: #e5e8ec; --matte-border: #d2d6dc; --matte-text: #2d3748; --matte-text-muted: #718096; --matte-primary: #4a6b8c; --matte-primary-hover: #3c5875; --matte-primary-light: #dce4eb;`;
      } else if (accentColor === 'purple') {
        vars = `--matte-bg: #f0edf4; --matte-surface: #f8f7f9; --matte-subtle: #e6e2ec; --matte-border: #d7d1e0; --matte-text: #3a3547; --matte-text-muted: #7a7387; --matte-primary: #7d6a98; --matte-primary-hover: #63527a; --matte-primary-light: #e4dced;`;
      } else if (accentColor === 'green') {
        vars = `--matte-bg: #ebf0ec; --matte-surface: #f4f7f5; --matte-subtle: #e1e8e2; --matte-border: #cdd9cf; --matte-text: #2f3b32; --matte-text-muted: #6e7d71; --matte-primary: #5c8266; --matte-primary-hover: #496b52; --matte-primary-light: #d9e6dc;`;
      } else if (accentColor === 'orange') {
        vars = `--matte-bg: #f4eeeb; --matte-surface: #fbf9f8; --matte-subtle: #ebe3e0; --matte-border: #dccfcb; --matte-text: #423430; --matte-text-muted: #8a7771; --matte-primary: #b56a56; --matte-primary-hover: #955442; --matte-primary-light: #ebd9d4;`;
      }
    } else {
      // Dark Mode Matte Palettes
      if (accentColor === 'blue') {
        vars = `--matte-bg: #1a1d24; --matte-surface: #242832; --matte-subtle: #2d323e; --matte-border: #3a4150; --matte-text: #e2e8f0; --matte-text-muted: #94a3b8; --matte-primary: #5c7c99; --matte-primary-hover: #7091af; --matte-primary-light: #2c3b4a;`;
      } else if (accentColor === 'purple') {
        vars = `--matte-bg: #1c1a21; --matte-surface: #26242c; --matte-subtle: #302d38; --matte-border: #3e3a47; --matte-text: #e2e8f0; --matte-text-muted: #94a3b8; --matte-primary: #8a7b9e; --matte-primary-hover: #a191b5; --matte-primary-light: #372f42;`;
      } else if (accentColor === 'green') {
        vars = `--matte-bg: #191c1a; --matte-surface: #232724; --matte-subtle: #2d332e; --matte-border: #3a423c; --matte-text: #e2e8f0; --matte-text-muted: #94a3b8; --matte-primary: #6c9176; --matte-primary-hover: #83a88d; --matte-primary-light: #2a3d30;`;
      } else if (accentColor === 'orange') {
        vars = `--matte-bg: #211c1a; --matte-surface: #2b2523; --matte-subtle: #362e2b; --matte-border: #453b38; --matte-text: #e2e8f0; --matte-text-muted: #94a3b8; --matte-primary: #bd7967; --matte-primary-hover: #d49282; --matte-primary-light: #4a2e26;`;
      }
    }
    
    let css = `
      :root {
        ${vars}
      }
      
      /* Global Matte Backgrounds */
      body, .min-h-screen, #root { background-color: var(--matte-bg) !important; color: var(--matte-text) !important; transition: background-color 0.3s ease, color 0.3s ease; }
      
      /* Surfaces and Cards (Removes Stark White/Black) */
      .bg-white, .dark\\\\:bg-gray-800, .bg-gray-800, .dark\\\\:bg-gray-900, .bg-gray-900 { 
        background-color: var(--matte-surface) !important; 
      }
      
      /* Subtle Backgrounds (Inputs, Sidebars, Hovers) */
      .bg-gray-50, .bg-gray-100, .dark\\\\:bg-gray-700, .dark\\\\:bg-gray-750, .dark\\\\:bg-gray-800\\\\/50 { 
        background-color: var(--matte-subtle) !important; 
      }
      
      /* Borders */
      .border-gray-100, .border-gray-200, .border-gray-300, .dark\\\\:border-gray-700, .dark\\\\:border-gray-800, .border-b { 
        border-color: var(--matte-border) !important; 
      }
      
      /* Text Overrides for Matte Softness */
      .text-gray-900, .text-gray-800, .text-black, .dark\\\\:text-white, .dark\\\\:text-gray-100 { color: var(--matte-text) !important; }
      .text-gray-700, .text-gray-600, .text-gray-500, .text-gray-400, .dark\\\\:text-gray-300, .dark\\\\:text-gray-400 { color: var(--matte-text-muted) !important; }
      
      /* Accent Color Mappings */
      .bg-blue-600, .bg-blue-500, .btn-primary { background-color: var(--matte-primary) !important; border-color: var(--matte-primary) !important; color: #ffffff !important; }
      .hover\\\\:bg-blue-700:hover, .btn-primary:hover { background-color: var(--matte-primary-hover) !important; }
      .text-blue-600, .text-blue-500 { color: var(--matte-primary) !important; }
      .border-blue-600, .border-blue-200 { border-color: var(--matte-primary) !important; }
      .ring-blue-500 { --tw-ring-color: var(--matte-primary) !important; }
      .bg-blue-100, .bg-blue-50 { background-color: var(--matte-primary-light) !important; }
      .text-blue-700 { color: var(--matte-primary) !important; }
      
      /* Miscellaneous Overrides */
      .shadow-sm, .shadow-md, .shadow-lg { box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.04) !important; }
      input, textarea, select { background-color: var(--matte-surface) !important; border-color: var(--matte-border) !important; color: var(--matte-text) !important; }
      
      /* Specific UI fixes */
      .text-white { color: #ffffff !important; }
      .text-purple-600, .text-emerald-600, .text-amber-600, .text-indigo-600, .text-teal-600, .text-red-500, .text-red-600 { color: var(--matte-primary) !important; }
      .bg-purple-100, .bg-emerald-100, .bg-amber-100, .bg-indigo-100, .bg-red-100 { background-color: var(--matte-primary-light) !important; }
    `;

    // Layout Density Override
    if (layoutDensity === 'compact') {
      css += `
        .p-8 { padding: 1.25rem !important; }
        .p-6 { padding: 1rem !important; }
        .space-y-8 > :not([hidden]) ~ :not([hidden]) { --tw-space-y-reverse: 0; margin-top: calc(1.5rem * calc(1 - var(--tw-space-y-reverse))) !important; margin-bottom: calc(1.5rem * var(--tw-space-y-reverse)) !important; }
        .space-y-6 > :not([hidden]) ~ :not([hidden]) { --tw-space-y-reverse: 0; margin-top: calc(1rem * calc(1 - var(--tw-space-y-reverse))) !important; margin-bottom: calc(1rem * var(--tw-space-y-reverse)) !important; }
        .gap-6 { gap: 1rem !important; }
        .mb-8 { margin-bottom: 1.5rem !important; }
        .mb-6 { margin-bottom: 1rem !important; }
        .py-4 { padding-top: 0.75rem !important; padding-bottom: 0.75rem !important; }
        .h-24 { height: 4.5rem !important; }
        .w-24 { width: 4.5rem !important; }
      `;
    }

    styleEl.innerHTML = css;

  }, [theme, accentColor, layoutDensity]);
"""

# Now we need to isolate the old big useEffect and replace it.
import re
pattern = re.compile(r"useEffect\(\(\) => \{[\s\S]*?window\.document\.documentElement\.setAttribute\('data-accent'[\s\S]*?\}, \[accentColor, layoutDensity\]\);", re.MULTILINE)
content = pattern.sub(new_effect.replace('\\', '\\\\'), content) # escape slashes for python writing

with open("src/contexts/ThemeContext.jsx", "w", encoding="utf-8") as f:
    f.write(content)

print("done")
