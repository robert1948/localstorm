import { Routes, Route } from "react-router-dom";
import { Suspense, lazy } from "react";
import Navbar from "./components/Navbar";
import { AuthProvider } from "./context/AuthContext";

// ✅ Lazy-loaded pages
const Landing = lazy(() => import("./pages/Landing"));
const Login = lazy(() => import("./pages/Login"));
const Register = lazy(() => import("./pages/RegisterV2"));
const RegisterLegacy = lazy(() => import("./pages/Register"));
const Phase2CustomerRegistration = lazy(() => import("./pages/Phase2CustomerRegistration"));
const Phase2DeveloperRegistration = lazy(() => import("./pages/Phase2DeveloperRegistration"));
const LoginCustomer = lazy(() => import("./pages/LoginCustomer"));
const LoginDeveloper = lazy(() => import("./pages/LoginDeveloper"));
const Dashboard = lazy(() => import("./pages/Dashboard"));
const UserDashboard = lazy(() => import("./pages/UserDashboard"));
const DeveloperDashboard = lazy(() => import("./pages/DeveloperDashboard"));
const Logout = lazy(() => import("./pages/Logout"));
const HowItWorks = lazy(() => import("./pages/HowItWorks"));
const HowItWorksUser = lazy(() => import("./pages/HowItWorksUser"));
const HowItWorksDeveloper = lazy(() => import("./pages/HowItWorksDeveloper"));
const Vision = lazy(() => import("./pages/Vision"));
const Platform = lazy(() => import("./pages/Platform"));
const Developers = lazy(() => import("./pages/Developers"));
const ProtectedRoute = lazy(() => import("./components/ProtectedRoute"));

export default function App() {
  return (
    <AuthProvider>
      <div className="min-h-screen bg-gray-100 text-gray-900">
        <Navbar />
        <Suspense fallback={<div className="p-4 text-center">Loading...</div>}>
          <Routes>
            <Route path="/" element={<Landing />} />
            <Route path="/vision" element={<Vision />} />
            <Route path="/platform" element={<Platform />} />
            <Route path="/developers" element={<Developers />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route path="/register-legacy" element={<RegisterLegacy />} />
            <Route path="/phase2-customer" element={<Phase2CustomerRegistration />} />
            <Route path="/phase2-developer" element={<Phase2DeveloperRegistration />} />
            <Route path="/login-customer" element={<LoginCustomer />} />
            <Route path="/login-developer" element={<LoginDeveloper />} />
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
    </AuthProvider>
  );
}
