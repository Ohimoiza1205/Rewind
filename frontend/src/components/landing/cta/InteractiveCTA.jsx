import { useState } from 'react';

const InteractiveCTA = ({ type = 'primary', onClick, children }) => {
  const [ripples, setRipples] = useState([]);

  const handleClick = (e) => {
    const rect = e.currentTarget.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    const newRipple = {
      x,
      y,
      id: Date.now(),
    };

    setRipples([...ripples, newRipple]);
    setTimeout(() => {
      setRipples((prev) => prev.filter((r) => r.id !== newRipple.id));
    }, 600);

    if (onClick) onClick(e);
  };

  const isPrimary = type === 'primary';

  return (
    <button
      onClick={handleClick}
      className={`
        relative overflow-hidden group
        px-8 py-4 rounded-lg font-semibold text-lg
        transition-all duration-300 transform
        ${isPrimary 
          ? 'bg-button-gradient text-white hover:scale-105 hover:shadow-2xl' 
          : 'glassmorphic text-white border-2 border-white/20 hover:border-cosmic-purple hover:scale-105'
        }
      `}
      style={{
        boxShadow: isPrimary 
          ? '0 0 30px rgba(99, 102, 241, 0.4)' 
          : '0 8px 32px rgba(0, 0, 0, 0.3)',
      }}
    >
      {/* Ripple effect */}
      {ripples.map((ripple) => (
        <span
          key={ripple.id}
          className="absolute rounded-full bg-white/30 animate-ping"
          style={{
            left: ripple.x,
            top: ripple.y,
            width: '20px',
            height: '20px',
            transform: 'translate(-50%, -50%)',
          }}
        />
      ))}

      {/* Hover glow */}
      <span className="absolute inset-0 bg-gradient-to-r from-transparent via-white/10 to-transparent translate-x-[-100%] group-hover:translate-x-[100%] transition-transform duration-1000" />

      {/* Content */}
      <span className="relative flex items-center gap-2">
        {children}
      </span>
    </button>
  );
};

export default InteractiveCTA;
