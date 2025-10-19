import { useRef, useEffect, useState } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, Html } from '@react-three/drei';
import { useNavigate, useParams } from 'react-router-dom';
import * as THREE from 'three';

// Point Cloud Renderer for the Scene
const ScenePointCloud = ({ points }) => {
  const pointsRef = useRef();
  const [geometry, setGeometry] = useState(null);

  useEffect(() => {
    if (!points || points.length === 0) return;

    const positions = new Float32Array(points.length * 3);
    const colors = new Float32Array(points.length * 3);

    points.forEach((point, i) => {
      positions[i * 3] = point.x;
      positions[i * 3 + 1] = point.y;
      positions[i * 3 + 2] = point.z;
      
      colors[i * 3] = point.r / 255;
      colors[i * 3 + 1] = point.g / 255;
      colors[i * 3 + 2] = point.b / 255;
    });

    const geo = new THREE.BufferGeometry();
    geo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    geo.setAttribute('color', new THREE.BufferAttribute(colors, 3));
    
    setGeometry(geo);
  }, [points]);

  useFrame(() => {
    if (pointsRef.current) {
      pointsRef.current.rotation.y += 0.001;
    }
  });

  if (!geometry) return null;

  return (
    <points ref={pointsRef}>
      <bufferGeometry attach="geometry" {...geometry} />
      <pointsMaterial
        size={0.02}
        vertexColors
        sizeAttenuation
        transparent
        opacity={0.95}
      />
    </points>
  );
};

// Portal Ring Effect
const PortalRing = () => {
  const ringRef = useRef();

  useFrame((state) => {
    if (ringRef.current) {
      ringRef.current.rotation.z = state.clock.elapsedTime * 0.5;
    }
  });

  return (
    <group>
      <mesh ref={ringRef}>
        <torusGeometry args={[3, 0.05, 16, 100]} />
        <meshStandardMaterial
          color="#6366f1"
          emissive="#6366f1"
          emissiveIntensity={2}
          transparent
          opacity={0.7}
        />
      </mesh>
      <mesh rotation={[0, 0, Math.PI / 4]}>
        <torusGeometry args={[3.2, 0.03, 16, 100]} />
        <meshStandardMaterial
          color="#06b6d4"
          emissive="#06b6d4"
          emissiveIntensity={1.5}
          transparent
          opacity={0.5}
        />
      </mesh>
    </group>
  );
};

