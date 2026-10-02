import re

with open("src/contexts/ThemeContext.jsx", "r", encoding="utf-8") as f:
    content = f.read()

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
    
    // Fully Integrated Color Modes (Removing all white from colored shades)
    if (accentColor === 'green') {
      vars = `--matte-bg: #2a3b32; --matte-surface: #344a3e; --matte-subtle: #3f594a; --matte-border: #4a6958; --matte-text: #f0f4f1; --matte-text-muted: #9bb3a4; --matte-primary: #5e8771; --matte-primary-hover: #719e86; --matte-primary-light: #2c4236; --matte-hero: #1f2c25;`;
    } else if (accentColor === 'blue') {
      vars = `--matte-bg: #1e293b; --matte-surface: #27354c; --matte-subtle: #31435e; --matte-border: #3d5273; --matte-text: #f1f5f9; --matte-text-muted: #94a3b8; --matte-primary: #567bb3; --matte-primary-hover: #6e93cc; --matte-primary-light: #1d2e45; --matte-hero: #151d2b;`;
    } else if (accentColor === 'purple') {
      vars = `--matte-bg: #2d2036; --matte-surface: #3b2a47; --matte-subtle: #4a3559; --matte-border: #58406b; --matte-text: #f5f0f7; --matte-text-muted: #b09db8; --matte-primary: #84629e; --matte-primary-hover: #9d7ab8; --matte-primary-light: #2e1c3b; --matte-hero: #211728;`;
    } else if (accentColor === 'orange') {
      vars = `--matte-bg: #38221b; --matte-surface: #472b22; --matte-subtle: #57352a; --matte-border: #694033; --matte-text: #f7f1ef; --matte-text-muted: #b89e95; --matte-primary: #a85c40; --matte-primary-hover: #c47052; --matte-primary-light: #3d2017; --matte-hero: #291813;`;
    } else {
      // Monochrome (White/Black) - Respects Light/Dark Mode
      if (theme !== 'dark') {
        vars = `--matte-bg: #e5e5e5; --matte-surface: #f4f4f4; --matte-subtle: #d4d4d4; --matte-border: #cccccc; --matte-text: #1a1a1a; --matte-text-muted: #666666; --matte-primary: #333333; --matte-primary-hover: #1a1a1a; --matte-primary-light: #d4d4d4; --matte-hero: #1a1a1a;`;
      } else {
        vars = `--matte-bg: #171717; --matte-surface: #262626; --matte-subtle: #333333; --matte-border: #404040; --matte-text: #f5f5f5; --matte-text-muted: #a3a3a3; --matte-primary: #d4d4d4; --matte-primary-hover: #ffffff; --matte-primary-light: #404040; --matte-hero: #0a0a0a;`;
      }
    }
    
    let css = `
      :root {
        ${vars}
      }
      
      /* Pure Eradication of White and Black Backgrounds */
      body, #root, .min-h-screen { background-color: var(--matte-bg) !important; color: var(--matte-text) !important; }
      
      .bg-white, .dark\\\\:bg-gray-800, .bg-gray-800, .bg-gray-900, .dark\\\\:bg-gray-900 { 
        background-color: var(--matte-surface) !important; 
      }
      
      /* Eviscerate hardcoded dark sections/heroes */
      .bg-gradient-to-br, .from-gray-900, .to-black, .bg-black {
        background: none !important;
        background-color: var(--matte-hero) !important;
      }
      
      /* Subtle components (Sidebar, Inputs) */
      .bg-gray-50, .bg-gray-100, .dark\\\\:bg-gray-700, .dark\\\\:bg-gray-750, .dark\\\\:bg-gray-800\\\\/50 { 
        background-color: var(--matte-subtle) !important; 
      }
      
      /* Borders */
      .border-gray-100, .border-gray-200, .border-gray-300, .dark\\\\:border-gray-700, .dark\\\\:border-gray-800, .border-b, .border-t { 
        border-color: var(--matte-border) !important; 
      }
      
      /* Texts */
      .text-gray-900, .text-gray-800, .text-black, .dark\\\\:text-white, .dark\\\\:text-gray-100 { color: var(--matte-text) !important; }
      .text-gray-700, .text-gray-600, .text-gray-500, .text-gray-400, .dark\\\\:text-gray-300, .dark\\\\:text-gray-400 { color: var(--matte-text-muted) !important; }
      
      /* Map ALL Primary UI Buttons/Highlights */
      .bg-blue-600, .bg-blue-500, .btn-primary, .bg-purple-500, .bg-purple-600, .bg-emerald-600, .bg-indigo-600, .bg-teal-600 { 
        background-color: var(--matte-primary) !important; 
        border-color: var(--matte-primary) !important; 
        color: ${accentColor === 'white' && theme !== 'dark' ? '#ffffff' : '#ffffff'} !important; 
      }
      .hover\\\\:bg-blue-700:hover, .btn-primary:hover { background-color: var(--matte-primary-hover) !important; }
      .text-blue-600, .text-blue-500, .text-purple-500, .text-purple-600, .text-emerald-600, .text-amber-600, .text-indigo-600, .text-teal-600, .text-pink-600 { color: var(--matte-primary) !important; }
      .border-blue-600, .border-blue-200, .border-purple-500, .border-purple-200 { border-color: var(--matte-primary) !important; }
      .ring-blue-500, .ring-purple-500 { --tw-ring-color: var(--matte-primary) !important; }
      
      /* Primary Lights (Pills, Checkboxes bg) */
      .bg-blue-100, .bg-blue-50, .bg-purple-100, .bg-purple-50, .bg-purple-500\\\\/20, .bg-emerald-100, .bg-amber-100, .bg-indigo-100, .bg-teal-100, .bg-pink-100, .bg-red-100 { 
        background-color: var(--matte-primary-light) !important; 
      }
      .text-blue-700, .text-blue-300, .text-purple-300 { color: var(--matte-primary) !important; }
      
      /* Input overrides */
      input, textarea, select { 
        background-color: var(--matte-subtle) !important; 
        border-color: var(--matte-border) !important; 
        color: var(--matte-text) !important; 
      }
      ::placeholder { color: var(--matte-text-muted) !important; opacity: 0.7; }
      
      /* Subtle Shadows for depth without harsh contrast */
      .shadow-sm, .shadow-md, .shadow-lg { box-shadow: 0 4px 24px -4px rgba(0, 0, 0, 0.2) !important; }
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

pattern = re.compile(r"useEffect\(\(\) => \{[\s\S]*?window\.document\.documentElement\.setAttribute\('data-accent'[\s\S]*?\}, \[theme, accentColor, layoutDensity\]\);", re.MULTILINE)
content = pattern.sub(new_effect.replace('\\', '\\\\'), content)

with open("src/contexts/ThemeContext.jsx", "w", encoding="utf-8") as f:
    f.write(content)

print("done")
