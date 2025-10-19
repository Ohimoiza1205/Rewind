import { BrowserRouter as Router, Routes, Route, Navigate, useNavigate, useParams } from 'react-router-dom';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import LandingPage from './components/landing/LandingPage';
import LoginPage from './components/auth/LoginPage';
import Dashboard from './components/dashboard/Dashboard';
import ProtectedRoute from './components/auth/ProtectedRoute';
import SpaceBackground from './components/landing/shared/SpaceBackground';
import './index.css';

function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/login" element={<LoginPage />} />
          
          <Route
            path="/dashboard"
            element={
              <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            }
          />

          <Route
            path="/viewer/:videoId"
            element={
              <ProtectedRoute>
                <ViewerPage />
              </ProtectedRoute>
            }
          />

          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </Router>
    </AuthProvider>
  );
}

const ViewerPage = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const { videoId } = useParams();

  return (
    <div className="relative min-h-screen">
      <SpaceBackground />
      
      <div className="relative z-10 min-h-screen flex items-center justify-center p-6">
        <div className="glassmorphic rounded-2xl p-8 max-w-4xl w-full text-center">
          <h1 className="text-4xl font-space font-bold mb-6">
            Your <span className="text-gradient">3D Memory Space</span>
          </h1>
          
          <div className="aspect-video bg-space-dark rounded-xl mb-6 flex items-center justify-center border border-white/10">
            <div className="text-center p-8">
              <div className="w-20 h-20 border-4 border-cosmic-purple border-t-transparent rounded-full animate-spin mx-auto mb-4" />
              <p className="text-xl text-space-gray mb-2">Rendering 3D Memory Space...</p>
              <p className="text-sm text-space-gray">Video ID: {videoId}</p>
              <p className="text-xs text-space-gray mt-4">
                3D viewer with Three.js coming next - for now this is a placeholder
              </p>
            </div>
          </div>

          <div className="flex gap-4 justify-center">
            <button onClick={() => navigate('/dashboard')} className="btn-primary">
              Back to Dashboard
            </button>
            <button className="glassmorphic px-6 py-3 rounded-lg font-semibold">
              Download Memory
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default App;
