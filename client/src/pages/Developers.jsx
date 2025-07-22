import { Link } from "react-router-dom";

export default function Developers() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 to-blue-50 pt-20">
      <div className="max-w-6xl mx-auto px-4 py-16">
        {/* Header */}
        <div className="text-center mb-16">
          <h1 className="text-5xl font-bold text-gray-900 mb-6">
            CapeControl Developer Platform
          </h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Build, monetize, and scale AI-agents in our thriving developer ecosystem
          </p>
        </div>

        {/* Hero Section */}
        <section className="mb-16">
          <div className="bg-gradient-to-r from-purple-600 to-blue-600 text-white p-12 rounded-lg text-center">
            <h2 className="text-3xl font-bold mb-4">Developer Revenue Platform</h2>
            <p className="text-xl mb-8 opacity-90">
              CapeControl includes a built-in developer earnings system that tracks AI-agent performance, revenue sharing, and automated payouts. Create a thriving ecosystem where AI developers can monetize their innovations while clients access cutting-edge solutions.
            </p>
            <div className="grid md:grid-cols-3 gap-6 mt-8">
              <div className="bg-white/10 p-6 rounded-lg">
                <div className="text-3xl mb-2">💰</div>
                <h3 className="font-semibold mb-2">Revenue Sharing</h3>
                <p className="text-sm opacity-90">Earn 30% commission on every AI-agent interaction</p>
              </div>
              <div className="bg-white/10 p-6 rounded-lg">
                <div className="text-3xl mb-2">📊</div>
                <h3 className="font-semibold mb-2">Real-time Analytics</h3>
                <p className="text-sm opacity-90">Track performance, usage, and earnings in real-time</p>
              </div>
              <div className="bg-white/10 p-6 rounded-lg">
                <div className="text-3xl mb-2">🚀</div>
                <h3 className="font-semibold mb-2">Automated Payouts</h3>
                <p className="text-sm opacity-90">Receive payments automatically when thresholds are met</p>
              </div>
            </div>
          </div>
        </section>

        {/* Developer Features */}
        <section className="mb-16">
          <h2 className="text-3xl font-bold text-gray-900 mb-8 text-center">Everything You Need to Succeed</h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div className="bg-white p-6 rounded-lg shadow-md">
              <div className="text-3xl mb-4">🤖</div>
              <h3 className="text-xl font-semibold text-purple-600 mb-3">AI-Agent Development</h3>
              <p className="text-gray-700 mb-4">
                Build sophisticated AI-agents using our comprehensive SDK and development tools. Support for multiple AI models and frameworks.
              </p>
              <ul className="text-sm text-gray-600 space-y-1">
                <li>• Pre-built templates and examples</li>
                <li>• Multi-model AI integration</li>
                <li>• Testing and debugging tools</li>
              </ul>
            </div>

            <div className="bg-white p-6 rounded-lg shadow-md">
              <div className="text-3xl mb-4">💳</div>
              <h3 className="text-xl font-semibold text-purple-600 mb-3">Revenue Tracking</h3>
              <p className="text-gray-700 mb-4">
                Monitor your earnings in real-time with detailed analytics on agent performance, user engagement, and revenue trends.
              </p>
              <ul className="text-sm text-gray-600 space-y-1">
                <li>• Daily/monthly earning reports</li>
                <li>• Usage analytics and metrics</li>
                <li>• Performance optimization insights</li>
              </ul>
            </div>

            <div className="bg-white p-6 rounded-lg shadow-md">
              <div className="text-3xl mb-4">🏪</div>
              <h3 className="text-xl font-semibold text-purple-600 mb-3">Marketplace Integration</h3>
              <p className="text-gray-700 mb-4">
                List your AI-agents in our marketplace where customers can discover, trial, and purchase your solutions.
              </p>
              <ul className="text-sm text-gray-600 space-y-1">
                <li>• Featured agent showcases</li>
                <li>• Customer reviews and ratings</li>
                <li>• Promotional campaigns</li>
              </ul>
            </div>

            <div className="bg-white p-6 rounded-lg shadow-md">
              <div className="text-3xl mb-4">📈</div>
              <h3 className="text-xl font-semibold text-purple-600 mb-3">Advanced Analytics</h3>
              <p className="text-gray-700 mb-4">
                Deep insights into how your AI-agents are performing, including usage patterns, customer satisfaction, and optimization opportunities.
              </p>
              <ul className="text-sm text-gray-600 space-y-1">
                <li>• User engagement metrics</li>
                <li>• Performance benchmarking</li>
                <li>• A/B testing capabilities</li>
              </ul>
            </div>

            <div className="bg-white p-6 rounded-lg shadow-md">
              <div className="text-3xl mb-4">🔧</div>
              <h3 className="text-xl font-semibold text-purple-600 mb-3">Developer Tools</h3>
              <p className="text-gray-700 mb-4">
                Comprehensive development environment with APIs, SDKs, documentation, and support to accelerate your development process.
              </p>
              <ul className="text-sm text-gray-600 space-y-1">
                <li>• RESTful API access</li>
                <li>• SDK for multiple languages</li>
                <li>• Interactive documentation</li>
              </ul>
            </div>

            <div className="bg-white p-6 rounded-lg shadow-md">
              <div className="text-3xl mb-4">🤝</div>
              <h3 className="text-xl font-semibold text-purple-600 mb-3">Community Support</h3>
              <p className="text-gray-700 mb-4">
                Join a thriving community of AI developers, share knowledge, collaborate on projects, and get support from our team.
              </p>
              <ul className="text-sm text-gray-600 space-y-1">
                <li>• Developer forums and chat</li>
                <li>• Technical support tickets</li>
                <li>• Regular workshops and events</li>
              </ul>
            </div>
          </div>
        </section>

        {/* Revenue Model */}
        <section className="mb-16">
          <div className="bg-green-50 border border-green-200 p-8 rounded-lg">
            <h2 className="text-3xl font-bold text-green-800 mb-6">Revenue Model</h2>
            <div className="grid md:grid-cols-2 gap-8">
              <div>
                <h3 className="text-xl font-semibold text-green-700 mb-4">How You Earn</h3>
                <div className="space-y-4">
                  <div className="flex items-center space-x-3">
                    <div className="w-8 h-8 bg-green-500 text-white rounded-full flex items-center justify-center font-bold">1</div>
                    <p className="text-gray-700">Create and deploy your AI-agent</p>
                  </div>
                  <div className="flex items-center space-x-3">
                    <div className="w-8 h-8 bg-green-500 text-white rounded-full flex items-center justify-center font-bold">2</div>
                    <p className="text-gray-700">Customers discover and use your agent</p>
                  </div>
                  <div className="flex items-center space-x-3">
                    <div className="w-8 h-8 bg-green-500 text-white rounded-full flex items-center justify-center font-bold">3</div>
                    <p className="text-gray-700">Earn 30% commission on every interaction</p>
                  </div>
                  <div className="flex items-center space-x-3">
                    <div className="w-8 h-8 bg-green-500 text-white rounded-full flex items-center justify-center font-bold">4</div>
                    <p className="text-gray-700">Receive automated payouts monthly</p>
                  </div>
                </div>
              </div>
              <div>
                <h3 className="text-xl font-semibold text-green-700 mb-4">Earning Potential</h3>
                <div className="bg-white p-6 rounded-lg shadow-sm">
                  <div className="text-3xl font-bold text-green-600 mb-2">$5,000+</div>
                  <p className="text-gray-600 mb-4">Average monthly earnings for top developers</p>
                  
                  <div className="space-y-3">
                    <div className="flex justify-between">
                      <span className="text-gray-600">100 daily users</span>
                      <span className="font-semibold">$900/month</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">500 daily users</span>
                      <span className="font-semibold">$4,500/month</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">1000+ daily users</span>
                      <span className="font-semibold">$9,000+/month</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* API Documentation Preview */}
        <section className="mb-16">
          <h2 className="text-3xl font-bold text-gray-900 mb-8 text-center">Developer API</h2>
          <div className="bg-gray-900 text-white p-8 rounded-lg">
            <div className="grid md:grid-cols-2 gap-8">
              <div>
                <h3 className="text-xl font-semibold text-green-400 mb-4">Developer Earnings API</h3>
                <div className="bg-black/50 p-4 rounded font-mono text-sm">
                  <div className="text-blue-300">GET /api/enhanced/developer/earnings</div>
                  <div className="text-gray-400 mt-2">// Get earnings summary</div>
                  <div className="text-gray-400">// Revenue share tracking</div>
                  <div className="text-gray-400">// Payout history</div>
                </div>
              </div>
              <div>
                <h3 className="text-xl font-semibold text-green-400 mb-4">Agent Management</h3>
                <div className="bg-black/50 p-4 rounded font-mono text-sm">
                  <div className="text-blue-300">POST /api/enhanced/developer/agents</div>
                  <div className="text-blue-300">GET /api/enhanced/analytics</div>
                  <div className="text-gray-400 mt-2">// Deploy new agents</div>
                  <div className="text-gray-400">// Performance metrics</div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Getting Started */}
        <section className="text-center">
          <div className="bg-purple-600 text-white p-12 rounded-lg">
            <h2 className="text-3xl font-bold mb-4">Start Building Today</h2>
            <p className="text-xl mb-8 opacity-90">
              Join our developer program and start earning from your AI innovations.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link
                to="/register"
                className="bg-white text-purple-600 hover:bg-gray-100 py-3 px-8 rounded-lg font-semibold transition-colors"
              >
                Register as Developer
              </Link>
              <Link
                to="/docs"
                className="border-2 border-white text-white hover:bg-white hover:text-purple-600 py-3 px-8 rounded-lg font-semibold transition-colors"
              >
                View Documentation
              </Link>
            </div>
            <p className="text-sm mt-6 opacity-75">
              Free to join • No setup fees • 30% revenue share • Automated payouts
            </p>
          </div>
        </section>
      </div>
    </div>
  );
}
