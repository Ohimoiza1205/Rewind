import { useRef, useEffect, useState } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { Sphere, MeshDistortMaterial } from '@react-three/drei';

const VideoOrb = () => {
  const meshRef = useRef();
  const [hovered, setHovered] = useState(false);

  useFrame((state) => {
    if (meshRef.current) {
      meshRef.current.rotation.y += 0.002;
      meshRef.current.rotation.x = Math.sin(state.clock.elapsedTime * 0.3) * 0.1;
      
      if (hovered) {
        meshRef.current.scale.lerp({ x: 1.1, y: 1.1, z: 1.1 }, 0.1);
      } else {
        meshRef.current.scale.lerp({ x: 1, y: 1, z: 1 }, 0.1);
      }
    }
  });

  return (
    <Sphere
      ref={meshRef}
      args={[1, 64, 64]}
      onPointerOver={() => setHovered(true)}
      onPointerOut={() => setHovered(false)}
    >
      <MeshDistortMaterial
        color="#6366f1"
        attach="material"
        distort={0.4}
        speed={2}
        roughness={0.2}
        metalness={0.8}
      />
    </Sphere>
  );
};

const HeroSection = ({ onGetStarted }) => {
  const [scrollY, setScrollY] = useState(0);

  useEffect(() => {
    const handleScroll = () => {
      setScrollY(window.scrollY);
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const heroOpacity = Math.max(0, 1 - scrollY / 400);
  const heroTransform = `translateY(${scrollY * 0.5}px)`;

  return (
    <section className="relative h-screen flex items-center justify-center overflow-hidden">
      <div 
        className="absolute inset-0 z-10"
        style={{ opacity: heroOpacity, transform: heroTransform }}
      >
        <div className="section-container h-full flex flex-col items-center justify-center text-center">
          <h1 className="text-6xl md:text-7xl lg:text-8xl font-space font-bold mb-6 leading-tight animate-fade-in">
            Transform Your <span className="text-gradient">Memories</span>
            <br />
            Into Living <span className="text-gradient">Universes</span>
          </h1>

          <div className="w-full max-w-md h-64 md:h-80 my-12 animate-float">
            <Canvas camera={{ position: [0, 0, 3], fov: 50 }}>
              <ambientLight intensity={0.5} />
              <pointLight position={[10, 10, 10]} intensity={1} />
              <pointLight position={[-10, -10, -10]} intensity={0.5} color="#06b6d4" />
              <VideoOrb />
            </Canvas>
          </div>

          <p className="text-xl md:text-2xl text-space-gray mb-8 max-w-2xl animate-slide-up">
            AI-powered 3D exploration. Your voice. Any language.
          </p>

          <button 
            onClick={onGetStarted}
            className="btn-primary text-lg animate-pulse-glow"
          >
            Explore Your First Memory
          </button>

          <div className="absolute bottom-10 left-1/2 transform -translate-x-1/2 animate-bounce">
            <svg className="w-8 h-8 text-cosmic-purple" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
            </svg>
          </div>
        </div>
      </div>
    </section>
  );
};

export default HeroSection;
