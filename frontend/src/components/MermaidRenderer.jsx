import React, { useEffect, useState } from 'react';
import mermaid from 'mermaid';

mermaid.initialize({
  startOnLoad: true,
  theme: 'base',
  securityLevel: 'loose',
  themeVariables: {
    primaryColor: '#e0e7ff',
    primaryTextColor: '#1e1b4b',
    primaryBorderColor: '#6366f1',
    lineColor: '#6366f1',
    secondaryColor: '#fef08a',
    tertiaryColor: '#fff'
  }
});

export default function MermaidRenderer({ chart }) {
  const [svg, setSvg] = useState('');

  useEffect(() => {
    if (chart) {
      try {
        mermaid.render(`mermaid-${Math.random().toString(36).substr(2, 9)}`, chart)
          .then(res => setSvg(res.svg))
          .catch(err => {
            console.error('Mermaid render error:', err);
            setSvg(`<div class="text-red-500 p-4 border border-red-200 bg-red-50 rounded-lg">Failed to render diagram</div>`);
          });
      } catch (e) {
        console.error(e);
      }
    }
  }, [chart]);

  return (
    <div 
      className="my-6 flex justify-center bg-gray-50 dark:bg-gray-900 rounded-xl p-4 overflow-x-auto border border-gray-100 dark:border-gray-700" 
      dangerouslySetInnerHTML={{ __html: svg }} 
    />
  );
}
