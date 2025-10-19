import { useState } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import { logout } from '../../services/firebase';
import { useNavigate } from 'react-router-dom';
import SpaceBackground from '../landing/shared/SpaceBackground';
import VideoUpload from '../upload/VideoUpload';

const Dashboard = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [showUpload, setShowUpload] = useState(false);

  const handleLogout = async () => {
    try {
      await logout();
      navigate('/');
    } catch (error) {
      console.error('Logout failed:', error);
    }
  };

  const handleUploadComplete = (videoId) => {
    navigate(`/viewer/${videoId}`);
  };

  if (showUpload) {
    return <VideoUpload onUploadComplete={handleUploadComplete} />;
  }

  return (
    <div className="relative min-h-screen">
      <SpaceBackground />

      <div className="relative z-10">
        <nav className="border-b border-white/10 backdrop-blur-sm">
          <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
            <h1 className="text-2xl font-space font-bold text-gradient">Rewind</h1>

            <div className="flex items-center gap-4">
              <span className="text-space-gray">
                {user?.displayName}
              </span>
              <img
                src={user?.photoURL}
                alt={user?.displayName}
                className="w-10 h-10 rounded-full border-2 border-cosmic-purple"
              />
              <button
                onClick={handleLogout}
                className="glassmorphic px-4 py-2 rounded-lg text-sm hover:border-cosmic-purple transition-colors"
              >
                Logout
              </button>
            </div>
          </div>
        </nav>

        <div className="max-w-7xl mx-auto px-6 py-12">
          <div className="text-center mb-12">
            <h2 className="text-5xl font-space font-bold mb-4">
              Welcome back, <span className="text-gradient">{user?.displayName?.split(' ')[0]}</span>
            </h2>
            <p className="text-xl text-space-gray">
              Ready to explore your memories in 3D?
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-6 mb-12">
            <div className="glassmorphic rounded-2xl p-6 text-center">
              <div className="text-4xl font-bold text-gradient mb-2">0</div>
              <div className="text-space-gray">Videos Uploaded</div>
            </div>

            <div className="glassmorphic rounded-2xl p-6 text-center">
              <div className="text-4xl font-bold text-gradient mb-2">0</div>
              <div className="text-space-gray">3D Memories</div>
            </div>

            <div className="glassmorphic rounded-2xl p-6 text-center">
              <div className="text-4xl font-bold text-gradient mb-2">0</div>
              <div className="text-space-gray">Narrations</div>
            </div>
          </div>

          <div className="glassmorphic rounded-3xl p-12 text-center">
            <svg className="w-24 h-24 mx-auto mb-6 text-cosmic-purple opacity-50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
            </svg>

            <h3 className="text-3xl font-space font-bold mb-4">
              Upload Your First Memory
            </h3>
            <p className="text-space-gray mb-8 max-w-2xl mx-auto">
              Transform your videos into immersive 3D experiences. Add voice narration in 29+ languages.
            </p>

            <button
              onClick={() => setShowUpload(true)}
              className="btn-primary text-lg"
            >
              Upload Video
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
