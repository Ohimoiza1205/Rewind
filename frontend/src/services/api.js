const API_BASE_URL = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000';

export const api = {
  async healthCheck() {
    const response = await fetch(`${API_BASE_URL}/api/health`);
    return response.json();
  },

  async uploadVideo(file) {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch(`${API_BASE_URL}/api/upload`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      throw new Error('Upload failed');
    }

    return response.json();
  },

  async getAnalysis(videoId) {
    const response = await fetch(`${API_BASE_URL}/api/analysis/${videoId}`);
    return response.json();
  },

  async generateNarration(sceneId, language, userId) {
    const response = await fetch(`${API_BASE_URL}/api/narration/generate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ scene_id: sceneId, target_language: language, user_id: userId }),
    });
    return response.json();
  },
};
