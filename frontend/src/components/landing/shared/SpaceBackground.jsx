import { useEffect, useRef } from 'react';

const SpaceBackground = () => {
  const canvasRef = useRef(null);
  const mouseRef = useRef({ x: 0, y: 0 });
  const starsRef = useRef([]);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    let animationFrameId;

    const setCanvasSize = () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    };

    setCanvasSize();
    window.addEventListener('resize', setCanvasSize);

    // Initialize stars
    const initStars = () => {
      const starCount = 200;
      starsRef.current = [];

      for (let i = 0; i < starCount; i++) {
        starsRef.current.push({
          x: Math.random() * canvas.width,
          y: Math.random() * canvas.height,
          radius: Math.random() * 1.5,
          opacity: Math.random(),
          speed: Math.random() * 0.5 + 0.1,
          layer: Math.floor(Math.random() * 3), // 3 parallax layers
        });
      }
    };

    initStars();

    // Mouse tracking
    const handleMouseMove = (e) => {
      mouseRef.current = {
        x: e.clientX,
        y: e.clientY,
      };
    };

    window.addEventListener('mousemove', handleMouseMove);

    // Animation loop
    const animate = () => {
      ctx.fillStyle = 'rgba(10, 14, 39, 0.1)';
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      // Draw stars with parallax
      starsRef.current.forEach((star) => {
        ctx.beginPath();
        ctx.arc(star.x, star.y, star.radius, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(255, 255, 255, ${star.opacity})`;
        ctx.fill();

        // Parallax movement based on layer
        const parallaxSpeed = (star.layer + 1) * 0.1;
        star.y += star.speed * parallaxSpeed;

        if (star.y > canvas.height) {
          star.y = 0;
          star.x = Math.random() * canvas.width;
        }

        // Twinkle effect
        star.opacity += Math.sin(Date.now() * 0.001 + star.x) * 0.01;
        star.opacity = Math.max(0.3, Math.min(1, star.opacity));
      });

      // Mouse spotlight effect
      const gradient = ctx.createRadialGradient(
        mouseRef.current.x,
        mouseRef.current.y,
        0,
        mouseRef.current.x,
        mouseRef.current.y,
        300
      );
      gradient.addColorStop(0, 'rgba(99, 102, 241, 0.15)');
      gradient.addColorStop(0.5, 'rgba(99, 102, 241, 0.05)');
      gradient.addColorStop(1, 'rgba(99, 102, 241, 0)');

      ctx.fillStyle = gradient;
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      animationFrameId = requestAnimationFrame(animate);
    };

    animate();

    return () => {
      window.removeEventListener('resize', setCanvasSize);
      window.removeEventListener('mousemove', handleMouseMove);
      cancelAnimationFrame(animationFrameId);
    };
  }, []);

  return (
    <canvas
      ref={canvasRef}
      className="fixed top-0 left-0 w-full h-full pointer-events-none z-0"
      style={{ background: 'linear-gradient(135deg, #0a0e27 0%, #1a1f3a 100%)' }}
    />
  );
};

export default SpaceBackground;
