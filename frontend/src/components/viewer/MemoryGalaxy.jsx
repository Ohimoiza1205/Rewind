import { useRef, useEffect, useState } from 'react';
import { Canvas, useFrame, useThree } from '@react-three/fiber';
import { OrbitControls, Sphere, Trail, Text, Html } from '@react-three/drei';
import * as THREE from 'three';
import { useNavigate, useParams } from 'react-router-dom';

// Glowing Memory Orb Component
const MemoryOrb = ({ position, sceneData, onClick, isActive, index }) => {
  const meshRef = useRef();
  const [hovered, setHovered] = useState(false);

  useFrame((state) => {
    if (meshRef.current) {
      // Gentle floating animation
      meshRef.current.position.y = position[1] + Math.sin(state.clock.elapsedTime + index) * 0.2;
      
      // Pulsing glow
      const scale = hovered || isActive ? 1.3 : 1 + Math.sin(state.clock.elapsedTime * 2) * 0.1;
      meshRef.current.scale.setScalar(scale);
      
      // Rotation
      meshRef.current.rotation.y += 0.01;
    }
  });

  return (
    <group position={position}>
      {/* Outer glow */}
      <Sphere ref={meshRef} args={[0.5, 32, 32]}>
        <meshStandardMaterial
          color={hovered ? "#00d4ff" : isActive ? "#a855f7" : "#6366f1"}
          emissive={hovered ? "#00d4ff" : isActive ? "#a855f7" : "#6366f1"}
          emissiveIntensity={hovered ? 2 : isActive ? 1.5 : 0.8}
          transparent
          opacity={0.9}
          metalness={0.8}
          roughness={0.2}
        />
      </Sphere>

      {/* Inner core */}
      <Sphere args={[0.3, 16, 16]}>
        <meshStandardMaterial
          color="#ffffff"
          emissive="#ffffff"
          emissiveIntensity={3}
        />
      </Sphere>

      {/* Interaction mesh */}
      <mesh
        position={[0, 0, 0]}
        onClick={onClick}
        onPointerOver={() => setHovered(true)}
        onPointerOut={() => setHovered(false)}
      >
        <sphereGeometry args={[0.7, 32, 32]} />
        <meshBasicMaterial transparent opacity={0} />
      </mesh>

      {/* Label when hovered */}
      {hovered && (
        <Html distanceFactor={10}>
          <div className="bg-black/80 backdrop-blur-sm px-4 py-2 rounded-lg border border-cyan-500/50 pointer-events-none whitespace-nowrap">
            <p className="text-cyan-400 text-sm font-semibold">Scene {index + 1}</p>
            <p className="text-white text-xs">{sceneData?.description || 'Memory moment'}</p>
          </div>
        </Html>
      )}
    </group>
  );
};

// Connection Lines Between Orbs
const ConnectionLine = ({ start, end }) => {
  const points = [];
  const steps = 20;
  
  for (let i = 0; i <= steps; i++) {
    const t = i / steps;
    const x = start[0] + (end[0] - start[0]) * t;
    const y = start[1] + (end[1] - start[1]) * t;
    const z = start[2] + (end[2] - start[2]) * t;
    points.push(new THREE.Vector3(x, y, z));
  }

  const curve = new THREE.CatmullRomCurve3(points);
  const linePoints = curve.getPoints(50);

  return (
    <line>
      <bufferGeometry>
        <bufferAttribute
          attach="attributes-position"
          count={linePoints.length}
          array={new Float32Array(linePoints.flatMap(p => [p.x, p.y, p.z]))}
          itemSize={3}
        />
      </bufferGeometry>
      <lineBasicMaterial color="#6366f1" opacity={0.3} transparent linewidth={2} />
    </line>
  );
};

