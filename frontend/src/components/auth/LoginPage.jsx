import { useState } from 'react';
import { signInWithGoogle } from '../../services/firebase';
import { useNavigate } from 'react-router-dom';
import SpaceBackground from '../landing/shared/SpaceBackground';

const LoginPage = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const handleGoogleSignIn = async () => {
    setLoading(true);
    setError(null);

    try {
      const user = await signInWithGoogle();
      console.log('Signed in:', user.displayName);
      navigate('/dashboard');
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="relative min-h-screen flex items-center justify-center overflow-hidden">
      <SpaceBackground />

      <div className="relative z-10 w-full max-w-md px-6">
        <div className="glassmorphic rounded-3xl p-8 md:p-12">
          <div className="text-center mb-8">
            <div className="inline-block mb-4">
              <div className="w-20 h-20 rounded-full bg-gradient-to-br from-cosmic-purple to-nebula-blue flex items-center justify-center">
                <svg className="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
              </div>
            </div>

            <h1 className="text-4xl font-space font-bold mb-2">
              Welcome to <span className="text-gradient">Rewind</span>
            </h1>
            <p className="text-space-gray">
              Step into your memories in 3D
            </p>
          </div>

          {error && (
            <div className="mb-6 p-4 bg-red-500/10 border border-red-500/50 rounded-lg text-red-400 text-sm">
              {error}
            </div>
          )}

          <button
            onClick={handleGoogleSignIn}
            disabled={loading}
            className="w-full glassmorphic border-2 border-white/20 hover:border-cosmic-purple px-6 py-4 rounded-xl font-semibold transition-all duration-300 hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-3 group"
          >
            <svg className="w-6 h-6" viewBox="0 0 24 24">
              <path
                fill="currentColor"
                d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
              />
              <path
                fill="currentColor"
                d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
              />
              <path
                fill="currentColor"
                d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
              />
              <path
                fill="currentColor"
                d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
              />
            </svg>
            <span className="group-hover:text-cosmic-purple transition-colors">
              {loading ? 'Signing in...' : 'Continue with Google'}
            </span>
          </button>

          <div className="mt-6 text-center text-sm text-space-gray">
            By continuing, you agree to our{' '}
            <a href="#" className="text-cosmic-purple hover:underline">
              Terms of Service
            </a>{' '}
            and{' '}
            <a href="#" className="text-cosmic-purple hover:underline">
              Privacy Policy
            </a>
          </div>

          <div className="mt-8 pt-6 border-t border-white/10 text-center">
            <button
              onClick={() => navigate('/')}
              className="text-space-gray hover:text-white transition-colors"
            >
              Back to Home
            </button>
          </div>
        </div>

        <div className="mt-6 text-center">
          <div className="inline-flex items-center gap-2 text-sm text-space-gray">
            <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse" />
            <span>Secure authentication powered by Google</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;