// Main Scene Portal Component
const ScenePortal = () => {
  const { videoId, sceneIndex } = useParams();
  const navigate = useNavigate();
  const [pointCloudData, setPointCloudData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [narration, setNarration] = useState(null);
  const [isPlaying, setIsPlaying] = useState(false);

  const API_BASE = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000';

  useEffect(() => {
    const loadScene = async () => {
      try {
        const response = await fetch(
          `${API_BASE}/api/pointcloud/frame/${videoId}/${sceneIndex}`
        );
        const data = await response.json();
        setPointCloudData(data);
        setLoading(false);
      } catch (err) {
        console.error('Failed to load scene:', err);
        setLoading(false);
      }
    };

    if (videoId && sceneIndex !== undefined) {
      loadScene();
    }
  }, [videoId, sceneIndex]);

  const handlePlayNarration = () => {
    setIsPlaying(true);
    // Simulate narration
    setNarration({
      text: "This is a beautiful moment from your memory, captured in three dimensions. You can explore every angle of this frozen moment in time.",
      language: "en"
    });
    
    setTimeout(() => {
      setIsPlaying(false);
    }, 5000);
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-deep-space flex items-center justify-center">
        <div className="text-center">
          <div className="relative w-32 h-32 mx-auto mb-6">
            <div className="absolute inset-0 border-4 border-cosmic-purple border-t-transparent rounded-full animate-spin" />
            <div className="absolute inset-2 border-4 border-cyan-400 border-t-transparent rounded-full animate-spin animation-delay-150" 
                 style={{ animationDirection: 'reverse' }} />
          </div>
          <p className="text-xl text-space-gray animate-pulse">Opening memory portal...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="relative min-h-screen bg-deep-space">
      {/* Header */}
      <div className="absolute top-0 left-0 right-0 z-10 border-b border-white/10 backdrop-blur-sm">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <div>
            <button
              onClick={() => navigate(`/viewer/${videoId}`)}
              className="flex items-center gap-2 text-space-gray hover:text-white transition-colors"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
              </svg>
              Back to Galaxy
            </button>
            <h1 className="text-xl font-space font-bold text-gradient mt-2">
              Memory Scene {parseInt(sceneIndex) + 1}
            </h1>
          </div>
          
          <div className="flex items-center gap-4">
            <button
              onClick={handlePlayNarration}
              disabled={isPlaying}
              className="btn-primary disabled:opacity-50"
            >
              {isPlaying ? (
                <>
                  <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin mr-2" />
                  Playing...
                </>
              ) : (
                <>
                  <svg className="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zM7 8a1 1 0 012 0v4a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v4a1 1 0 102 0V8a1 1 0 00-1-1z" />
                  </svg>
                  Hear My Voice
                </>
              )}
            </button>
          </div>
        </div>
      </div>

      {/* 3D Scene */}
      <div className="w-full h-screen">
        <Canvas camera={{ position: [0, 0, 5], fov: 60 }}>
          <color attach="background" args={['#0a0e27']} />
          
          {/* Dramatic lighting */}
          <ambientLight intensity={0.4} />
          <pointLight position={[10, 10, 10]} intensity={1.5} color="#6366f1" />
          <pointLight position={[-10, -10, -10]} intensity={0.8} color="#06b6d4" />
          <spotLight
            position={[0, 10, 0]}
            angle={0.3}
            penumbra={1}
            intensity={2}
            color="#a855f7"
          />
          
          <PortalRing />
          
          {pointCloudData && (
            <ScenePointCloud points={pointCloudData.points} />
          )}
          
          <OrbitControls
            enableZoom={true}
            enablePan={true}
            minDistance={2}
            maxDistance={10}
            autoRotate={false}
          />
        </Canvas>
      </div>

      {/* Narration Overlay */}
      {narration && (
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 z-20 max-w-2xl">
          <div className="glassmorphic rounded-2xl p-8 border-2 border-cyan-400/50 animate-fade-in">
            <div className="flex items-start gap-4">
              <div className="flex-shrink-0">
                <div className="w-12 h-12 rounded-full bg-gradient-to-br from-cosmic-purple to-cyan-400 flex items-center justify-center animate-pulse">
                  <svg className="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zM7 8a1 1 0 012 0v4a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v4a1 1 0 102 0V8a1 1 0 00-1-1z" />
                  </svg>
                </div>
              </div>
              <div className="flex-1">
                <p className="text-white text-lg leading-relaxed">
                  {narration.text}
                </p>
                <div className="mt-4 flex items-center gap-2">
                  <span className="text-sm text-cyan-400">Speaking in your voice</span>
                  <div className="flex gap-1">
                    {[...Array(4)].map((_, i) => (
                      <div
                        key={i}
                        className="w-1 h-4 bg-cyan-400 rounded-full animate-pulse"
                        style={{ animationDelay: `${i * 0.1}s` }}
                      />
                    ))}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Bottom Stats */}
      <div className="absolute bottom-0 left-0 right-0 z-10 p-6">
        <div className="max-w-4xl mx-auto">
          <div className="glassmorphic rounded-xl p-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-6">
                <div className="text-center">
                  <div className="text-2xl font-bold text-gradient">
                    {pointCloudData?.points?.length?.toLocaleString() || 0}
                  </div>
                  <div className="text-xs text-space-gray">3D Points</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-gradient">
                    {sceneIndex}
                  </div>
                  <div className="text-xs text-space-gray">Scene Number</div>
                </div>
              </div>
              
              <div className="flex gap-2">
                <button
                  onClick={() => navigate(`/viewer/${videoId}/scene/${Math.max(0, parseInt(sceneIndex) - 1)}`)}
                  disabled={parseInt(sceneIndex) === 0}
                  className="glassmorphic px-4 py-2 rounded-lg hover:border-cosmic-purple transition-colors disabled:opacity-30"
                >
                  Previous
                </button>
                <button
                  onClick={() => navigate(`/viewer/${videoId}/scene/${parseInt(sceneIndex) + 1}`)}
                  className="glassmorphic px-4 py-2 rounded-lg hover:border-cosmic-purple transition-colors"
                >
                  Next
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ScenePortal;
