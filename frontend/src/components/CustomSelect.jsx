import { useState, useRef, useEffect } from 'react';
import { ChevronDown, Check } from 'lucide-react';

export default function CustomSelect({ value, onChange, options, className = '', direction = 'down', size = 'default' }) {
  const [isOpen, setIsOpen] = useState(false);
  const containerRef = useRef(null);

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (containerRef.current && !containerRef.current.contains(event.target)) {
        setIsOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const selectedOption = options.find(opt => opt.value === value) || options[0];
  const positionClass = direction === 'up' ? 'bottom-full mb-1' : 'top-full mt-1';

  return (
    <div className={`relative ${className}`} ref={containerRef}>
      <div
        onClick={() => setIsOpen(!isOpen)}
        className={`flex items-center justify-between w-full ${size === 'small' ? 'px-3 py-2 text-xs' : 'p-3 text-sm'} bg-white dark:bg-gray-800 dark:bg-gray-800 border border-gray-200 dark:border-gray-600 dark:border-gray-700 rounded-lg cursor-pointer hover:border-blue-400 focus:ring-2 focus:ring-blue-500 outline-none transition-colors`}
      >
        <div className={`flex items-center gap-2 overflow-hidden ${size === 'small' ? '' : 'text-sm md:text-base'}`}>
          {selectedOption?.icon && <span className="shrink-0">{selectedOption.icon}</span>}
          <span className="text-gray-700 dark:text-gray-300 dark:text-gray-200 truncate">{selectedOption?.label}</span>
        </div>
        <ChevronDown size={16} className={`text-gray-400 transition-transform shrink-0 ml-2 ${isOpen ? (direction === 'up' ? 'rotate-0' : 'rotate-180') : (direction === 'up' ? 'rotate-180' : 'rotate-0')}`} />
      </div>

      {isOpen && (
        <div className={`absolute z-50 w-full bg-white dark:bg-gray-800 dark:bg-gray-800 border border-gray-100 dark:border-gray-700 dark:border-gray-700 rounded-lg shadow-xl overflow-hidden py-1 max-h-60 overflow-y-auto ${positionClass}`}>
          {options.map((option) => (
            <div
              key={option.value}
              onClick={() => {
                onChange({ target: { value: option.value } });
                setIsOpen(false);
              }}
              className={`flex items-center justify-between px-4 py-2.5 cursor-pointer hover:bg-blue-50 dark:hover:bg-blue-900/30 transition-colors text-sm md:text-base ${
                value === option.value ? 'bg-blue-50 dark:bg-blue-900/40 text-blue-700 dark:text-blue-400 font-medium' : 'text-gray-600 dark:text-gray-400 dark:text-gray-300'
              }`}
            >
              <div className="flex items-center gap-2 overflow-hidden">
                {option.icon && <span className="shrink-0">{option.icon}</span>}
                <span className="truncate">{option.label}</span>
              </div>
              {value === option.value && <Check size={16} className="text-blue-600 dark:text-blue-400 shrink-0 ml-2" />}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
