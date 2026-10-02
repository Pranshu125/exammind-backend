with open("src/contexts/ThemeContext.jsx", "r", encoding="utf-8") as f:
    content = f.read()

dynamic_style = """
  useEffect(() => {
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
    
    let css = '';
    
    // Accent Colors Override (Translating default Blue to the selected color)
    if (accentColor === 'purple') {
      css += `
        .bg-blue-600 { background-color: #9333ea !important; }
        .hover\:bg-blue-700:hover { background-color: #7e22ce !important; }
        .text-blue-600 { color: #9333ea !important; }
        .text-blue-500 { color: #a855f7 !important; }
        .border-blue-600 { border-color: #9333ea !important; }
        .border-blue-200 { border-color: #e9d5ff !important; }
        .ring-blue-500 { --tw-ring-color: #a855f7 !important; }
        .bg-blue-100 { background-color: #f3e8ff !important; }
        .bg-blue-50 { background-color: #faf5ff !important; }
        .text-blue-700 { color: #7e22ce !important; }
      `;
    } else if (accentColor === 'green') {
      css += `
        .bg-blue-600 { background-color: #16a34a !important; }
        .hover\:bg-blue-700:hover { background-color: #15803d !important; }
        .text-blue-600 { color: #16a34a !important; }
        .text-blue-500 { color: #22c55e !important; }
        .border-blue-600 { border-color: #16a34a !important; }
        .border-blue-200 { border-color: #bbf7d0 !important; }
        .ring-blue-500 { --tw-ring-color: #22c55e !important; }
        .bg-blue-100 { background-color: #dcfce7 !important; }
        .bg-blue-50 { background-color: #f0fdf4 !important; }
        .text-blue-700 { color: #15803d !important; }
      `;
    } else if (accentColor === 'orange') {
      css += `
        .bg-blue-600 { background-color: #ea580c !important; }
        .hover\:bg-blue-700:hover { background-color: #c2410c !important; }
        .text-blue-600 { color: #ea580c !important; }
        .text-blue-500 { color: #f97316 !important; }
        .border-blue-600 { border-color: #ea580c !important; }
        .border-blue-200 { border-color: #fed7aa !important; }
        .ring-blue-500 { --tw-ring-color: #f97316 !important; }
        .bg-blue-100 { background-color: #ffedd5 !important; }
        .bg-blue-50 { background-color: #fff7ed !important; }
        .text-blue-700 { color: #c2410c !important; }
      `;
    }

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

  }, [accentColor, layoutDensity]);"""

old_effect_1 = """  useEffect(() => {
    window.document.documentElement.setAttribute('data-accent', accentColor);
    localStorage.setItem('accentColor', accentColor);
  }, [accentColor]);"""

old_effect_2 = """  useEffect(() => {
    window.document.documentElement.setAttribute('data-density', layoutDensity);
    localStorage.setItem('layoutDensity', layoutDensity);
  }, [layoutDensity]);"""

content = content.replace(old_effect_1, dynamic_style).replace(old_effect_2, "")

with open("src/contexts/ThemeContext.jsx", "w", encoding="utf-8") as f:
    f.write(content)

print("done")
