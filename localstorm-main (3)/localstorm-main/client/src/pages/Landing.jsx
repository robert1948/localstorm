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
          <div className="flex justify-center">
            <img
              className="max-w-full h-auto"
              src="https://lightning-s3.s3.us-east-1.amazonaws.com/static/website/img/landing01.png"
              alt="Landing page showcase"
            />
          </div>
        </div>
      </div>
    </section>
  );
}
