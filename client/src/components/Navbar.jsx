import { useState } from "react";
import { Link } from "react-router-dom";

export default function NavBar() {
  const [menuOpen, setMenuOpen] = useState(false);

  return (
    <nav className="fixed top-0 left-0 right-0 h-16 bg-blue-600 dark:bg-gray-900 text-white shadow-lg z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo + Brand */}
          <Link to="/" className="flex items-center space-x-2 py-2">
            <img
              src="https://lightning-s3.s3.amazonaws.com/static/website/img/capecontrol-logo.png"
              alt="CapeControl Logo"
              className="h-8 w-8 hidden sm:block"
            />
            <span className="text-xl font-semibold">CapeControl</span>
          </Link>

          {/* Desktop links - hide on smaller screens */}
          <div className="hidden lg:flex space-x-6 items-center">
            <Link to="/login" className="hover:underline py-2 px-3 rounded transition-colors hover:bg-blue-700">
              Login
            </Link>
            <Link to="/register" className="hover:underline py-2 px-3 rounded transition-colors hover:bg-blue-700">
              Register
            </Link>
          </div>

          {/* Hamburger menu button - show on smaller screens */}
          <div className="lg:hidden">
            <button
              onClick={() => setMenuOpen(!menuOpen)}
              className="text-white focus:outline-none p-2 rounded hover:bg-blue-700 transition-colors"
              aria-label="Toggle menu"
            >
              <svg
                className="w-6 h-6"
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
              to="/login"
              className="block py-3 px-4 text-white hover:bg-blue-700 rounded transition-colors"
              onClick={() => setMenuOpen(false)}
            >
              Login
            </Link>
            <Link
              to="/register"
              className="block py-3 px-4 text-white hover:bg-blue-700 rounded transition-colors"
              onClick={() => setMenuOpen(false)}
            >
              Register
            </Link>
          </div>
        )}
      </div>
    </nav>
  );
}
