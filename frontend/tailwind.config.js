/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'deep-space': '#0a0e27',
        'space-dark': '#1a1f3a',
        'cosmic-purple': '#6366f1',
        'nebula-blue': '#3b82f6',
        'starlight': '#ffffff',
        'accent-cyan': '#06b6d4',
        'space-gray': '#9ca3af',
      },
      fontFamily: {
        'space': ['Space Grotesk', 'sans-serif'],
        'inter': ['Inter', 'sans-serif'],
        'orbitron': ['Orbitron', 'monospace'],
      },
      animation: {
        'float': 'float 6s ease-in-out infinite',
        'pulse-glow': 'pulse-glow 2s ease-in-out infinite',
        'rotate-slow': 'rotate 20s linear infinite',
        'fade-in': 'fadeIn 1s ease-in forwards',
        'slide-up': 'slideUp 0.8s ease-out forwards',
      },
      keyframes: {
        float: {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-20px)' },
        },
        'pulse-glow': {
          '0%, 100%': { boxShadow: '0 0 20px rgba(99, 102, 241, 0.4)' },
          '50%': { boxShadow: '0 0 40px rgba(99, 102, 241, 0.8)' },
        },
        rotate: {
          '0%': { transform: 'rotate(0deg)' },
          '100%': { transform: 'rotate(360deg)' },
        },
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { transform: 'translateY(30px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
      },
      backgroundImage: {
        'cosmic-gradient': 'linear-gradient(135deg, #0a0e27 0%, #1a1f3a 100%)',
        'button-gradient': 'linear-gradient(135deg, #6366f1 0%, #3b82f6 100%)',
        'wormhole': 'radial-gradient(circle, #6366f1 0%, #3b82f6 50%, #06b6d4 100%)',
      },
      backdropBlur: {
        'glass': '20px',
      },
    },
  },
  plugins: [],
}
