import { motion } from 'framer-motion';
import { useInView } from 'react-intersection-observer';
import { X, Sparkles } from 'lucide-react';

const ProblemSolution = () => {
  const [ref, inView] = useInView({
    triggerOnce: true,
    threshold: 0.3,
  });

  return (
    <section ref={ref} className="relative min-h-screen flex items-center py-20">
      <div className="section-container w-full">
        <motion.h2
          className="text-5xl md:text-6xl font-space font-bold text-center mb-20"
          initial={{ opacity: 0, y: 30 }}
          animate={inView ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.8 }}
        >
          Videos Trap Memories. <span className="text-gradient">REWIND Sets Them Free.</span>
        </motion.h2>

        <div className="grid md:grid-cols-2 gap-8 items-center">
          <motion.div
            className="relative p-8 rounded-2xl border border-red-500/30 bg-gradient-to-br from-red-900/10 to-transparent"
            initial={{ opacity: 0, x: -50 }}
            animate={inView ? { opacity: 1, x: 0 } : {}}
            transition={{ duration: 0.8, delay: 0.2 }}
          >
            <div className="absolute top-4 right-4">
              <X className="w-8 h-8 text-red-500" />
            </div>
            
            <h3 className="text-2xl font-space font-bold mb-4 text-red-400">Traditional Playback</h3>
            
            <div className="aspect-video bg-gray-800 rounded-lg mb-6 flex items-center justify-center grayscale">
              <div className="w-16 h-16 border-4 border-gray-600 rounded-full" />
            </div>

            <ul className="space-y-3 text-gray-400">
              <li className="flex items-start">
                <span className="mr-2">-</span>
                <span>Linear, sequential viewing only</span>
              </li>
              <li className="flex items-start">
                <span className="mr-2">-</span>
                <span>Language barriers limit sharing</span>
              </li>
              <li className="flex items-start">
                <span className="mr-2">-</span>
                <span>No context or understanding</span>
              </li>
              <li className="flex items-start">
                <span className="mr-2">-</span>
                <span>Difficult to find specific moments</span>
              </li>
            </ul>
          </motion.div>

          <motion.div
            className="relative p-8 rounded-2xl glassmorphic"
            initial={{ opacity: 0, x: 50 }}
            animate={inView ? { opacity: 1, x: 0 } : {}}
            transition={{ duration: 0.8, delay: 0.4 }}
          >
            <div className="absolute top-4 right-4">
              <Sparkles className="w-8 h-8 text-cosmic-purple animate-pulse" />
            </div>
            
            <h3 className="text-2xl font-space font-bold mb-4 text-gradient">REWIND Exploration</h3>
            
            <div className="aspect-video bg-gradient-to-br from-cosmic-purple/20 to-nebula-blue/20 rounded-lg mb-6 flex items-center justify-center relative overflow-hidden">
              <div className="absolute inset-0 bg-[radial-gradient(circle_at_50%_50%,rgba(99,102,241,0.3),transparent_70%)]" />
              <div className="relative w-16 h-16 border-4 border-cosmic-purple rounded-full animate-pulse-glow" />
            </div>

            <ul className="space-y-3">
              <li className="flex items-start text-starlight">
                <span className="mr-2 text-cosmic-purple">+</span>
                <span>Navigate memories in 3D space</span>
              </li>
              <li className="flex items-start text-starlight">
                <span className="mr-2 text-cosmic-purple">+</span>
                <span>Narrate in 29+ languages with your voice</span>
              </li>
              <li className="flex items-start text-starlight">
                <span className="mr-2 text-cosmic-purple">+</span>
                <span>AI understands scenes and objects</span>
              </li>
              <li className="flex items-start text-starlight">
                <span className="mr-2 text-cosmic-purple">+</span>
                <span>Click to explore, not just watch</span>
              </li>
            </ul>
          </motion.div>
        </div>

        <div className="flex justify-center mt-12">
          <motion.div
            className="glassmorphic px-6 py-3 rounded-full"
            initial={{ opacity: 0, scale: 0.8 }}
            animate={inView ? { opacity: 1, scale: 1 } : {}}
            transition={{ duration: 0.8, delay: 0.6 }}
          >
            <span className="text-cosmic-purple font-semibold">VS</span>
          </motion.div>
        </div>
      </div>
    </section>
  );
};

export default ProblemSolution;
