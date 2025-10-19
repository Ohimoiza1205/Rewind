import { motion } from 'framer-motion';
import { useInView } from 'react-intersection-observer';
import { Box, Brain, Mic } from 'lucide-react';
import { useState } from 'react';

const features = [
  {
    icon: Box,
    title: '3D Exploration',
    description: 'Navigate through memories in immersive 3D space. Click, explore, and discover moments from any angle.',
    demo: '3d-scene',
  },
  {
    icon: Brain,
    title: 'AI Understanding',
    description: 'Advanced AI automatically detects objects, people, and actions. Search your memories naturally.',
    demo: 'ai-detection',
  },
  {
    icon: Mic,
    title: 'VoiceBridge™',
    description: 'Your voice, any language. Generate narration in 29+ languages while preserving your unique voice.',
    demo: 'voice-wave',
  },
];

const FeatureCard = ({ feature, index }) => {
  const [isHovered, setIsHovered] = useState(false);
  const Icon = feature.icon;

  return (
    <motion.div
      className="feature-card relative group"
      initial={{ opacity: 0, y: 50 }}
      whileInView={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6, delay: index * 0.2 }}
      viewport={{ once: true }}
      onHoverStart={() => setIsHovered(true)}
      onHoverEnd={() => setIsHovered(false)}
      whileHover={{ y: -8 }}
    >
      <div className="absolute inset-0 bg-gradient-to-br from-cosmic-purple/20 to-nebula-blue/20 rounded-2xl blur-xl opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
      
      <div className="relative z-10">
        <div className="mb-6">
          <div className="w-16 h-16 rounded-full bg-gradient-to-br from-cosmic-purple to-nebula-blue flex items-center justify-center">
            <Icon className="w-8 h-8 text-white" />
          </div>
        </div>

        <h3 className="text-2xl font-space font-bold mb-4">{feature.title}</h3>
        <p className="text-space-gray leading-relaxed mb-6">{feature.description}</p>

        <div className="h-32 rounded-lg bg-gradient-to-br from-deep-space to-space-dark flex items-center justify-center overflow-hidden">
          {feature.demo === '3d-scene' && (
            <div className="relative w-20 h-20">
              <motion.div
                className="absolute inset-0 border-2 border-cosmic-purple rounded-lg"
                animate={isHovered ? { rotate: 360 } : { rotate: 0 }}
                transition={{ duration: 2, ease: 'linear', repeat: isHovered ? Infinity : 0 }}
              />
            </div>
          )}
          
          {feature.demo === 'ai-detection' && (
            <div className="relative w-full h-full flex items-center justify-center">
              <motion.div
                className="absolute w-16 h-16 border-2 border-nebula-blue rounded"
                animate={isHovered ? { scale: [1, 1.2, 1] } : {}}
                transition={{ duration: 1, repeat: isHovered ? Infinity : 0 }}
              />
              <motion.div
                className="absolute w-10 h-10 border-2 border-accent-cyan rounded"
                animate={isHovered ? { scale: [1, 1.3, 1] } : {}}
                transition={{ duration: 1, delay: 0.2, repeat: isHovered ? Infinity : 0 }}
              />
            </div>
          )}
          
          {feature.demo === 'voice-wave' && (
            <div className="flex items-center justify-center gap-1">
              {[...Array(8)].map((_, i) => (
                <motion.div
                  key={i}
                  className="w-2 bg-gradient-to-t from-cosmic-purple to-accent-cyan rounded-full"
                  animate={isHovered ? {
                    height: [16, 32, 16],
                  } : { height: 16 }}
                  transition={{
                    duration: 0.8,
                    repeat: isHovered ? Infinity : 0,
                    delay: i * 0.1,
                  }}
                />
              ))}
            </div>
          )}
        </div>

        <motion.a
          href="#"
          className="inline-flex items-center text-cosmic-purple mt-4 font-semibold group-hover:text-nebula-blue transition-colors"
        >
          Learn More
          <motion.span
            className="ml-2"
            animate={isHovered ? { x: 5 } : { x: 0 }}
            transition={{ duration: 0.3 }}
          >
            →
          </motion.span>
        </motion.a>
      </div>
    </motion.div>
  );
};

const FeatureCards = () => {
  const [ref, inView] = useInView({
    triggerOnce: true,
    threshold: 0.1,
  });

  return (
    <section ref={ref} className="relative py-32">
      <div className="section-container">
        <motion.div
          className="text-center mb-20"
          initial={{ opacity: 0, y: 30 }}
          animate={inView ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.8 }}
        >
          <h2 className="text-5xl md:text-6xl font-space font-bold mb-6">
            Powered by <span className="text-gradient">Cutting-Edge AI</span>
          </h2>
          <p className="text-xl text-space-gray max-w-3xl mx-auto">
            Three revolutionary technologies working together to transform how you experience video memories
          </p>
        </motion.div>

        <div className="grid md:grid-cols-3 gap-8">
          {features.map((feature, index) => (
            <FeatureCard key={index} feature={feature} index={index} />
          ))}
        </div>
      </div>
    </section>
  );
};

export default FeatureCards;
