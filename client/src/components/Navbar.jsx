import { useState } from "react";
import { Link } from "react-router-dom";
import useAuth from "../hooks/useAuth";

export function Navbar() {
  const [menuOpen, setMenuOpen] = useState(false);
  const { user, isAuthenticated, logout, isLoading } = useAuth();

  const handleLogout = () => {
    logout();
    setMenuOpen(false);
  };

  if (isLoading) {
    return (
      <nav className="fixed top-0 left-0 right-0 h-16 sm:h-20 bg-blue-600 dark:bg-gray-900 text-white shadow-lg z-50" role="navigation" aria-label="Main navigation">
        <div className="container-mobile">
          <div className="flex justify-between items-center h-16 sm:h-20">
            <div data-testid="nav-loading" className="text-white">Loading...</div>
          </div>
        </div>
      </nav>
    );
  }

  return (
    <nav className="fixed top-0 left-0 right-0 h-16 sm:h-20 bg-blue-600 dark:bg-gray-900 text-white shadow-lg z-50" role="navigation" aria-label="Main navigation">
      <div className="container-mobile">
        <div className="flex justify-between items-center h-16 sm:h-20">
          {/* Logo + Brand */}
          <Link to="/" className="flex items-center space-x-2 py-2 active:scale-95 transition-transform">
            <img
              src="https://lightning-s3.s3.us-east-1.amazonaws.com/static/website/img/LogoW.png"
              alt="LocalStorm Logo"
              className="h-8 w-8 sm:h-10 sm:w-10"
            />
            <span className="text-lg sm:text-2xl font-bold">LocalStorm</span>
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden lg:flex space-x-2 xl:space-x-6 items-center">
            <Link to="/" className="btn-mobile text-white hover:bg-blue-700 font-medium">
              Home
            </Link>
            <Link to="/about" className="btn-mobile text-white hover:bg-blue-700 font-medium">
              About
            </Link>

            {/* Authentication Links */}
            {isAuthenticated ? (
              <div className="flex items-center space-x-4">
                <span className="text-white" aria-label={`Logged in as ${user?.name || user?.email}`}>
                  {user?.name || user?.email}
                </span>
                <Link to="/dashboard" className="btn-mobile text-white hover:bg-blue-700 font-medium">
                  Dashboard
                </Link>
                <Link to="/dashboard/personalized" className="btn-mobile text-white hover:bg-blue-700 font-medium">
                  Personalized
                </Link>
                <Link to="/profile" className="btn-mobile text-white hover:bg-blue-700 font-medium">
                  Profile
                </Link>
                <Link to="/settings" className="btn-mobile text-white hover:bg-blue-700 font-medium">
                  Settings
                </Link>
                <button
                  onClick={handleLogout}
                  className="btn-mobile text-white hover:bg-blue-700 font-medium"
                >
                  Logout
                </button>
              </div>
            ) : (
              <div className="flex items-center space-x-2">
                <Link to="/login" className="btn-mobile text-white hover:bg-blue-700 font-medium">
                  Login
                </Link>
                <Link to="/register" className="btn-mobile bg-white text-blue-600 hover:bg-gray-100 font-semibold shadow-lg">
                  Register
                </Link>
              </div>
            )}

            {/* CapeAI Toggle Button */}
            <button
              className="btn-mobile text-white hover:bg-blue-700 font-medium"
              aria-label="Toggle CapeAI chat"
              role="button"
            >
              CapeAI
            </button>
          </div>

          {/* Mobile Hamburger Menu */}
          <div className="lg:hidden">
            <button
              onClick={() => setMenuOpen(!menuOpen)}
              className="text-white focus:outline-none p-2 sm:p-3 rounded-lg hover:bg-blue-700 transition-all duration-200 active:scale-95 min-h-[44px] min-w-[44px] flex items-center justify-center"
              aria-label="Toggle menu"
              role="button"
            >
              <svg
                className="w-6 h-6 sm:w-7 sm:h-7"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                {menuOpen ? (
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M6 18L18 6M6 6l12 12"
                  />
                ) : (
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M4 6h16M4 12h16M4 18h16"
                  />
                )}
              </svg>
            </button>
          </div>
        </div>

        {/* Mobile Dropdown Menu */}
        {menuOpen && (
          <div className="lg:hidden animate-dropdown bg-blue-600 border-t border-blue-500 shadow-xl">
            <div className="py-2 space-y-1">
              <Link
                to="/"
                className="block btn-mobile-lg w-full text-left text-white hover:bg-blue-700 transition-all duration-200"
                onClick={() => setMenuOpen(false)}
              >
                Home
              </Link>
              <Link
                to="/about"
                className="block btn-mobile-lg w-full text-left text-white hover:bg-blue-700 transition-all duration-200"
                onClick={() => setMenuOpen(false)}
              >
                About
              </Link>

              {isAuthenticated ? (
                <>
                  <div className="block btn-mobile-lg w-full text-left text-white bg-blue-800">
                    {user?.name || user?.email}
                  </div>
                  <Link
                    to="/dashboard"
                    className="block btn-mobile-lg w-full text-left text-white hover:bg-blue-700 transition-all duration-200"
                    onClick={() => setMenuOpen(false)}
                  >
                    Dashboard
                  </Link>
                  <Link
                    to="/profile"
                    className="block btn-mobile-lg w-full text-left text-white hover:bg-blue-700 transition-all duration-200"
                    onClick={() => setMenuOpen(false)}
                  >
                    Profile
                  </Link>
                  <Link
                    to="/settings"
                    className="block btn-mobile-lg w-full text-left text-white hover:bg-blue-700 transition-all duration-200"
                    onClick={() => setMenuOpen(false)}
                  >
                    Settings
                  </Link>
                  <button
                    onClick={handleLogout}
                    className="block btn-mobile-lg w-full text-left text-white hover:bg-blue-700 transition-all duration-200"
                  >
                    Logout
                  </button>
                </>
              ) : (
                <>
                  <Link
                    to="/login"
                    className="block btn-mobile-lg w-full text-left text-white hover:bg-blue-700 transition-all duration-200"
                    onClick={() => setMenuOpen(false)}
                  >
                    Login
                  </Link>
                  <Link
                    to="/register"
                    className="block btn-mobile-lg w-full text-left text-white hover:bg-blue-700 transition-all duration-200"
                    onClick={() => setMenuOpen(false)}
                  >
                    Register
                  </Link>
                </>
              )}
            </div>
          </div>
        )}
      </div>
    </nav>
  );
}

export default Navbar;