// Particle Starfield
const Starfield = () => {
  const pointsRef = useRef();
  
  const particlesCount = 2000;
  const positions = new Float32Array(particlesCount * 3);
  const colors = new Float32Array(particlesCount * 3);
  
  for (let i = 0; i < particlesCount; i++) {
    positions[i * 3] = (Math.random() - 0.5) * 50;
    positions[i * 3 + 1] = (Math.random() - 0.5) * 50;
    positions[i * 3 + 2] = (Math.random() - 0.5) * 50;
    
    const color = new THREE.Color();
    color.setHSL(Math.random() * 0.2 + 0.6, 0.5, Math.random() * 0.5 + 0.5);
    colors[i * 3] = color.r;
    colors[i * 3 + 1] = color.g;
    colors[i * 3 + 2] = color.b;
  }

  useFrame((state) => {
    if (pointsRef.current) {
      pointsRef.current.rotation.y = state.clock.elapsedTime * 0.02;
    }
  });

  return (
    <points ref={pointsRef}>
      <bufferGeometry>
        <bufferAttribute
          attach="attributes-position"
          count={particlesCount}
          array={positions}
          itemSize={3}
        />
        <bufferAttribute
          attach="attributes-color"
          count={particlesCount}
          array={colors}
          itemSize={3}
        />
      </bufferGeometry>
      <pointsMaterial size={0.1} vertexColors transparent opacity={0.8} />
    </points>
  );
};

// Nebula Background
const NebulaBackground = () => {
  const meshRef = useRef();

  useFrame((state) => {
    if (meshRef.current) {
      meshRef.current.rotation.z = state.clock.elapsedTime * 0.01;
    }
  });

  return (
    <mesh ref={meshRef} position={[0, 0, -20]}>
      <planeGeometry args={[100, 100]} />
      <meshBasicMaterial>
        <primitive
          attach="map"
          object={(() => {
            const canvas = document.createElement('canvas');
            canvas.width = 512;
            canvas.height = 512;
            const ctx = canvas.getContext('2d');
            
            // Create nebula gradient
            const gradient = ctx.createRadialGradient(256, 256, 0, 256, 256, 256);
            gradient.addColorStop(0, 'rgba(99, 102, 241, 0.3)');
            gradient.addColorStop(0.4, 'rgba(139, 92, 246, 0.2)');
            gradient.addColorStop(0.7, 'rgba(6, 182, 212, 0.1)');
            gradient.addColorStop(1, 'rgba(10, 14, 39, 0)');
            
            ctx.fillStyle = gradient;
            ctx.fillRect(0, 0, 512, 512);
            
            return new THREE.CanvasTexture(canvas);
          })()}
        />
      </meshBasicMaterial>
    </mesh>
  );
};

// Main Memory Galaxy Scene
const MemoryGalaxyScene = ({ scenes, onSceneClick, activeScene }) => {
  // Arrange orbs in a spiral constellation pattern
  const positions = scenes.map((_, index) => {
    const angle = (index / scenes.length) * Math.PI * 4;
    const radius = 3 + index * 0.8;
    return [
      Math.cos(angle) * radius,
      Math.sin(index * 0.5) * 2,
      Math.sin(angle) * radius
    ];
  });

  return (
    <>
      <NebulaBackground />
      <Starfield />
      
      {/* Ambient lighting */}
      <ambientLight intensity={0.3} />
      <pointLight position={[10, 10, 10]} intensity={1} color="#6366f1" />
      <pointLight position={[-10, -10, -10]} intensity={0.5} color="#06b6d4" />
      
      {/* Memory orbs */}
      {scenes.map((scene, index) => (
        <MemoryOrb
          key={index}
          position={positions[index]}
          sceneData={scene}
          onClick={() => onSceneClick(index)}
          isActive={activeScene === index}
          index={index}
        />
      ))}
      
      {/* Connection lines */}
      {positions.map((pos, index) => {
        if (index < positions.length - 1) {
          return (
            <ConnectionLine
              key={`line-${index}`}
              start={pos}
              end={positions[index + 1]}
            />
          );
        }
        return null;
      })}
      
      <OrbitControls
        enableZoom={true}
        enablePan={true}
        minDistance={5}
        maxDistance={30}
        autoRotate={true}
        autoRotateSpeed={0.5}
      />
    </>
  );
};

