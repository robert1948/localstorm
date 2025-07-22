import { Routes, Route } from "react-router-dom";
import { Suspense, lazy } from "react";
import Navbar from "./components/Navbar";

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
    <div className="min-h-screen flex flex-col font-sans bg-white text-gray-900 dark:bg-gray-900 dark:text-white">
      <Navbar />
      <main className="flex-1 pt-20">
          <Suspense
            fallback={
              <div className="flex items-center justify-center min-h-[50vh]" role="status">
                <div className="text-center">
                  <div className="animate-spin rounded-full h-8 w-8 border-4 border-blue-500 border-t-transparent mx-auto"></div>
                  <p className="mt-2 text-sm text-gray-600 dark:text-gray-400">Loading...</p>
                </div>
              </div>
            }
          >
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
              <Route
                path="*"
                element={
                  <div className="p-4 text-center text-red-600">
                    404 - Page Not Found
                  </div>
                }
              />
            </Routes>
          </Suspense>
        </main>
      </div>
  );
}
