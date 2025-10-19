import { useEffect, useRef, useState } from 'react';

const testimonials = [
  {
    name: 'Sarah Johnson',
    role: 'Family Memories Keeper',
    text: 'Finally, my grandmother in Mexico can understand our family videos in Spanish. The emotion in my voice comes through perfectly.',
    rating: 5,
    avatar: 'SJ',
  },
  {
    name: 'Miguel Rodriguez',
    role: 'Content Creator',
    text: 'This changed my streaming game. I can reach English audiences without losing my authentic voice. Incredible technology.',
    rating: 5,
    avatar: 'MR',
  },
  {
    name: 'Dr. Amara Okafor',
    role: 'Medical Educator',
    text: 'I use REWIND to make my medical training videos accessible in multiple African languages. The 3D exploration is revolutionary.',
    rating: 5,
    avatar: 'AO',
  },
  {
    name: 'Chen Wei',
    role: 'Wedding Videographer',
    text: 'My clients love that their wedding videos can be narrated in their families native languages. Bookings increased 40%.',
    rating: 5,
    avatar: 'CW',
  },
  {
    name: 'Emma Thompson',
    role: 'History Teacher',
    text: 'The AI scene detection helps me create interactive lessons. Students can explore historical footage in their own language.',
    rating: 5,
    avatar: 'ET',
  },
  {
    name: 'Raj Patel',
    role: 'Tech Enthusiast',
    text: 'The 3D navigation is mind-blowing. It is like stepping into your memories. The voice cloning quality is exceptional.',
    rating: 5,
    avatar: 'RP',
  },
];

const TestimonialCard = ({ testimonial, style }) => {
  return (
    <div
      className="glassmorphic rounded-2xl p-6 transition-all duration-300 hover:scale-105 hover:shadow-2xl"
      style={style}
    >
      <div className="flex items-center mb-4">
        <div className="w-12 h-12 rounded-full bg-gradient-to-br from-cosmic-purple to-nebula-blue flex items-center justify-center font-bold mr-3">
          {testimonial.avatar}
        </div>
        <div>
          <div className="font-semibold">{testimonial.name}</div>
          <div className="text-sm text-space-gray">{testimonial.role}</div>
        </div>
      </div>

      <div className="flex mb-3">
        {[...Array(testimonial.rating)].map((_, i) => (
          <svg
            key={i}
            className="w-5 h-5 text-yellow-400 fill-current"
            viewBox="0 0 20 20"
          >
            <path d="M10 15l-5.878 3.09 1.123-6.545L.489 6.91l6.572-.955L10 0l2.939 5.955 6.572.955-4.756 4.635 1.123 6.545z" />
          </svg>
        ))}
      </div>

      <p className="text-space-gray italic leading-relaxed">
        "{testimonial.text}"
      </p>
    </div>
  );
};

const SocialProof = () => {
  const [isVisible, setIsVisible] = useState(false);
  const sectionRef = useRef(null);

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            setIsVisible(true);
          }
        });
      },
      { threshold: 0.2 }
    );

    if (sectionRef.current) {
      observer.observe(sectionRef.current);
    }

    return () => observer.disconnect();
  }, []);

  return (
    <section ref={sectionRef} className="relative py-32">
      <div className="section-container">
        <div className="text-center mb-20">
          <h2 className="text-5xl md:text-6xl font-space font-bold mb-6">
            Trusted by <span className="text-gradient">Memory Makers</span> Worldwide
          </h2>

          <div className="grid grid-cols-3 gap-8 max-w-4xl mx-auto mt-12">
            <div className="glassmorphic rounded-xl p-6">
              <div className="text-4xl font-bold text-gradient mb-2">1,000+</div>
              <div className="text-space-gray">Videos Processed</div>
            </div>
            <div className="glassmorphic rounded-xl p-6">
              <div className="text-4xl font-bold text-gradient mb-2">29</div>
              <div className="text-space-gray">Languages Supported</div>
            </div>
            <div className="glassmorphic rounded-xl p-6">
              <div className="text-4xl font-bold text-gradient mb-2">500+</div>
              <div className="text-space-gray">Hours Saved</div>
            </div>
          </div>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {testimonials.map((testimonial, index) => (
            <div
              key={index}
              className={isVisible ? 'animate-fade-in' : 'opacity-0'}
              style={{
                animationDelay: `${index * 0.1}s`,
                animationFillMode: 'forwards',
              }}
            >
              <TestimonialCard testimonial={testimonial} />
            </div>
          ))}
        </div>

        <div className="mt-16 text-center">
          <p className="text-space-gray mb-4">Powered by cutting-edge AI</p>
          <div className="flex justify-center items-center gap-8 flex-wrap opacity-50 grayscale">
            <div className="text-xl font-bold">TwelveLabs</div>
            <div className="text-xl font-bold">Google Gemini</div>
            <div className="text-xl font-bold">ElevenLabs</div>
            <div className="text-xl font-bold">Firebase</div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default SocialProof;
