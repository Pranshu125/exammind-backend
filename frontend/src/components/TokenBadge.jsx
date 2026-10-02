import { Cpu } from 'lucide-react';

export default function TokenBadge({ data }) {
  if (!data) return null;
  const tokenCount = Math.round(JSON.stringify(data).length / 3.5);
  
  return (
    <div className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-gray-50 border border-gray-200 text-xs font-mono text-gray-500 shadow-sm" title="Estimated AI Tokens Used">
      <Cpu size={14} className="text-gray-400" />
      <span>{tokenCount.toLocaleString()} Tokens</span>
    </div>
  );
}