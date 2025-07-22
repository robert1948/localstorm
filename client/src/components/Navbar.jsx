import { useState } from "react";
import { Link } from "react-router-dom";

export default function NavBar() {
  const [menuOpen, setMenuOpen] = useState(false);

  return (
    <nav className="fixed top-0 left-0 right-0 h-20 bg-blue-600 dark:bg-gray-900 text-white shadow-lg z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-20">
          {/* Logo + Brand */}
          <Link to="/" className="flex items-center space-x-2 py-2">
            <img
              src="https://lightning-s3.s3.us-east-1.amazonaws.com/static/website/img/LogoC.png"
              alt="CapeControl Logo"
              className="h-10 w-10 hidden sm:block"
            />
            <span className="text-2xl font-bold">CapeControl</span>
          </Link>

          {/* Desktop links - hide on smaller screens */}
          <div className="hidden lg:flex space-x-6 items-center">
            <Link to="/vision" className="hover:underline py-3 px-4 rounded transition-colors hover:bg-blue-700 text-lg font-medium">
              Vision
            </Link>
            <Link to="/platform" className="hover:underline py-3 px-4 rounded transition-colors hover:bg-blue-700 text-lg font-medium">
              Platform
            </Link>
            <Link to="/developers" className="hover:underline py-3 px-4 rounded transition-colors hover:bg-blue-700 text-lg font-medium">
              Developers
            </Link>
            <Link to="/login" className="hover:underline py-3 px-4 rounded transition-colors hover:bg-blue-700 text-lg font-medium">
              Login
            </Link>
            <Link to="/register" className="bg-white text-blue-600 hover:bg-gray-100 py-3 px-6 rounded-lg transition-colors text-lg font-semibold">
              Get Started
            </Link>
          </div>

          {/* Hamburger menu button - show on smaller screens */}
          <div className="lg:hidden">
            <button
              onClick={() => setMenuOpen(!menuOpen)}
              className="text-white focus:outline-none p-3 rounded hover:bg-blue-700 transition-colors"
              aria-label="Toggle menu"
            >
              <svg
                className="w-7 h-7"
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

        {/* Mobile dropdown */}
        {menuOpen && (
          <div className="lg:hidden animate-dropdown bg-blue-600 px-2 pb-3 space-y-2 border-t border-blue-500">
            <Link
              to="/vision"
              className="block py-4 px-4 text-white hover:bg-blue-700 rounded transition-colors text-lg font-medium"
              onClick={() => setMenuOpen(false)}
            >
              Vision
            </Link>
            <Link
              to="/platform"
              className="block py-4 px-4 text-white hover:bg-blue-700 rounded transition-colors text-lg font-medium"
              onClick={() => setMenuOpen(false)}
            >
              Platform
            </Link>
            <Link
              to="/developers"
              className="block py-4 px-4 text-white hover:bg-blue-700 rounded transition-colors text-lg font-medium"
              onClick={() => setMenuOpen(false)}
            >
              Developers
            </Link>
            <Link
              to="/login"
              className="block py-4 px-4 text-white hover:bg-blue-700 rounded transition-colors text-lg font-medium"
              onClick={() => setMenuOpen(false)}
            >
              Login
            </Link>
            <Link
              to="/register"
              className="block py-4 px-4 text-white bg-white/10 hover:bg-white/20 rounded transition-colors text-lg font-semibold"
              onClick={() => setMenuOpen(false)}
            >
              Get Started
            </Link>
          </div>
        )}
      </div>
    </nav>
  );
}
