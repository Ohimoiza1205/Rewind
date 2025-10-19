import { useEffect, useRef, useState } from 'react';
import VoiceRecorder from './VoiceRecorder';

const languages = [
  { code: 'en', flag: '🇺🇸', name: 'English' },
  { code: 'es', flag: '🇪🇸', name: 'Spanish' },
  { code: 'fr', flag: '🇫🇷', name: 'French' },
  { code: 'de', flag: '🇩🇪', name: 'German' },
  { code: 'zh', flag: '🇨🇳', name: 'Mandarin' },
];

const AudioWaveform = ({ isPlaying }) => {
  const canvasRef = useRef(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    const bars = 64;
    const barWidth = canvas.width / bars;
    let animationId;

    const animate = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      for (let i = 0; i < bars; i++) {
        const height = isPlaying
          ? Math.sin(Date.now() * 0.01 + i * 0.5) * 50 + 50
          : 20;

        const gradient = ctx.createLinearGradient(0, 0, 0, canvas.height);
        gradient.addColorStop(0, '#6366f1');
        gradient.addColorStop(1, '#06b6d4');

        ctx.fillStyle = gradient;
        ctx.fillRect(i * barWidth, canvas.height - height, barWidth - 2, height);
      }

      animationId = requestAnimationFrame(animate);
    };

    animate();
    return () => cancelAnimationFrame(animationId);
  }, [isPlaying]);

  return <canvas ref={canvasRef} width={800} height={200} className="w-full h-full" />;
};

const VoiceBridgeDemo = () => {
  const [selectedLang, setSelectedLang] = useState('en');
  const [displayText, setDisplayText] = useState("Here's Emma blowing out the candles...");
  const [isPlaying, setIsPlaying] = useState(false);
  const [showRecorder, setShowRecorder] = useState(false);
  const [voiceCloned, setVoiceCloned] = useState(false);

  const translations = {
    en: "Here's Emma blowing out the candles on her fifth birthday cake...",
    es: "Aquí está Emma soplando las velas de su pastel de quinto cumpleaños...",
    fr: "Voici Emma soufflant les bougies de son gâteau d'anniversaire...",
    de: "Hier bläst Emma die Kerzen auf ihrer Geburtstagstorte aus...",
    zh: "这是艾玛吹灭她的五岁生日蛋糕上的蜡烛...",
  };

  const handleLanguageSelect = (langCode) => {
    setSelectedLang(langCode);
    setDisplayText(translations[langCode]);
  };

  const handlePlayNarration = () => {
    if (!voiceCloned) {
      setShowRecorder(true);
      return;
    }
    setIsPlaying(true);
    setTimeout(() => setIsPlaying(false), 3000);
  };

  const handleRecordingComplete = (blob) => {
    console.log('Recording complete:', blob);
    setVoiceCloned(true);
    setShowRecorder(false);
  };

  return (
    <section className="relative min-h-screen flex items-center py-20">
      <div className="section-container w-full">
        <div className="text-center mb-16">
          <h2 className="text-5xl md:text-6xl font-space font-bold mb-6">
            One Video. <span className="text-gradient">29 Languages.</span> Always Your Voice.
          </h2>
          <p className="text-xl text-space-gray max-w-3xl mx-auto">
            VoiceBridge translates scene descriptions while preserving your unique voice
          </p>
        </div>

        {showRecorder ? (
          <div className="max-w-2xl mx-auto mb-12">
            <VoiceRecorder onRecordingComplete={handleRecordingComplete} />
            <button
              onClick={() => setShowRecorder(false)}
              className="mt-4 mx-auto block text-space-gray hover:text-white transition-colors"
            >
              Skip for now
            </button>
          </div>
        ) : (
          <div className="max-w-5xl mx-auto">
            <div className="glassmorphic rounded-3xl p-8 md:p-12 mb-8">
              <div className="text-center mb-8">
                <p className="text-2xl md:text-3xl leading-relaxed min-h-[100px] font-space">
                  {displayText}
                </p>
              </div>

              <div className="h-48 mb-8 glassmorphic rounded-xl p-4">
                <AudioWaveform isPlaying={isPlaying} />
              </div>

              <div className="flex justify-center">
                <button onClick={handlePlayNarration} className="btn-primary flex items-center gap-2">
                  <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M6.3 2.841A1.5 1.5 0 004 4.11V15.89a1.5 1.5 0 002.3 1.269l9.344-5.89a1.5 1.5 0 000-2.538L6.3 2.84z" />
                  </svg>
                  {voiceCloned ? 'Hear My Voice' : 'Clone Voice First'}
                </button>
              </div>

              {voiceCloned && (
                <p className="text-center text-green-400 text-sm mt-4">
                  ✓ Voice cloned successfully
                </p>
              )}
            </div>

            <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
              {languages.map((lang) => (
                <button
                  key={lang.code}
                  onClick={() => handleLanguageSelect(lang.code)}
                  className={`glassmorphic rounded-xl p-4 transition-all duration-300 hover:scale-105 ${
                    selectedLang === lang.code
                      ? 'border-2 border-cosmic-purple shadow-lg shadow-cosmic-purple/50'
                      : 'border border-white/10'
                  }`}
                >
                  <div className="text-4xl mb-2">{lang.flag}</div>
                  <div className="text-sm font-semibold">{lang.name}</div>
                </button>
              ))}
            </div>
          </div>
        )}
      </div>
    </section>
  );
};

export default VoiceBridgeDemo;
