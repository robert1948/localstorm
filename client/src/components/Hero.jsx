import { useNavigate } from 'react-router-dom';

export default function Hero() {
  const navigate = useNavigate();

  const handleSeeHowItWorks = () => {
    navigate('/how-it-works');
  };

  const handleTryForFree = () => {
    navigate('/register');
  };

  return (
    <section className="pt-24 pb-16 px-4 bg-gradient-to-b from-white to-blue-50 text-center min-h-screen flex flex-col justify-center">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-2xl sm:text-3xl md:text-4xl lg:text-5xl font-extrabold text-blue-700 mb-6 leading-tight px-2">
          Where Intelligence Meets Impact—
          <br className="hidden sm:inline" />
          <span className="text-blue-600">AI Accessible to Everyone.</span>
        </h1>

        <p className="text-gray-600 max-w-2xl mx-auto mb-8 text-base sm:text-lg md:text-xl px-4 leading-relaxed">
          Democratizing artificial intelligence through our platform that bridges human ambition and technological possibility. 
          Access cutting-edge AI-agents while empowering developers to innovate and earn.
        </p>

        <div className="flex flex-col sm:flex-row justify-center gap-4 mb-12 px-4">
          <button 
            onClick={handleTryForFree}
            className="bg-blue-600 text-white px-8 py-4 rounded-lg hover:bg-blue-700 transition-colors text-lg font-semibold"
          >
            Get Started Free
          </button>
          <button 
            onClick={() => navigate('/developers')}
            className="bg-purple-600 text-white px-8 py-4 rounded-lg hover:bg-purple-700 transition-colors text-lg font-semibold"
          >
            Join as Developer
          </button>
          <button 
            onClick={handleSeeHowItWorks}
            className="border border-blue-600 text-blue-600 px-8 py-4 rounded-lg hover:bg-blue-50 transition-colors text-lg font-semibold"
          >
            See How It Works
          </button>
        </div>

        {/* Hero visual - hide on mobile, show on tablet and up */}
        <div className="hidden md:block bg-white rounded-xl shadow-lg mx-auto w-full max-w-3xl overflow-hidden mb-8">
          {/* Clean, minimalist AI representation */}
          <div className="bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50 p-16 text-center relative overflow-hidden">
            {/* Background pattern */}
            <div className="absolute inset-0 opacity-5">
              <div className="absolute top-4 left-4 w-2 h-2 bg-blue-400 rounded-full"></div>
              <div className="absolute top-8 right-12 w-1 h-1 bg-purple-400 rounded-full"></div>
              <div className="absolute bottom-6 left-8 w-1.5 h-1.5 bg-indigo-400 rounded-full"></div>
              <div className="absolute bottom-12 right-6 w-2 h-2 bg-blue-400 rounded-full"></div>
              <div className="absolute top-1/3 left-1/4 w-1 h-1 bg-purple-400 rounded-full"></div>
              <div className="absolute top-2/3 right-1/3 w-1.5 h-1.5 bg-indigo-400 rounded-full"></div>
            </div>
            
            {/* Main content */}
            <div className="relative z-10">
              <div className="text-6xl mb-6 text-blue-600">🤖</div>
              <h3 className="text-2xl font-bold text-gray-800 mb-3">AI That Understands</h3>
              <p className="text-gray-600 max-w-lg mx-auto text-sm leading-relaxed">
                Experience the future of artificial intelligence—context-aware, adaptive, and designed to amplify human potential across every industry.
              </p>
              
              {/* Feature highlights */}
              <div className="mt-8 grid grid-cols-3 gap-6 max-w-md mx-auto">
                <div className="text-center">
                  <div className="w-8 h-8 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center mx-auto mb-2 text-sm">⚡</div>
                  <div className="text-xs font-medium text-gray-700">Fast</div>
                </div>
                <div className="text-center">
                  <div className="w-8 h-8 bg-purple-100 text-purple-600 rounded-full flex items-center justify-center mx-auto mb-2 text-sm">🎯</div>
                  <div className="text-xs font-medium text-gray-700">Precise</div>
                </div>
                <div className="text-center">
                  <div className="w-8 h-8 bg-green-100 text-green-600 rounded-full flex items-center justify-center mx-auto mb-2 text-sm">🌐</div>
                  <div className="text-xs font-medium text-gray-700">Global</div>
                </div>
              </div>
            </div>
          </div>
          <div className="py-3 text-sm text-gray-700 font-medium bg-gray-50 text-center">
            Platform Preview • Where Intelligence Meets Impact
          </div>
        </div>

        {/* Mobile-friendly feature cards */}
        <div className="md:hidden grid grid-cols-1 gap-4 mb-8 px-4">
          <div className="bg-white p-6 rounded-lg shadow-md">
            <div className="text-blue-600 font-semibold mb-2 text-lg">🤖 AI That Evolves</div>
            <div className="text-sm text-gray-600">
              Experience AI-agents that understand context, anticipate needs, and continuously learn from interactions.
            </div>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-md">
            <div className="text-purple-600 font-semibold mb-2 text-lg">💰 Developer Ecosystem</div>
            <div className="text-sm text-gray-600">
              Build innovative AI-agents and earn 30% revenue share through our thriving developer platform.
            </div>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-md">
            <div className="text-green-600 font-semibold mb-2 text-lg">🌍 Global Impact</div>
            <div className="text-sm text-gray-600">
              Join a platform designed to address diverse challenges across industries, geographies, and use cases.
            </div>
          </div>
        </div>

        {/* Trust indicator */}
        <div className="mt-8 text-gray-500 text-sm sm:text-base flex justify-center items-center gap-2 px-4">
          <span className="text-yellow-500">⭐</span>
          <span className="text-center">Empowering developers and businesses across industries worldwide</span>
        </div>

        {/* Testimonial */}
        <div className="mt-8 max-w-2xl mx-auto bg-white p-6 rounded-lg shadow-md text-gray-700 italic mx-4">
          <span className="text-blue-500 text-2xl">"</span>
          <div className="text-base sm:text-lg leading-relaxed">
            CapeControl is more than a service—it's a showcase of what AI can achieve. 
            The platform's intelligence and responsiveness demonstrate the transformative potential of AI.
          </div>
          <div className="mt-3 text-right text-sm font-medium">
            — From our Vision Statement
          </div>
        </div>

        {/* Vision tagline */}
        <div className="mt-8 text-center">
          <p className="text-lg font-medium text-blue-700">
            "Where intelligence meets impact, and possibilities become realities."
          </p>
        </div>

        {/* Dual audience section */}
        <div className="hidden md:block mt-16 grid md:grid-cols-2 gap-8 px-4">
          <div className="bg-gradient-to-br from-blue-50 to-blue-100 p-8 rounded-lg text-left">
            <div className="text-3xl mb-4">🚀</div>
            <h3 className="text-xl font-bold text-blue-700 mb-3">For Businesses & Individuals</h3>
            <p className="text-gray-700 mb-4">
              Transform your operations with AI-agents that understand context, anticipate needs, and deliver personalized solutions—no technical expertise required.
            </p>
            <ul className="text-sm text-gray-600 space-y-2 mb-4">
              <li>• Streamline operations and boost productivity</li>
              <li>• Access cutting-edge AI without complexity</li>
              <li>• Scale from startups to enterprises</li>
              <li>• Global solutions with local relevance</li>
            </ul>
            <button 
              onClick={handleTryForFree}
              className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors"
            >
              Start Your Journey
            </button>
          </div>

          <div className="bg-gradient-to-br from-purple-50 to-purple-100 p-8 rounded-lg text-left">
            <div className="text-3xl mb-4">💡</div>
            <h3 className="text-xl font-bold text-purple-700 mb-3">For AI Developers</h3>
            <p className="text-gray-700 mb-4">
              Build innovative AI-agents, earn passive income through revenue sharing, and contribute to a platform that showcases AI excellence.
            </p>
            <ul className="text-sm text-gray-600 space-y-2 mb-4">
              <li>• Earn 30% revenue share from your agents</li>
              <li>• Access comprehensive developer tools</li>
              <li>• Join a thriving developer community</li>
              <li>• Real-time earnings and analytics</li>
            </ul>
            <button 
              onClick={() => navigate('/developers')}
              className="bg-purple-600 text-white px-6 py-2 rounded-lg hover:bg-purple-700 transition-colors"
            >
              Join Developer Program
            </button>
          </div>
        </div>
      </div>
    </section>
  );
}