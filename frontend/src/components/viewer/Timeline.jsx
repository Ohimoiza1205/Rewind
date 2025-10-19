import { useState, useEffect } from 'react';

const Timeline = ({ totalFrames, currentFrame, onFrameChange, isLoading }) => {
  const [isDragging, setIsDragging] = useState(false);

  const handleSliderChange = (e) => {
    const frame = parseInt(e.target.value);
    onFrameChange(frame);
  };

  return (
    <div className="w-full glassmorphic rounded-xl p-4">
      <div className="flex items-center gap-4">
        <div className="flex-shrink-0">
          <span className="text-sm font-space text-space-gray">
            Frame {currentFrame} / {totalFrames}
          </span>
        </div>

        <div className="flex-1 relative">
          <input
            type="range"
            min="0"
            max={totalFrames}
            value={currentFrame}
            onChange={handleSliderChange}
            disabled={isLoading}
            className="w-full h-2 bg-space-dark rounded-lg appearance-none cursor-pointer slider"
            style={{
              background: `linear-gradient(to right, #6366f1 0%, #6366f1 ${(currentFrame / totalFrames) * 100}%, #1a1f3a ${(currentFrame / totalFrames) * 100}%, #1a1f3a 100%)`
            }}
          />
        </div>

        <div className="flex gap-2">
          <button
            onClick={() => onFrameChange(Math.max(0, currentFrame - 1))}
            disabled={currentFrame === 0 || isLoading}
            className="glassmorphic px-3 py-1 rounded text-sm hover:border-cosmic-purple transition-colors disabled:opacity-50"
          >
            ←
          </button>
          <button
            onClick={() => onFrameChange(Math.min(totalFrames, currentFrame + 1))}
            disabled={currentFrame === totalFrames || isLoading}
            className="glassmorphic px-3 py-1 rounded text-sm hover:border-cosmic-purple transition-colors disabled:opacity-50"
          >
            →
          </button>
        </div>
      </div>

      {isLoading && (
        <div className="mt-2 text-center">
          <span className="text-xs text-space-gray animate-pulse">Loading frame...</span>
        </div>
      )}
    </div>
  );
};

export default Timeline;
