export default function Hero() {
  return (
    <section className="pt-20 pb-16 px-4 bg-gradient-to-b from-white to-blue-50 text-center">
      <h1 className="text-3xl sm:text-4xl md:text-5xl font-extrabold text-blue-700 mb-6 leading-tight px-2">
        Empower Your Business with AI Agents—
        <br className="hidden sm:inline" />
        <span className="text-blue-600">Fast, Affordable, and Simple.</span>
      </h1>

      <p className="text-gray-600 max-w-xl mx-auto mb-8 text-sm sm:text-base md:text-lg px-4">
        Access a curated library of AI-driven tools to automate tasks, boost productivity,
        and grow your business—no coding required.
      </p>

      <div className="flex flex-col sm:flex-row justify-center gap-4 mb-10 px-4">
        <button className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-colors">
          Try for Free
        </button>
        <button className="border border-blue-600 text-blue-600 px-6 py-3 rounded-lg hover:bg-blue-50 transition-colors">
          See How It Works
        </button>
      </div>

      {/* Dashboard preview - hide on mobile to reduce clutter */}
      <div className="hidden sm:block bg-white rounded-xl shadow-md mx-auto w-full max-w-4xl overflow-hidden mb-8">
        <img
          src="https://lightning-s3.s3.amazonaws.com/static/website/img/dashboard-preview.png"
          alt="CapeControl Dashboard Preview"
          className="w-full h-auto"
          loading="lazy"
        />
        <div className="py-2 text-sm text-gray-700 font-medium">Dashboard preview</div>
      </div>

      {/* Mobile-specific message */}
      <div className="sm:hidden mb-8 p-4 bg-blue-50 rounded-lg mx-4">
        <div className="text-blue-600 font-semibold mb-2">⚡ Powerful Dashboard</div>
        <div className="text-sm text-gray-600">
          Access your AI agent control center with an intuitive interface designed for speed and simplicity.
        </div>
      </div>

      <div className="mt-8 text-gray-500 text-xs sm:text-sm flex justify-center items-center gap-2 px-4">
        <span className="text-yellow-500">⭐</span>
        <span className="text-center">Trusted by 1,200+ freelancers and small businesses</span>
      </div>

      <div className="mt-10 max-w-2xl mx-auto bg-white p-4 sm:p-6 rounded-lg shadow-md text-gray-700 italic mx-4">
        <span className="text-blue-500 text-xl sm:text-2xl">"</span>
        <div className="text-sm sm:text-base">
          CapeControl helped us streamline our workflow in ways we didn't think possible.
          The AI tools feel like extra team members!
        </div>
        <div className="mt-2 text-right text-xs sm:text-sm font-medium">
          — Alex M., Founder of SmartEdge
        </div>
      </div>
    </section>
  );
}