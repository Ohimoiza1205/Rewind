import { Navigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';

const ProtectedRoute = ({ children }) => {
  const { user, loading } = useAuth();

  if (loading) {
    return (
      <div className="min-h-screen bg-deep-space flex items-center justify-center">
        <div className="text-center">
          <div className="w-16 h-16 border-4 border-cosmic-purple border-t-transparent rounded-full animate-spin mx-auto mb-4" />
          <p className="text-space-gray">Loading...</p>
        </div>
      </div>
    );
  }

  if (!user) {
    return <Navigate to="/login" replace />;
  }

  return children;
};

export default ProtectedRoute;
