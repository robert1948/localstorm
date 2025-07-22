// Minimal Landing page without any hooks
export default function Landing() {
  return (
    <section className="min-h-screen bg-gradient-to-b from-white to-blue-50 flex flex-col">
      <div className="flex-1 flex flex-col justify-center px-4 pt-20 pb-8 sm:pt-24 lg:pt-32 lg:pb-16">
        <div className="max-w-5xl mx-auto w-full">
          
          {/* Main heading */}
          <div className="text-center mb-8 lg:mb-12">
            <h1 className="text-3xl sm:text-4xl md:text-5xl lg:text-6xl font-extrabold text-blue-700 leading-tight mb-6">
              Where Intelligence Meets Impact—
              <br className="hidden sm:block" />
              <span className="text-blue-600">AI Accessible to Everyone.</span>
            </h1>

            <p className="text-gray-600 text-base sm:text-lg lg:text-xl leading-relaxed max-w-3xl mx-auto px-2">
              Democratizing artificial intelligence through our platform that bridges human ambition and technological possibility.
            </p>
          </div>

          {/* Action buttons */}
          <div className="mb-12 lg:mb-16 space-y-4 sm:space-y-0 sm:flex sm:flex-wrap sm:justify-center sm:gap-4 lg:gap-6">
            <a 
              href="/how-it-works"
              className="block w-full sm:w-auto bg-blue-600 text-white px-8 py-4 rounded-lg hover:bg-blue-700 transition-colors text-lg font-semibold shadow-lg text-center"
            >
              Get Started Free
            </a>
            <a 
              href="/developers"
              className="block w-full sm:w-auto bg-purple-600 text-white px-8 py-4 rounded-lg hover:bg-purple-700 transition-colors text-lg font-semibold shadow-lg text-center"
            >
              Join as Developer
            </a>
            <a 
              href="/how-it-works"
              className="block w-full sm:w-auto border-2 border-blue-600 text-blue-600 px-8 py-4 rounded-lg hover:bg-blue-50 transition-colors text-lg font-semibold text-center"
            >
              See How It Works
            </a>
          </div>

          {/* Logo showcase */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 lg:gap-16">
            
            {/* Landing Image */}
            <div className="bg-gray-800 rounded-2xl shadow-xl p-8 mx-2 flex items-center justify-center">
              <img 
                src="https://lightning-s3.s3.us-east-1.amazonaws.com/static/website/img/landing01.png" 
                alt="CapeControl Landing" 
                className="w-full h-auto rounded-lg"
              />
            </div>

            {/* Business section */}
            <div className="bg-white rounded-2xl shadow-xl p-8 mx-2">
              <div className="text-center">
                <h3 className="text-2xl font-bold text-gray-800 mb-4">Business Growth</h3>
                <p className="text-gray-600 mb-6">
                  Transform your business operations with intelligent AI agents designed for efficiency and scale.
                </p>
                <div className="space-y-2">
                  <div className="flex items-center justify-center text-green-600">
                    <span className="mr-2">✓</span>
                    <span>Automated workflows</span>
                  </div>
                  <div className="flex items-center justify-center text-green-600">
                    <span className="mr-2">✓</span>
                    <span>Smart decision making</span>
                  </div>
                  <div className="flex items-center justify-center text-green-600">
                    <span className="mr-2">✓</span>
                    <span>24/7 availability</span>
                  </div>
                </div>
              </div>
            </div>

          </div>
        </div>
      </div>
    </section>
  );
}
