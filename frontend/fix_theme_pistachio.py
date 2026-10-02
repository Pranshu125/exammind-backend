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
    
    // Light Mode (Pastel / Pistachio) vs Dark Mode (Deep Shades)
    if (theme !== 'dark') {
      if (accentColor === 'green') {
        vars = `--matte-bg: #e8f2e9; --matte-surface: #dcebdc; --matte-subtle: #d0e3d0; --matte-border: #b8c9b9; --matte-text: #172b1d; --matte-text-muted: #3a5240; --matte-primary: #3d6e4b; --matte-primary-hover: #2d5438; --matte-primary-light: #c8e0cc; --matte-hero: #c8e0cc;`;
      } else if (accentColor === 'blue') {
        vars = `--matte-bg: #e6eff7; --matte-surface: #d9e6f2; --matte-subtle: #ccdded; --matte-border: #b3c7d9; --matte-text: #1a2636; --matte-text-muted: #3b4f63; --matte-primary: #4373a5; --matte-primary-hover: #325a85; --matte-primary-light: #c8dcf0; --matte-hero: #c8dcf0;`;
      } else if (accentColor === 'purple') {
        vars = `--matte-bg: #f0ebf5; --matte-surface: #e5dcf0; --matte-subtle: #dacfe6; --matte-border: #c4b5d1; --matte-text: #2c1c38; --matte-text-muted: #4e395e; --matte-primary: #775094; --matte-primary-hover: #5d3d75; --matte-primary-light: #decce8; --matte-hero: #decce8;`;
      } else if (accentColor === 'orange') {
        vars = `--matte-bg: #f7ebe6; --matte-surface: #f2dbd3; --matte-subtle: #ebd0c5; --matte-border: #d9b6a7; --matte-text: #381c11; --matte-text-muted: #613a29; --matte-primary: #a6593a; --matte-primary-hover: #824329; --matte-primary-light: #ebcebf; --matte-hero: #ebcebf;`;
      } else {
        // Monochrome (White) - THE ONLY PLACE WHITE IS USED
        vars = `--matte-bg: #f9fafb; --matte-surface: #ffffff; --matte-subtle: #f3f4f6; --matte-border: #e5e7eb; --matte-text: #111827; --matte-text-muted: #6b7280; --matte-primary: #374151; --matte-primary-hover: #1f2937; --matte-primary-light: #e5e7eb; --matte-hero: #f3f4f6;`;
      }
    } else {
      // Dark Mode Deep Shades
      if (accentColor === 'green') {
        vars = `--matte-bg: #1b241e; --matte-surface: #232e27; --matte-subtle: #2c3b31; --matte-border: #3d5244; --matte-text: #e3ede6; --matte-text-muted: #89a392; --matte-primary: #437053; --matte-primary-hover: #568a68; --matte-primary-light: #233b2b; --matte-hero: #141c17;`;
      } else if (accentColor === 'blue') {
        vars = `--matte-bg: #171c24; --matte-surface: #1f2630; --matte-subtle: #28313d; --matte-border: #384657; --matte-text: #e1e8f0; --matte-text-muted: #8496a8; --matte-primary: #4d73a1; --matte-primary-hover: #638ac2; --matte-primary-light: #25364d; --matte-hero: #11151c;`;
      } else if (accentColor === 'purple') {
        vars = `--matte-bg: #211826; --matte-surface: #291e30; --matte-subtle: #35283d; --matte-border: #4b3757; --matte-text: #ebdff2; --matte-text-muted: #a18eb0; --matte-primary: #7f5b9c; --matte-primary-hover: #9b72bd; --matte-primary-light: #3e2b4d; --matte-hero: #17111c;`;
      } else if (accentColor === 'orange') {
        vars = `--matte-bg: #2b1b15; --matte-surface: #362119; --matte-subtle: #452a20; --matte-border: #5c382b; --matte-text: #f5e4df; --matte-text-muted: #ab8f85; --matte-primary: #a85c3f; --matte-primary-hover: #c46d4b; --matte-primary-light: #4f2b1d; --matte-hero: #1f130f;`;
      } else {
        // Monochrome Dark
        vars = `--matte-bg: #111827; --matte-surface: #1f2937; --matte-subtle: #374151; --matte-border: #4b5563; --matte-text: #f9fafb; --matte-text-muted: #9ca3af; --matte-primary: #d1d5db; --matte-primary-hover: #ffffff; --matte-primary-light: #374151; --matte-hero: #030712;`;
      }
    }
    
    let css = `
      :root {
        ${vars}
      }
      
      /* Pure Eradication of Hardcoded Backgrounds */
      body, #root, .min-h-screen, .h-screen { 
        background-color: var(--matte-bg) !important; 
        color: var(--matte-text) !important; 
      }
      
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
      .border-gray-100, .border-gray-200, .border-gray-300, .dark\\\\:border-gray-700, .dark\\\\:border-gray-800, .border-b, .border-t, .border-r, .border-l, .border { 
        border-color: var(--matte-border) !important; 
      }
      
      /* Texts */
      .text-gray-900, .text-gray-800, .text-black, .dark\\\\:text-white, .dark\\\\:text-gray-100 { color: var(--matte-text) !important; }
      .text-gray-700, .text-gray-600, .text-gray-500, .text-gray-400, .dark\\\\:text-gray-300, .dark\\\\:text-gray-400 { color: var(--matte-text-muted) !important; }
      
      /* Map ALL Primary UI Buttons/Highlights */
      .bg-blue-600, .bg-blue-500, .btn-primary, .bg-purple-500, .bg-purple-600, .bg-emerald-600, .bg-indigo-600, .bg-teal-600 { 
        background-color: var(--matte-primary) !important; 
        border-color: var(--matte-primary) !important; 
        color: ${(accentColor === 'white' && theme === 'light') ? '#ffffff' : '#ffffff'} !important; 
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
        background-color: var(--matte-surface) !important; 
        border-color: var(--matte-border) !important; 
        color: var(--matte-text) !important; 
      }
      ::placeholder { color: var(--matte-text-muted) !important; opacity: 0.7; }
      
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
