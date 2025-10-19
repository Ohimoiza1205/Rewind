import { useState, useEffect } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import { logout } from '../../services/firebase';
import { useNavigate } from 'react-router-dom';
import SpaceBackground from '../landing/shared/SpaceBackground';
import { api } from '../../services/api';

const Dashboard = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [uploadResult, setUploadResult] = useState(null);
  const [error, setError] = useState(null);
  const [processingStatus, setProcessingStatus] = useState(null);
  const [videos, setVideos] = useState([]);
  const [loadingVideos, setLoadingVideos] = useState(true);

  // Load existing videos on mount
  useEffect(() => {
    const loadVideos = async () => {
      try {
        const result = await api.getVideos();
        const videosWithMetadata = await Promise.all(
          result.videos.map(async (videoName) => {
            try {
              const metadata = await api.getVideoMetadata(videoName);
              return {
                id: videoName,
                name: videoName,
                frames: metadata.metadata?.total_frames || 0,
              };
            } catch {
              return {
                id: videoName,
                name: videoName,
                frames: 0,
              };
            }
          })
        );
        setVideos(videosWithMetadata);
      } catch (err) {
        console.error('Error loading videos:', err);
      } finally {
        setLoadingVideos(false);
      }
    };
    loadVideos();
  }, []);

  // Poll for processing status
  useEffect(() => {
    if (!uploadResult?.video_id) return;

    const pollStatus = setInterval(async () => {
      try {
        const status = await api.getDepthStatus(uploadResult.video_id);
        setProcessingStatus(status.depth_processing);

        if (status.depth_processing?.status === 'complete') {
          clearInterval(pollStatus);
          setTimeout(() => {
            navigate(`/viewer/${uploadResult.video_id}`);
          }, 1000);
        }
      } catch (err) {
        console.error('Error checking status:', err);
      }
    }, 3000);

    return () => clearInterval(pollStatus);
  }, [uploadResult, navigate]);

  const handleLogout = async () => {
    try {
      await logout();
      navigate('/');
    } catch (error) {
      console.error('Logout failed:', error);
    }
  };

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      setFile(selectedFile);
      setError(null);
      setUploadResult(null);
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setError('Please select a file');
      return;
    }

    setUploading(true);
    setError(null);

    try {
      const result = await api.uploadVideo(file);
      setUploadResult(result);
      setUploading(false);
    } catch (err) {
      setError(err.message);
      setUploading(false);
    }
  };

  const handleViewExisting = (videoId) => {
    navigate(`/viewer/${videoId}`);
  };

  return (
    <div className="relative min-h-screen">
      <SpaceBackground />

      <div className="relative z-10">
        {/* Header */}
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
          {/* Welcome Section */}
          <div className="text-center mb-12">
            <h2 className="text-5xl font-space font-bold mb-4">
              Welcome back, <span className="text-gradient">{user?.displayName?.split(' ')[0]}</span>
            </h2>
            <p className="text-xl text-space-gray">
              Transform your videos into explorable memory galaxies
            </p>
          </div>

          {/* Stats */}
          <div className="grid md:grid-cols-3 gap-6 mb-12">
            <div className="glassmorphic rounded-2xl p-6 text-center">
              <div className="text-4xl font-bold text-gradient mb-2">{videos.length}</div>
              <div className="text-space-gray">Videos Uploaded</div>
            </div>

            <div className="glassmorphic rounded-2xl p-6 text-center">
              <div className="text-4xl font-bold text-gradient mb-2">{videos.length}</div>
              <div className="text-space-gray">3D Memories</div>
            </div>

            <div className="glassmorphic rounded-2xl p-6 text-center">
              <div className="text-4xl font-bold text-gradient mb-2">
                {videos.reduce((sum, v) => sum + v.frames, 0)}
              </div>
              <div className="text-space-gray">Narrations</div>
            </div>
          </div>

          {/* Upload Section */}
          {!uploadResult ? (
            <div className="glassmorphic rounded-3xl p-12 text-center max-w-3xl mx-auto">
              <div className="w-24 h-24 mx-auto mb-6 rounded-full bg-gradient-to-br from-cosmic-purple to-nebula-blue flex items-center justify-center">
                <svg className="w-12 h-12 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                </svg>
              </div>

              <h3 className="text-3xl font-space font-bold mb-4">
                Upload Your First Memory
              </h3>
              <p className="text-space-gray mb-8 max-w-2xl mx-auto">
                Transform your videos into immersive 3D experiences. Explore frozen moments in time, navigate through memory constellations, and add voice narration in 29+ languages.
              </p>

              <div className="mb-6">
                <input
                  type="file"
                  accept="video/*"
                  onChange={handleFileChange}
                  className="hidden"
                  id="video-upload"
                />
                <label
                  htmlFor="video-upload"
                  className="inline-block glassmorphic px-6 py-3 rounded-lg cursor-pointer hover:border-cosmic-purple transition-colors"
                >
                  {file ? `Selected: ${file.name}` : 'Choose Video File'}
                </label>
              </div>

              {error && (
                <div className="mb-4 p-4 bg-red-500/10 border border-red-500/50 rounded-lg text-red-400 text-sm">
                  {error}
                </div>
              )}

              <button
                onClick={handleUpload}
                disabled={!file || uploading}
                className="btn-primary text-lg disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {uploading ? 'Uploading...' : 'Upload & Create Memory Galaxy'}
              </button>
            </div>
          ) : (
            <div className="glassmorphic rounded-3xl p-12 text-center max-w-3xl mx-auto">
              <div className="mb-6">
                <div className="w-20 h-20 mx-auto mb-4 rounded-full bg-gradient-to-br from-cosmic-purple to-cyan-400 flex items-center justify-center">
                  <div className="w-16 h-16 border-4 border-white border-t-transparent rounded-full animate-spin" />
                </div>
                <h2 className="text-3xl font-space font-bold mb-2">Processing Your Memory</h2>
                <p className="text-space-gray mb-4">Video ID: {uploadResult.video_id}</p>
                
                {processingStatus && (
                  <div className="space-y-2">
                    <div className="text-lg text-cyan-400">
                      {processingStatus.status === 'complete' 
                        ? '✨ Processing Complete!' 
                        : `🔄 ${processingStatus.progress || 0}% - Generating 3D depth maps...`}
                    </div>
                    {processingStatus.status === 'complete' && (
                      <p className="text-sm text-green-400">Redirecting to Memory Galaxy...</p>
                    )}
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Quick Access to Processed Videos */}
          <div className="mt-12 max-w-3xl mx-auto">
            <h3 className="text-2xl font-space font-bold mb-6 text-center">
              Your Memory Galaxies
            </h3>
            
            {loadingVideos ? (
              <div className="text-center text-space-gray">Loading memories...</div>
            ) : videos.length === 0 ? (
              <div className="text-center text-space-gray">No memories yet. Upload your first video!</div>
            ) : (
              <div className="grid md:grid-cols-2 gap-4">
                {videos.map((video) => (
                  <button
                    key={video.id}
                    onClick={() => handleViewExisting(video.id)}
                    className="glassmorphic rounded-xl p-6 text-left hover:border-cosmic-purple transition-all hover:scale-105"
                  >
                    <div className="flex items-center gap-4">
                      <div className="w-12 h-12 rounded-full bg-gradient-to-br from-cosmic-purple to-cyan-400 flex-shrink-0" />
                      <div className="flex-1 min-w-0">
                        <h4 className="font-semibold mb-1 truncate">{video.name}</h4>
                        <p className="text-sm text-space-gray">{video.frames} frames</p>
                      </div>
                    </div>
                  </button>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;