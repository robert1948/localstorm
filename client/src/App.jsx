import { Routes, Route } from "react-router-dom";
import { Suspense, lazy } from "react";
import Navbar from "./components/Navbar";

// ✅ Lazy-loaded pages
const Landing = lazy(() => import("./pages/Landing"));
const Login = lazy(() => import("./pages/Login"));
const Register = lazy(() => import("./pages/Register"));
const Dashboard = lazy(() => import("./pages/Dashboard"));
const UserDashboard = lazy(() => import("./pages/UserDashboard"));
const DeveloperDashboard = lazy(() => import("./pages/DeveloperDashboard"));
const Logout = lazy(() => import("./pages/Logout"));
const HowItWorks = lazy(() => import("./pages/HowItWorks"));
const HowItWorksUser = lazy(() => import("./pages/HowItWorksUser"));
const HowItWorksDeveloper = lazy(() => import("./pages/HowItWorksDeveloper"));
const ProtectedRoute = lazy(() => import("./components/ProtectedRoute"));

export default function App() {
  return (
    <div className="min-h-screen bg-gray-100 text-gray-900">
      <Navbar />
      <Suspense fallback={<div className="p-4 text-center">Loading...</div>}>
        <Routes>
          <Route path="/" element={<Landing />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/logout" element={<Logout />} />
          <Route path="/how-it-works" element={<HowItWorks />} />
          <Route path="/how-it-works-user" element={<HowItWorksUser />} />
          <Route path="/how-it-works-developer" element={<HowItWorksDeveloper />} />
          <Route
            path="/dashboard"
            element={
              <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            }
          />
          <Route
            path="/dashboard/user"
            element={
              <ProtectedRoute>
                <UserDashboard />
              </ProtectedRoute>
            }
          />
          <Route
            path="/dashboard/developer"
            element={
              <ProtectedRoute>
                <DeveloperDashboard />
              </ProtectedRoute>
            }
          />
        </Routes>
      </Suspense>
    </div>
  );
}
