export default function Hero() {
  return (
    <section className="text-center py-16 px-4 bg-gradient-to-b from-white to-blue-50">
      <h1 className="text-4xl sm:text-5xl font-extrabold text-blue-700 mb-6 leading-tight">
        Empower Your Business with AI Agents—
        <br className="hidden sm:inline" />
        <span className="text-blue-600">Fast, Affordable, and Simple.</span>
      </h1>

      <p className="text-gray-600 max-w-xl mx-auto mb-8 text-base sm:text-lg">
        Access a curated library of AI-driven tools to automate tasks, boost productivity,
        and grow your business—no coding required.
      </p>

      <div className="flex flex-col sm:flex-row justify-center gap-4 mb-10">
        <button className="bg-blue-600 text-white px-6 py-2 rounded hover:bg-blue-700">
          Try for Free
        </button>
        <button className="border border-blue-600 text-blue-600 px-6 py-2 rounded hover:bg-blue-50">
          See How It Works
        </button>
      </div>

      {/* Dashboard preview */}
      <div className="bg-white rounded-xl shadow-md mx-auto w-full max-w-4xl overflow-hidden mb-8">
        <img
          src="https://lightning-s3.s3.amazonaws.com/static/website/img/dashboard-preview.png"
          alt="CapeControl Dashboard Preview"
          className="w-full h-auto"
          loading="lazy"
        />
        <div className="py-2 text-sm text-gray-700 font-medium">Dashboard preview</div>
      </div>

      <div className="mt-8 text-gray-500 text-sm flex justify-center items-center gap-2">
        <span className="text-yellow-500">⭐</span>
        Trusted by 1,200+ freelancers and small businesses
      </div>

      <div className="mt-10 max-w-2xl mx-auto bg-white p-6 rounded-lg shadow-md text-gray-700 italic">
        <span className="text-blue-500 text-2xl">"</span>
        CapeControl helped us streamline our workflow in ways we didn't think possible.
        The AI tools feel like extra team members!
        <div className="mt-2 text-right text-sm font-medium">
          — Alex M., Founder of SmartEdge
        </div>
      </div>
    </section>
  );
}