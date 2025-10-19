const VideoSelector = ({ videos, selectedVideo, onVideoChange, isLoading }) => {
  return (
    <div className="glassmorphic rounded-xl p-4">
      <label className="block text-sm font-space text-space-gray mb-2">
        Select Memory
      </label>
      <select
        value={selectedVideo}
        onChange={(e) => onVideoChange(e.target.value)}
        disabled={isLoading}
        className="w-full bg-space-dark border border-white/10 rounded-lg px-4 py-2 text-white focus:border-cosmic-purple focus:outline-none disabled:opacity-50"
      >
        <option value="">Choose a video...</option>
        {videos.map((video) => (
          <option key={video} value={video}>
            {video.replace(/_/g, ' ')}
          </option>
        ))}
      </select>
    </div>
  );
};

export default VideoSelector;
