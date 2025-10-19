import { useEffect, useRef } from 'react';

const CustomCursor = () => {
  const cursorRef = useRef(null);
  const cursorGlowRef = useRef(null);

  useEffect(() => {
    const cursor = cursorRef.current;
    const cursorGlow = cursorGlowRef.current;
    
    if (!cursor || !cursorGlow) return;

    let mouseX = 0;
    let mouseY = 0;
    let cursorX = 0;
    let cursorY = 0;
    let glowX = 0;
    let glowY = 0;

    const handleMouseMove = (e) => {
      mouseX = e.clientX;
      mouseY = e.clientY;
    };

    const handleMouseEnter = (e) => {
      if (e.target.tagName === 'A' || e.target.tagName === 'BUTTON') {
        cursor.style.transform = 'translate(-50%, -50%) scale(2)';
        cursor.style.borderColor = '#6366f1';
      }
    };

    const handleMouseLeave = () => {
      cursor.style.transform = 'translate(-50%, -50%) scale(1)';
      cursor.style.borderColor = '#fff';
    };

    window.addEventListener('mousemove', handleMouseMove);
    document.querySelectorAll('a, button').forEach((el) => {
      el.addEventListener('mouseenter', handleMouseEnter);
      el.addEventListener('mouseleave', handleMouseLeave);
    });

    const animate = () => {
      // Smooth cursor follow
      cursorX += (mouseX - cursorX) * 0.2;
      cursorY += (mouseY - cursorY) * 0.2;
      glowX += (mouseX - glowX) * 0.1;
      glowY += (mouseY - glowY) * 0.1;

      cursor.style.left = `${cursorX}px`;
      cursor.style.top = `${cursorY}px`;
      cursorGlow.style.left = `${glowX}px`;
      cursorGlow.style.top = `${glowY}px`;

      requestAnimationFrame(animate);
    };

    animate();

    return () => {
      window.removeEventListener('mousemove', handleMouseMove);
    };
  }, []);

  return (
    <>
      <div
        ref={cursorGlowRef}
        className="hidden lg:block fixed w-8 h-8 pointer-events-none z-50 mix-blend-screen"
        style={{
          background: 'radial-gradient(circle, rgba(99, 102, 241, 0.4) 0%, transparent 70%)',
        }}
      />
      <div
        ref={cursorRef}
        className="hidden lg:block fixed w-4 h-4 border-2 border-white rounded-full pointer-events-none z-50 transition-transform duration-200"
        style={{ transform: 'translate(-50%, -50%)' }}
      />
    </>
  );
};

export default CustomCursor;
