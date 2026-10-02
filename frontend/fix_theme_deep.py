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
    
    // Define Deep Matte Palettes
    if (theme !== 'dark') {
      if (accentColor === 'green') {
        vars = `--matte-bg: #e6eae8; --matte-surface: #f1f4f2; --matte-subtle: #dfe6e2; --matte-border: #c8d4ce; --matte-text: #2c3b33; --matte-text-muted: #6b7a70; --matte-primary: #3b4d45; --matte-primary-hover: #2d3b34; --matte-primary-light: #d4dcd7; --matte-hero: #24302b;`;
      } else if (accentColor === 'blue') {
        vars = `--matte-bg: #e6ebf0; --matte-surface: #f0f4f7; --matte-subtle: #dbe4ec; --matte-border: #c3d1de; --matte-text: #222d3b; --matte-text-muted: #65778a; --matte-primary: #314152; --matte-primary-hover: #23303d; --matte-primary-light: #d0dce8; --matte-hero: #1c2733;`;
      } else if (accentColor === 'purple') {
        vars = `--matte-bg: #ece6ed; --matte-surface: #f5f1f5; --matte-subtle: #e3dae6; --matte-border: #cfc2d1; --matte-text: #312333; --matte-text-muted: #756478; --matte-primary: #453347; --matte-primary-hover: #322433; --matte-primary-light: #e1cfe3; --matte-hero: #281d29;`;
      } else if (accentColor === 'orange') {
        vars = `--matte-bg: #ede8e6; --matte-surface: #f7f4f2; --matte-subtle: #e6ddd8; --matte-border: #d4c3ba; --matte-text: #3b251d; --matte-text-muted: #7d655c; --matte-primary: #753c29; --matte-primary-hover: #572a1a; --matte-primary-light: #e6cdbe; --matte-hero: #3b1c11;`;
      } else {
        // White / Monochrome
        vars = `--matte-bg: #efefef; --matte-surface: #f8f8f8; --matte-subtle: #e5e5e5; --matte-border: #d4d4d4; --matte-text: #262626; --matte-text-muted: #737373; --matte-primary: #3b3b3b; --matte-primary-hover: #262626; --matte-primary-light: #e0e0e0; --matte-hero: #1a1a1a;`;
      }
    } else {
      // Dark Mode Deep Matte
      if (accentColor === 'green') {
        vars = `--matte-bg: #1b211d; --matte-surface: #222924; --matte-subtle: #2c362f; --matte-border: #3d4d44; --matte-text: #e6ebe8; --matte-text-muted: #8b9c91; --matte-primary: #577566; --matte-primary-hover: #698c7b; --matte-primary-light: #25362c; --matte-hero: #141a17;`;
      } else if (accentColor === 'blue') {
        vars = `--matte-bg: #1a1e24; --matte-surface: #222830; --matte-subtle: #2a333d; --matte-border: #384654; --matte-text: #e6eaed; --matte-text-muted: #8496a8; --matte-primary: #5a7694; --matte-primary-hover: #6e8ca8; --matte-primary-light: #25313d; --matte-hero: #14181c;`;
      } else if (accentColor === 'purple') {
        vars = `--matte-bg: #211c24; --matte-surface: #2a232e; --matte-subtle: #342b38; --matte-border: #443a4a; --matte-text: #ebe6eb; --matte-text-muted: #968699; --matte-primary: #856a8c; --matte-primary-hover: #9b7ea3; --matte-primary-light: #372a3b; --matte-hero: #18141a;`;
      } else if (accentColor === 'orange') {
        vars = `--matte-bg: #241c19; --matte-surface: #2e231f; --matte-subtle: #3a2c26; --matte-border: #4a3a33; --matte-text: #ebe8e6; --matte-text-muted: #99837a; --matte-primary: #b36e52; --matte-primary-hover: #c98265; --matte-primary-light: #3d2319; --matte-hero: #1a1411;`;
      } else {
        // White / Monochrome Dark
        vars = `--matte-bg: #171717; --matte-surface: #262626; --matte-subtle: #333333; --matte-border: #404040; --matte-text: #f5f5f5; --matte-text-muted: #a3a3a3; --matte-primary: #d4d4d4; --matte-primary-hover: #f5f5f5; --matte-primary-light: #404040; --matte-hero: #0a0a0a;`;
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
      .border-gray-100, .border-gray-200, .border-gray-300, .dark\\\\:border-gray-700, .dark\\\\:border-gray-800, .border-b { 
        border-color: var(--matte-border) !important; 
      }
      
      /* Texts */
      .text-gray-900, .text-gray-800, .text-black, .dark\\\\:text-white, .dark\\\\:text-gray-100 { color: var(--matte-text) !important; }
      .text-gray-700, .text-gray-600, .text-gray-500, .text-gray-400, .dark\\\\:text-gray-300, .dark\\\\:text-gray-400 { color: var(--matte-text-muted) !important; }
      
      /* Map ALL Primary UI Buttons/Highlights */
      .bg-blue-600, .bg-blue-500, .btn-primary, .bg-purple-500, .bg-purple-600 { 
        background-color: var(--matte-primary) !important; 
        border-color: var(--matte-primary) !important; 
        color: ${accentColor === 'white' && theme !== 'dark' ? '#ffffff' : '#ffffff'} !important; 
      }
      .hover\\\\:bg-blue-700:hover, .btn-primary:hover { background-color: var(--matte-primary-hover) !important; }
      .text-blue-600, .text-blue-500, .text-purple-500, .text-purple-600 { color: var(--matte-primary) !important; }
      .border-blue-600, .border-blue-200, .border-purple-500, .border-purple-200 { border-color: var(--matte-primary) !important; }
      .ring-blue-500, .ring-purple-500 { --tw-ring-color: var(--matte-primary) !important; }
      
      /* Primary Lights (Pills, Checkboxes bg) */
      .bg-blue-100, .bg-blue-50, .bg-purple-100, .bg-purple-50, .bg-purple-500\\\\/20 { 
        background-color: var(--matte-primary-light) !important; 
      }
      .text-blue-700, .text-blue-300, .text-purple-300 { color: var(--matte-primary) !important; }
      
      /* Input overrides */
      input, textarea, select { 
        background-color: var(--matte-surface) !important; 
        border-color: var(--matte-border) !important; 
        color: var(--matte-text) !important; 
      }
      
      /* Subtle Shadows for depth without harsh contrast */
      .shadow-sm, .shadow-md, .shadow-lg { box-shadow: 0 4px 24px -4px rgba(0, 0, 0, 0.08) !important; }
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
