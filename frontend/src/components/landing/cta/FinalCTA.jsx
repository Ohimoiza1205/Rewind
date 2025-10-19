import { useEffect, useRef, useState } from 'react';

const FinalCTA = ({ onGetStarted }) => {
  const canvasRef = useRef(null);
  const [showDemo, setShowDemo] = useState(false);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    let rotation = 0;
    const particles = [];

    for (let i = 0; i < 100; i++) {
      particles.push({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        speed: Math.random() * 2 + 1,
        size: Math.random() * 2,
      });
    }

    const animate = () => {
      ctx.fillStyle = 'rgba(10, 14, 39, 0.1)';
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      const centerX = canvas.width / 2;
      const centerY = canvas.height / 2;

      for (let i = 0; i < 8; i++) {
        const radius = 200 + i * 50;

        ctx.beginPath();
        ctx.arc(centerX, centerY, radius, 0, Math.PI * 2);
        ctx.strokeStyle = `rgba(99, 102, 241, ${0.1 - i * 0.01})`;
        ctx.lineWidth = 2;
        ctx.stroke();
      }

      particles.forEach((particle) => {
        const dx = centerX - particle.x;
        const dy = centerY - particle.y;
        const distance = Math.sqrt(dx * dx + dy * dy);

        particle.x += (dx / distance) * particle.speed;
        particle.y += (dy / distance) * particle.speed;

        ctx.beginPath();
        ctx.arc(particle.x, particle.y, particle.size, 0, Math.PI * 2);
        ctx.fillStyle = 'rgba(99, 102, 241, 0.6)';
        ctx.fill();

        if (distance < 50) {
          particle.x = Math.random() * canvas.width;
          particle.y = Math.random() * canvas.height;
        }
      });

      rotation += 0.005;
      requestAnimationFrame(animate);
    };

    animate();

    const handleResize = () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    };

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  return (
    <section className="relative min-h-screen flex items-center justify-center overflow-hidden">
      <canvas
        ref={canvasRef}
        className="absolute inset-0"
        style={{ background: 'linear-gradient(135deg, #0a0e27 0%, #1a1f3a 100%)' }}
      />

      <div className="relative z-10 text-center section-container">
        <h2 className="text-6xl md:text-7xl font-space font-bold mb-6 animate-fade-in">
          Step Into Your <span className="text-gradient">Memories</span>
        </h2>

        <p className="text-2xl text-space-gray mb-12 animate-slide-up">
          Transform your videos in minutes. No installation required.
        </p>

        <div className="flex flex-col sm:flex-row gap-6 justify-center items-center">
          <button 
            onClick={onGetStarted}
            className="btn-primary text-xl px-12 py-6 animate-pulse-glow"
          >
            Get Started Free
          </button>

          <button 
            onClick={() => setShowDemo(true)}
            className="glassmorphic px-8 py-4 rounded-lg font-semibold hover:scale-105 transition-transform duration-300 flex items-center gap-2"
          >
            <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
              <path d="M6.3 2.841A1.5 1.5 0 004 4.11V15.89a1.5 1.5 0 002.3 1.269l9.344-5.89a1.5 1.5 0 000-2.538L6.3 2.84z" />
            </svg>
            Watch 2-Minute Demo
          </button>
        </div>

        <p className="text-space-gray mt-8 text-sm">
          Join 1,000+ users transforming their video memories
        </p>
      </div>

      {showDemo && (
        <div 
          className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm"
          onClick={() => setShowDemo(false)}
        >
          <div 
            className="glassmorphic rounded-2xl p-8 max-w-4xl w-full mx-4"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-2xl font-space font-bold">Demo Video</h3>
              <button 
                onClick={() => setShowDemo(false)}
                className="text-space-gray hover:text-white transition-colors"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
            
            <div className="aspect-video bg-deep-space rounded-lg flex items-center justify-center">
              <p className="text-space-gray">Demo video coming soon - Record your screen!</p>
            </div>
          </div>
        </div>
      )}
    </section>
  );
};

export default FinalCTA;
