import { useState, useRef } from 'react';

export default function DraggableNode({ id, x, y, z, title, scale, onDrag, bringToFront, children }) {
  const [isDragging, setIsDragging] = useState(false);
  const nodeRef = useRef(null);

  const handlePointerDown = (e) => {
    if (e.target.closest('button, input, textarea, select, .no-drag')) return;
    
    e.stopPropagation();
    setIsDragging(true);
    bringToFront(id);
    if (nodeRef.current) nodeRef.current.setPointerCapture(e.pointerId);
  };

  const handlePointerMove = (e) => {
    if (!isDragging) return;
    e.stopPropagation();
    // adjust for the canvas scale so cursor stays attached to node
    onDrag(id, e.movementX / scale, e.movementY / scale);
  };

  const handlePointerUp = (e) => {
    e.stopPropagation();
    setIsDragging(false);
    if (nodeRef.current) nodeRef.current.releasePointerCapture(e.pointerId);
  };

  return (
    <div
      ref={nodeRef}
      onPointerDown={handlePointerDown}
      onPointerMove={handlePointerMove}
      onPointerUp={handlePointerUp}
      onPointerCancel={handlePointerUp}
      style={{
        transform: `translate(${x}px, ${y}px)`,
        zIndex: z,
      }}
      className={`absolute top-0 left-0 flex flex-col shadow-2xl rounded-3xl bg-slate-900/80 backdrop-blur-xl border border-white/10 overflow-hidden transition-shadow ${isDragging ? 'cursor-grabbing shadow-cyan-500/20 shadow-2xl ring-2 ring-cyan-500/50' : 'cursor-grab'}`}
    >
      <div className="bg-white/5 px-4 py-2 border-b border-white/10 flex items-center justify-between pointer-events-none">
        <span className="text-xs font-bold tracking-widest text-cyan-400 uppercase">{title}</span>
        <div className="flex gap-1.5">
          <div className="w-3 h-3 rounded-full bg-slate-600"></div>
          <div className="w-3 h-3 rounded-full bg-slate-600"></div>
          <div className="w-3 h-3 rounded-full bg-slate-600"></div>
        </div>
      </div>
      <div className="cursor-auto no-drag max-h-[70vh] overflow-y-auto custom-scrollbar">
        {children}
      </div>
    </div>
  );
}
