import { useState, useRef } from 'react';

const VoiceRecorder = ({ onRecordingComplete }) => {
  const [isRecording, setIsRecording] = useState(false);
  const [recordingTime, setRecordingTime] = useState(0);
  const [hasRecording, setHasRecording] = useState(false);
  const mediaRecorderRef = useRef(null);
  const timerRef = useRef(null);

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorderRef.current = new MediaRecorder(stream);
      
      const chunks = [];
      mediaRecorderRef.current.ondataavailable = (e) => chunks.push(e.data);
      
      mediaRecorderRef.current.onstop = () => {
        const blob = new Blob(chunks, { type: 'audio/webm' });
        setHasRecording(true);
        if (onRecordingComplete) onRecordingComplete(blob);
        stream.getTracks().forEach(track => track.stop());
      };

      mediaRecorderRef.current.start();
      setIsRecording(true);
      setRecordingTime(0);

      timerRef.current = setInterval(() => {
        setRecordingTime((prev) => {
          if (prev >= 30) {
            stopRecording();
            return 30;
          }
          return prev + 1;
        });
      }, 1000);
    } catch (err) {
      console.error('Error accessing microphone:', err);
      alert('Please allow microphone access to record your voice.');
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
      clearInterval(timerRef.current);
    }
  };

  return (
    <div className="glassmorphic rounded-2xl p-8 max-w-md mx-auto">
      <div className="text-center mb-6">
        <div className="w-20 h-20 mx-auto mb-4 rounded-full bg-gradient-to-br from-cosmic-purple to-nebula-blue flex items-center justify-center">
          <svg className="w-10 h-10" fill="currentColor" viewBox="0 0 20 20">
            <path d="M7 4a3 3 0 016 0v4a3 3 0 11-6 0V4zm4 10.93A7.001 7.001 0 0017 8a1 1 0 10-2 0A5 5 0 015 8a1 1 0 00-2 0 7.001 7.001 0 006 6.93V17H6a1 1 0 100 2h8a1 1 0 100-2h-3v-2.07z" />
          </svg>
        </div>
        
        <h3 className="text-2xl font-space font-bold mb-2">Clone Your Voice</h3>
        <p className="text-space-gray text-sm">
          Record 30 seconds of your voice to enable multilingual narration
        </p>
      </div>

      {/* Recording visualizer */}
      <div className="mb-6">
        <div className="h-32 glassmorphic rounded-xl p-4 flex items-center justify-center">
          {isRecording ? (
            <div className="flex items-center gap-1">
              {[...Array(16)].map((_, i) => (
                <div
                  key={i}
                  className="w-2 bg-gradient-to-t from-cosmic-purple to-accent-cyan rounded-full animate-pulse"
                  style={{
                    height: `${Math.random() * 60 + 20}px`,
                    animationDelay: `${i * 0.1}s`,
                  }}
                />
              ))}
            </div>
          ) : hasRecording ? (
            <div className="text-center">
              <svg className="w-12 h-12 mx-auto mb-2 text-green-400" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
              </svg>
              <p className="text-sm text-space-gray">Voice recorded successfully</p>
            </div>
          ) : (
            <p className="text-space-gray">Ready to record</p>
          )}
        </div>

        {/* Timer */}
        {(isRecording || recordingTime > 0) && (
          <div className="mt-4 text-center">
            <div className="text-3xl font-bold text-gradient">
              {recordingTime}s
            </div>
            <div className="w-full h-2 bg-deep-space rounded-full mt-2 overflow-hidden">
              <div 
                className="h-full bg-gradient-to-r from-cosmic-purple to-accent-cyan transition-all duration-300"
                style={{ width: `${(recordingTime / 30) * 100}%` }}
              />
            </div>
          </div>
        )}
      </div>

      {/* Controls */}
      <div className="flex gap-4">
        {!isRecording && !hasRecording && (
          <button
            onClick={startRecording}
            className="flex-1 btn-primary flex items-center justify-center gap-2"
          >
            <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
              <path d="M7 4a3 3 0 016 0v4a3 3 0 11-6 0V4zm4 10.93A7.001 7.001 0 0017 8a1 1 0 10-2 0A5 5 0 015 8a1 1 0 00-2 0 7.001 7.001 0 006 6.93V17H6a1 1 0 100 2h8a1 1 0 100-2h-3v-2.07z" />
            </svg>
            Start Recording
          </button>
        )}

        {isRecording && (
          <button
            onClick={stopRecording}
            className="flex-1 bg-red-500 hover:bg-red-600 text-white px-6 py-3 rounded-lg font-semibold transition-colors flex items-center justify-center gap-2"
          >
            <div className="w-3 h-3 bg-white rounded-sm" />
            Stop Recording
          </button>
        )}

        {hasRecording && (
          <>
            <button
              onClick={() => {
                setHasRecording(false);
                setRecordingTime(0);
              }}
              className="flex-1 glassmorphic px-6 py-3 rounded-lg font-semibold hover:border-cosmic-purple transition-colors"
            >
              Re-record
            </button>
            <button
              onClick={() => alert('Voice cloning would start here - Backend integration needed')}
              className="flex-1 btn-primary"
            >
              Clone Voice
            </button>
          </>
        )}
      </div>

      <p className="text-xs text-space-gray text-center mt-4">
        Your voice data is processed securely and never shared
      </p>
    </div>
  );
};

export default VoiceRecorder;
