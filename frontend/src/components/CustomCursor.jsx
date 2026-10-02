import { useEffect, useRef } from 'react';

export default function CustomCursor() {
  const cursorRef = useRef(null);
  const auraRef = useRef(null);

  useEffect(() => {
    let mouseX = 0;
    let mouseY = 0;
    let auraX = 0;
    let auraY = 0;

    const moveCursor = (e) => {
      mouseX = e.clientX;
      mouseY = e.clientY;
      
      if (cursorRef.current) {
        cursorRef.current.style.transform = `translate3d(${mouseX}px, ${mouseY}px, 0)`;
      }
    };

    // Smooth lerp for the aura
    const render = () => {
      auraX += (mouseX - auraX) * 0.15;
      auraY += (mouseY - auraY) * 0.15;
      
      if (auraRef.current) {
        auraRef.current.style.transform = `translate3d(${auraX}px, ${auraY}px, 0)`;
      }
      requestAnimationFrame(render);
    };

    window.addEventListener('mousemove', moveCursor);
    const animId = requestAnimationFrame(render);

    return () => {
      window.removeEventListener('mousemove', moveCursor);
      cancelAnimationFrame(animId);
    };
  }, []);

  return (
    <>
      {/* Core Dot */}
      <div 
        ref={cursorRef} 
        className="fixed top-0 left-0 w-2 h-2 bg-cyan-400 rounded-full pointer-events-none z-[9999] mix-blend-screen shadow-[0_0_10px_#00f0ff] -ml-1 -mt-1 hidden lg:block" 
      />
      {/* Trailing Aura */}
      <div 
        ref={auraRef} 
        className="fixed top-0 left-0 w-10 h-10 border border-cyan-500/50 bg-cyan-500/10 rounded-full pointer-events-none z-[9998] backdrop-blur-[1px] -ml-5 -mt-5 hidden lg:block" 
      />
    </>
  );
}
