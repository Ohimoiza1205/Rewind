import { useNavigate } from 'react-router-dom';
import SpaceBackground from './shared/SpaceBackground';
import HeroSection from './hero/HeroSection';
import ProblemSolution from './shared/ProblemSolution';
import FeatureCards from './features/FeatureCards';
import VoiceBridgeDemo from './voicebridge/VoiceBridgeDemo';
import SocialProof from './social/SocialProof';
import FinalCTA from './cta/FinalCTA';

const LandingPage = () => {
  const navigate = useNavigate();

  const handleGetStarted = () => {
    navigate('/login');
  };

  return (
    <div className="relative min-h-screen">
      <SpaceBackground />
      
      <div className="relative z-10">
        <HeroSection onGetStarted={handleGetStarted} />
        <ProblemSolution />
        <FeatureCards />
        <VoiceBridgeDemo />
        <SocialProof />
        <FinalCTA onGetStarted={handleGetStarted} />
      </div>

      <footer className="relative z-10 border-t border-white/10 py-8">
        <div className="section-container">
          <div className="flex flex-col md:flex-row justify-between items-center gap-4">
            <div className="text-space-gray text-sm">
              © 2024 REWIND. All rights reserved.
            </div>
            <div className="flex gap-6 text-sm">
              <a href="#" className="text-space-gray hover:text-starlight transition-colors">
                Privacy Policy
              </a>
              <a href="#" className="text-space-gray hover:text-starlight transition-colors">
                Terms of Service
              </a>
              <a href="#" className="text-space-gray hover:text-starlight transition-colors">
                Contact
              </a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default LandingPage;
