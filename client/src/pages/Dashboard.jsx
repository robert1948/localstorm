import { useEffect, useState } from "react";
import axios from "axios";
import OnboardingChecklist from "../components/onboarding/OnboardingChecklist";
import useOnboarding from "../hooks/useOnboarding";

function Dashboard() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const { isComplete, progress } = useOnboarding();

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      setError("");

      try {
        const response = await axios.get("/api/me");
        setData(response.data);
      } catch (err) {
        setError("Failed to load user data.");
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  return (
    <div className="max-w-4xl mx-auto mt-20 p-6">
      <div className="mb-8">
        <h2 className="text-3xl font-bold mb-4">Welcome to Your Dashboard</h2>
        
        {!isComplete && (
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
            <div className="flex items-center justify-between mb-2">
              <h3 className="text-lg font-semibold text-blue-800">Getting Started</h3>
              <span className="text-sm text-blue-600 font-medium">
                {progress.percentage}% Complete
              </span>
            </div>
            <p className="text-blue-700 text-sm">
              Complete your onboarding to unlock the full potential of CapeControl
            </p>
          </div>
        )}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <div className="bg-white border rounded-xl shadow p-6">
            <h3 className="text-xl font-bold mb-4">User Information</h3>

            {loading && <p className="text-blue-500">Loading...</p>}
            {error && <p className="text-red-500">{error}</p>}

            {data && (
              <div className="space-y-3">
                <div className="flex justify-between py-2 border-b">
                  <span className="font-medium text-gray-600">Name:</span>
                  <span className="text-gray-800">{data.name}</span>
                </div>
                <div className="flex justify-between py-2 border-b">
                  <span className="font-medium text-gray-600">Email:</span>
                  <span className="text-gray-800">{data.email}</span>
                </div>
                <div className="flex justify-between py-2">
                  <span className="font-medium text-gray-600">Status:</span>
                  <span className="text-green-600 font-medium">Active</span>
                </div>
              </div>
            )}
          </div>

          {/* Quick Actions */}
          <div className="bg-white border rounded-xl shadow p-6 mt-6">
            <h3 className="text-xl font-bold mb-4">Quick Actions</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <button className="bg-blue-600 text-white p-4 rounded-lg hover:bg-blue-700 transition-colors">
                🚀 Launch New Agent
              </button>
              <button className="bg-green-600 text-white p-4 rounded-lg hover:bg-green-700 transition-colors">
                📊 View Analytics
              </button>
              <button className="bg-purple-600 text-white p-4 rounded-lg hover:bg-purple-700 transition-colors">
                ⚙️ Manage Settings
              </button>
              <button className="bg-orange-600 text-white p-4 rounded-lg hover:bg-orange-700 transition-colors">
                💬 Get Support
              </button>
            </div>
          </div>
        </div>

        <div className="lg:col-span-1">
          {/* Onboarding Checklist */}
          {!isComplete && <OnboardingChecklist />}
          
          {/* Recent Activity */}
          <div className="bg-white border rounded-xl shadow p-6 mt-6">
            <h3 className="text-lg font-semibold mb-4">Recent Activity</h3>
            <div className="space-y-3 text-sm">
              <div className="flex items-center gap-2 text-gray-600">
                <span className="w-2 h-2 bg-green-400 rounded-full"></span>
                Account created successfully
              </div>
              <div className="flex items-center gap-2 text-gray-600">
                <span className="w-2 h-2 bg-blue-400 rounded-full"></span>
                Dashboard accessed
              </div>
              <div className="flex items-center gap-2 text-gray-600">
                <span className="w-2 h-2 bg-purple-400 rounded-full"></span>
                CapeAI assistant activated
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
