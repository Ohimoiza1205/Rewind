import { useState } from 'react';
import { api } from '../../services/api';

const VideoUpload = ({ onUploadComplete }) => {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [uploadResult, setUploadResult] = useState(null);
  const [error, setError] = useState(null);

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
    } catch (err) {
      setError(err.message);
    } finally {
      setUploading(false);
    }
  };

  const handleViewMemory = () => {
    if (onUploadComplete && uploadResult) {
      onUploadComplete(uploadResult.video_id);
    }
  };

  return (
    <div className="min-h-screen bg-deep-space flex items-center justify-center p-6">
      <div className="glassmorphic rounded-2xl p-8 max-w-2xl w-full">
        <h1 className="text-4xl font-space font-bold mb-6 text-center">
          Upload Your <span className="text-gradient">Memory</span>
        </h1>

        {!uploadResult ? (
          <>
            <div className="mb-6">
              <label className="block text-space-gray mb-2">Select Video</label>
              <input
                type="file"
                accept="video/*"
                onChange={handleFileChange}
                className="w-full px-4 py-3 bg-space-dark rounded-lg border border-white/10 text-white"
              />
              {file && (
                <p className="mt-2 text-sm text-space-gray">
                  Selected: {file.name} ({(file.size / 1024 / 1024).toFixed(2)} MB)
                </p>
              )}
            </div>

            {error && (
              <div className="mb-4 p-4 bg-red-500/10 border border-red-500/50 rounded-lg text-red-400">
                {error}
              </div>
            )}

            <button
              onClick={handleUpload}
              disabled={!file || uploading}
              className="w-full btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {uploading ? 'Uploading...' : 'Upload Video'}
            </button>

            {uploading && (
              <div className="mt-4">
                <div className="w-full h-2 bg-deep-space rounded-full overflow-hidden">
                  <div className="h-full bg-gradient-to-r from-cosmic-purple to-accent-cyan animate-pulse w-3/4" />
                </div>
                <p className="text-center text-space-gray mt-2 text-sm">Processing your memory...</p>
              </div>
            )}
          </>
        ) : (
          <div className="text-center">
            <div className="mb-6 p-6 bg-green-500/10 border border-green-500/50 rounded-lg">
              <svg className="w-16 h-16 mx-auto mb-4 text-green-400" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
              </svg>
              <h2 className="text-2xl font-space font-bold text-green-400 mb-2">Upload Successful!</h2>
              <p className="text-space-gray">Video ID: {uploadResult.video_id}</p>
              <p className="text-space-gray text-sm mt-2">Size: {uploadResult.file_size_mb} MB</p>
            </div>

            <div className="mb-6 p-6 glassmorphic rounded-xl">
              <h3 className="text-xl font-space font-bold mb-4">Processing Your Memory...</h3>
              <div className="space-y-3 text-left">
                <div className="flex items-center">
                  <svg className="w-5 h-5 text-green-400 mr-3" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                  </svg>
                  <span>Extracting video frames</span>
                </div>
                <div className="flex items-center">
                  <div className="w-5 h-5 border-2 border-cosmic-purple border-t-transparent rounded-full animate-spin mr-3" />
                  <span className="text-space-gray">Generating 3D depth maps...</span>
                </div>
                <div className="flex items-center opacity-50">
                  <div className="w-5 h-5 border-2 border-space-gray rounded-full mr-3" />
                  <span className="text-space-gray">AI scene detection</span>
                </div>
                <div className="flex items-center opacity-50">
                  <div className="w-5 h-5 border-2 border-space-gray rounded-full mr-3" />
                  <span className="text-space-gray">Creating narration</span>
                </div>
              </div>
            </div>

            <div className="flex gap-4">
              <button
                onClick={handleViewMemory}
                className="flex-1 btn-primary"
              >
                View 3D Memory Space
              </button>
              <button
                onClick={() => {
                  setUploadResult(null);
                  setFile(null);
                }}
                className="flex-1 glassmorphic px-6 py-3 rounded-lg font-semibold hover:border-cosmic-purple transition-colors"
              >
                Upload Another
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default VideoUpload;
