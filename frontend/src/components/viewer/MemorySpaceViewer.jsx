import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import PointCloudViewer from './PointCloudViewer';
import Timeline from './Timeline';
import VideoSelector from './VideoSelector';
import SpaceBackground from '../landing/shared/SpaceBackground';

const MemorySpaceViewer = ({ videoId }) => {
  const navigate = useNavigate();
  const [videos, setVideos] = useState([]);
  const [selectedVideo, setSelectedVideo] = useState(videoId || '');
  const [metadata, setMetadata] = useState(null);
  const [currentFrame, setCurrentFrame] = useState(0);
  const [pointCloudData, setPointCloudData] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const API_BASE = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000';

  // Load available videos
  useEffect(() => {
    const loadVideos = async () => {
      try {
        const response = await fetch(`${API_BASE}/api/pointcloud/videos`);
        const data = await response.json();
        
        if (data.success && data.videos.length > 0) {
          setVideos(data.videos);
          if (!selectedVideo && data.videos.length > 0) {
            setSelectedVideo(data.videos[0]);
          }
        }
      } catch (err) {
        console.error('Failed to load videos:', err);
        setError('No processed videos found');
      }
    };

    loadVideos();
  }, []);

  // Load metadata when video selected
  useEffect(() => {
    if (!selectedVideo) return;

    const loadMetadata = async () => {
      try {
        const response = await fetch(`${API_BASE}/api/pointcloud/metadata/${selectedVideo}`);
        const data = await response.json();
        
        if (data.success) {
          setMetadata(data.metadata);
          setCurrentFrame(0);
        }
      } catch (err) {
        console.error('Failed to load metadata:', err);
      }
    };

    loadMetadata();
  }, [selectedVideo]);

  // Load point cloud frame
  useEffect(() => {
    if (!selectedVideo || !metadata) return;

    const loadFrame = async () => {
      setIsLoading(true);
      try {
        const response = await fetch(
          `${API_BASE}/api/pointcloud/frame/${selectedVideo}/${currentFrame}`
        );
        const data = await response.json();
        setPointCloudData(data);
        setError(null);
      } catch (err) {
        console.error('Failed to load frame:', err);
        setError('Failed to load 3D data');
      } finally {
        setIsLoading(false);
      }
    };

    loadFrame();
  }, [selectedVideo, currentFrame, metadata]);

  const handleFrameChange = (newFrame) => {
    setCurrentFrame(newFrame);
  };

  const handleVideoChange = (newVideo) => {
    setSelectedVideo(newVideo);
    setCurrentFrame(0);
  };

  if (error && videos.length === 0) {
    return (
      <div className="relative min-h-screen">
        <SpaceBackground />
        <div className="relative z-10 min-h-screen flex items-center justify-center p-6">
          <div className="glassmorphic rounded-2xl p-8 max-w-2xl w-full text-center">
            <div className="w-20 h-20 mx-auto mb-6 rounded-full bg-red-500/10 flex items-center justify-center">
              <svg className="w-10 h-10 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            
            <h2 className="text-2xl font-space font-bold mb-4">No Processed Videos Yet</h2>
            <p className="text-space-gray mb-6">
              Upload a video and wait for 3D processing to complete before viewing
            </p>
            
            <button
              onClick={() => navigate('/dashboard')}
              className="btn-primary"
            >
              Go to Dashboard
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="relative min-h-screen">
      <SpaceBackground />
      
      <div className="relative z-10 min-h-screen flex flex-col">
        {/* Header */}
        <div className="border-b border-white/10 backdrop-blur-sm">
          <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
            <h1 className="text-2xl font-space font-bold">
              <span className="text-gradient">3D Memory Space</span>
            </h1>
            <button
              onClick={() => navigate('/dashboard')}
              className="glassmorphic px-4 py-2 rounded-lg text-sm hover:border-cosmic-purple transition-colors"
            >
              ← Back
            </button>
          </div>
        </div>

        {/* Main Content */}
        <div className="flex-1 max-w-7xl mx-auto w-full px-6 py-6 flex flex-col gap-4">
          {/* Video Selector */}
          {videos.length > 0 && (
            <VideoSelector
              videos={videos}
              selectedVideo={selectedVideo}
              onVideoChange={handleVideoChange}
              isLoading={isLoading}
            />
          )}

          {/* 3D Viewer */}
          <div className="flex-1 glassmorphic rounded-2xl overflow-hidden" style={{ minHeight: '500px' }}>
            {pointCloudData ? (
              <PointCloudViewer
                pointCloudData={pointCloudData}
                currentFrame={currentFrame}
              />
            ) : (
              <div className="w-full h-full flex items-center justify-center">
                <div className="text-center">
                  <div className="w-16 h-16 border-4 border-cosmic-purple border-t-transparent rounded-full animate-spin mx-auto mb-4" />
                  <p className="text-space-gray">Loading 3D memory space...</p>
                </div>
              </div>
            )}
          </div>

          {/* Timeline */}
          {metadata && (
            <Timeline
              totalFrames={metadata.total_frames - 1}
              currentFrame={currentFrame}
              onFrameChange={handleFrameChange}
              isLoading={isLoading}
            />
          )}

          {/* Stats */}
          {metadata && pointCloudData && (
            <div className="grid grid-cols-3 gap-4">
              <div className="glassmorphic rounded-xl p-4 text-center">
                <div className="text-2xl font-bold text-gradient mb-1">
                  {pointCloudData.points?.length?.toLocaleString() || 0}
                </div>
                <div className="text-xs text-space-gray">3D Points</div>
              </div>
              <div className="glassmorphic rounded-xl p-4 text-center">
                <div className="text-2xl font-bold text-gradient mb-1">
                  {metadata.total_frames}
                </div>
                <div className="text-xs text-space-gray">Total Frames</div>
              </div>
              <div className="glassmorphic rounded-xl p-4 text-center">
                <div className="text-2xl font-bold text-gradient mb-1">
                  {metadata.fps || 2} FPS
                </div>
                <div className="text-xs text-space-gray">Frame Rate</div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default MemorySpaceViewer;
