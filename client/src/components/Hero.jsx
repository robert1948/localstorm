export default function Hero() {
  return (
    <section className="pt-20 pb-16 px-4 bg-gradient-to-b from-white to-blue-50 text-center min-h-screen flex flex-col justify-center">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-2xl sm:text-3xl md:text-4xl lg:text-5xl font-extrabold text-blue-700 mb-6 leading-tight px-2">
          Empower Your Business with AI Agents—
          <br className="hidden sm:inline" />
          <span className="text-blue-600">Fast, Affordable, and Simple.</span>
        </h1>

        <p className="text-gray-600 max-w-2xl mx-auto mb-8 text-base sm:text-lg md:text-xl px-4 leading-relaxed">
          Access a curated library of AI-driven tools to automate tasks, boost productivity,
          and grow your business—no coding required.
        </p>

        <div className="flex flex-col sm:flex-row justify-center gap-4 mb-12 px-4">
          <button className="bg-blue-600 text-white px-8 py-4 rounded-lg hover:bg-blue-700 transition-colors text-lg font-semibold">
            Try for Free
          </button>
          <button className="border border-blue-600 text-blue-600 px-8 py-4 rounded-lg hover:bg-blue-50 transition-colors text-lg font-semibold">
            See How It Works
          </button>
        </div>

        {/* Dashboard preview - hide on mobile, show on tablet and up */}
        <div className="hidden md:block bg-white rounded-xl shadow-lg mx-auto w-full max-w-3xl overflow-hidden mb-8">
          <img
            src="https://lightning-s3.s3.amazonaws.com/static/website/img/dashboard-preview.png"
            alt="CapeControl Dashboard Preview"
            className="w-full h-auto"
            loading="lazy"
          />
          <div className="py-3 text-sm text-gray-700 font-medium">Dashboard preview</div>
        </div>

        {/* Mobile-friendly feature cards */}
        <div className="md:hidden grid grid-cols-1 gap-4 mb-8 px-4">
          <div className="bg-white p-6 rounded-lg shadow-md">
            <div className="text-blue-600 font-semibold mb-2 text-lg">⚡ Powerful Dashboard</div>
            <div className="text-sm text-gray-600">
              Access your AI agent control center with an intuitive interface designed for speed and simplicity.
            </div>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-md">
            <div className="text-blue-600 font-semibold mb-2 text-lg">🤖 AI-Powered Tools</div>
            <div className="text-sm text-gray-600">
              Leverage cutting-edge AI to automate tasks and boost your productivity effortlessly.
            </div>
          </div>
        </div>

        {/* Trust indicator */}
        <div className="mt-8 text-gray-500 text-sm sm:text-base flex justify-center items-center gap-2 px-4">
          <span className="text-yellow-500">⭐</span>
          <span className="text-center">Trusted by 1,200+ freelancers and small businesses</span>
        </div>

        {/* Testimonial */}
        <div className="mt-8 max-w-2xl mx-auto bg-white p-6 rounded-lg shadow-md text-gray-700 italic mx-4">
          <span className="text-blue-500 text-2xl">"</span>
          <div className="text-base sm:text-lg leading-relaxed">
            CapeControl helped us streamline our workflow in ways we didn't think possible.
            The AI tools feel like extra team members!
          </div>
          <div className="mt-3 text-right text-sm font-medium">
            — Alex M., Founder of SmartEdge
          </div>
        </div>
      </div>
    </section>
  );
}