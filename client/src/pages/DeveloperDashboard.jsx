import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

export default function DeveloperDashboard() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const token = localStorage.getItem("token");
        if (!token) {
          navigate("/login");
          return;
        }

        const response = await fetch("/api/user/profile", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (response.ok) {
          const userData = await response.json();
          setUser(userData);
        } else {
          navigate("/login");
        }
      } catch (error) {
        console.error("Error fetching user data:", error);
        navigate("/login");
      } finally {
        setLoading(false);
      }
    };

    fetchUserData();
  }, [navigate]);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading your dashboard...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 pt-24">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Welcome Header */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-8">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">
                Developer Dashboard
              </h1>
              <p className="text-gray-600 mt-1">
                Welcome, {user?.firstName || "Developer"}! Build and monetize your AI agents.
              </p>
            </div>
            <div className="text-right">
              <div className="text-sm text-gray-500">Revenue this month</div>
              <div className="font-semibold text-2xl text-green-600">$0.00</div>
            </div>
          </div>
        </div>

        {/* Developer Stats */}
        <div className="grid md:grid-cols-4 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="text-blue-600 text-2xl mb-2">⚡</div>
            <div className="text-3xl font-bold">0</div>
            <div className="text-sm text-gray-600">Published Agents</div>
          </div>

          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="text-green-600 text-2xl mb-2">💰</div>
            <div className="text-3xl font-bold">$0</div>
            <div className="text-sm text-gray-600">Total Revenue</div>
          </div>

          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="text-purple-600 text-2xl mb-2">📈</div>
            <div className="text-3xl font-bold">0</div>
            <div className="text-sm text-gray-600">Active Users</div>
          </div>

          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="text-orange-600 text-2xl mb-2">⭐</div>
            <div className="text-3xl font-bold">-</div>
            <div className="text-sm text-gray-600">Avg Rating</div>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="grid md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow cursor-pointer">
            <div className="text-blue-600 text-3xl mb-4">🛠️</div>
            <h3 className="text-xl font-semibold mb-2">Create New Agent</h3>
            <p className="text-gray-600 text-sm">
              Build a new AI agent using our developer tools and templates.
            </p>
          </div>

          <div className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow cursor-pointer">
            <div className="text-green-600 text-3xl mb-4">📚</div>
            <h3 className="text-xl font-semibold mb-2">Documentation</h3>
            <p className="text-gray-600 text-sm">
              Access comprehensive guides and API documentation.
            </p>
          </div>

          <div className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow cursor-pointer">
            <div className="text-purple-600 text-3xl mb-4">🏪</div>
            <h3 className="text-xl font-semibold mb-2">Marketplace</h3>
            <p className="text-gray-600 text-sm">
              Publish and manage your agents in the marketplace.
            </p>
          </div>
        </div>

        {/* Getting Started */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-2xl font-bold mb-4">Getting Started</h2>
          <div className="space-y-4">
            <div className="flex items-center space-x-4 p-4 bg-blue-50 rounded-lg border-l-4 border-blue-500">
              <div className="text-blue-600 text-2xl">📋</div>
              <div>
                <div className="font-semibold">Complete Your Developer Profile</div>
                <div className="text-sm text-gray-600">
                  Add your portfolio, skills, and payment information to start earning.
                </div>
              </div>
              <button className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 ml-auto">
                Complete Profile
              </button>
            </div>

            <div className="flex items-center space-x-4 p-4 bg-gray-50 rounded-lg">
              <div className="text-gray-400 text-2xl">🚀</div>
              <div>
                <div className="font-semibold text-gray-500">Create Your First Agent</div>
                <div className="text-sm text-gray-400">
                  Use our SDK and templates to build your first AI agent.
                </div>
              </div>
              <button className="bg-gray-300 text-gray-500 px-4 py-2 rounded-lg cursor-not-allowed ml-auto">
                Coming Soon
              </button>
            </div>

            <div className="flex items-center space-x-4 p-4 bg-gray-50 rounded-lg">
              <div className="text-gray-400 text-2xl">💳</div>
              <div>
                <div className="font-semibold text-gray-500">Setup Payment Method</div>
                <div className="text-sm text-gray-400">
                  Configure how you'll receive payments from agent sales.
                </div>
              </div>
              <button className="bg-gray-300 text-gray-500 px-4 py-2 rounded-lg cursor-not-allowed ml-auto">
                Coming Soon
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
