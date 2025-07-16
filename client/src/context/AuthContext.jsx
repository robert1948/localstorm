// client/src/context/AuthContext.jsx
import { createContext, useState, useEffect } from 'react';
import { getCurrentUser } from '../api/user';
import { getToken, clearToken } from '../utils/token';

// Initial context to avoid undefined errors
export const AuthContext = createContext({
  user: null,
  setUser: () => {},
  logout: () => {},
  loading: true,
});

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  const logout = () => {
    clearToken();
    setUser(null);
  };

  useEffect(() => {
    const initializeUser = async () => {
      const token = getToken();
      if (!token) {
        setLoading(false);
        return;
      }

      try {
        const currentUser = await getCurrentUser();
        setUser(currentUser);
      } catch (err) {
        console.warn('⚠️ Auto-login failed:', err.message);
        logout();
      } finally {
        setLoading(false);
      }
    };

    initializeUser();
  }, []);

  const contextValue = {
    user,
    setUser,
    logout,
    loading,
  };

  return (
    <AuthContext.Provider value={contextValue}>
      {loading ? (
        <div className="flex items-center justify-center min-h-screen">
          <div className="text-center">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
            <p className="mt-2 text-sm text-gray-600">Loading...</p>
          </div>
        </div>
      ) : (
        children
      )}
    </AuthContext.Provider>
  );
};