// Main Component
const MemoryGalaxy = () => {
  const { videoId } = useParams();
  const navigate = useNavigate();
  const [scenes, setScenes] = useState([]);
  const [activeScene, setActiveScene] = useState(null);
  const [loading, setLoading] = useState(true);
  const [metadata, setMetadata] = useState(null);

  const API_BASE = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000';

  useEffect(() => {
    const loadMemoryData = async () => {
      try {
        // Load metadata
        const metaResponse = await fetch(`${API_BASE}/api/pointcloud/metadata/${videoId}`);
        const metaData = await metaResponse.json();
        
        if (metaData.success) {
          setMetadata(metaData.metadata);
          
          // Create scene objects for each frame
          const sceneList = Array.from({ length: metaData.metadata.total_frames }, (_, i) => ({
            frameNumber: i,
            description: `Memory moment ${i + 1}`,
            timestamp: i * 0.5
          }));
          
          setScenes(sceneList);
        }
        
        setLoading(false);
      } catch (err) {
        console.error('Failed to load memory data:', err);
        setLoading(false);
      }
    };

    if (videoId) {
      loadMemoryData();
    }
  }, [videoId]);

  const handleSceneClick = (sceneIndex) => {
    setActiveScene(sceneIndex);
    // Navigate to detailed 3D view
    navigate(`/viewer/${videoId}/scene/${sceneIndex}`);
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-deep-space flex items-center justify-center">
        <div className="text-center">
          <div className="w-20 h-20 border-4 border-cosmic-purple border-t-transparent rounded-full animate-spin mx-auto mb-4" />
          <p className="text-space-gray animate-pulse">Loading memory galaxy...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="relative min-h-screen bg-deep-space">
      {/* Header */}
      <div className="absolute top-0 left-0 right-0 z-10 border-b border-white/10 backdrop-blur-sm">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <h1 className="text-2xl font-space font-bold text-gradient">
            Memory Galaxy
          </h1>
          <button
            onClick={() => navigate('/dashboard')}
            className="glassmorphic px-4 py-2 rounded-lg text-sm hover:border-cosmic-purple transition-colors"
          >
            Back to Dashboard
          </button>
        </div>
      </div>

      {/* 3D Canvas */}
      <div className="w-full h-screen">
        <Canvas camera={{ position: [0, 5, 15], fov: 60 }}>
          <color attach="background" args={['#0a0e27']} />
          <MemoryGalaxyScene
            scenes={scenes}
            onSceneClick={handleSceneClick}
            activeScene={activeScene}
          />
        </Canvas>
      </div>

      {/* Bottom UI */}
      <div className="absolute bottom-0 left-0 right-0 z-10 p-6">
        <div className="max-w-4xl mx-auto">
          <div className="glassmorphic rounded-xl p-6">
            <div className="grid grid-cols-3 gap-4 text-center">
              <div>
                <div className="text-3xl font-bold text-gradient mb-1">
                  {scenes.length}
                </div>
                <div className="text-xs text-space-gray">Memory Moments</div>
              </div>
              <div>
                <div className="text-3xl font-bold text-gradient mb-1">
                  {metadata?.points_per_frame?.toLocaleString() || '15,000'}
                </div>
                <div className="text-xs text-space-gray">3D Points per Scene</div>
              </div>
              <div>
                <div className="text-3xl font-bold text-gradient mb-1">
                  {metadata?.fps || 2} FPS
                </div>
                <div className="text-xs text-space-gray">Frame Rate</div>
              </div>
            </div>
            
            <div className="mt-4 text-center text-sm text-space-gray">
              Click any glowing orb to explore that memory moment in 3D
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default MemoryGalaxy;
