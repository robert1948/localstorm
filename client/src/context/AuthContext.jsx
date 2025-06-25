import { createContext, useState, useEffect } from 'react';
import { getCurrentUser } from '../api/user';
import { getToken, clearToken } from '../utils/token';

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const initializeUser = async () => {
      const token = getToken();
      if (token) {
        try {
          const currentUser = await getCurrentUser();
          setUser(currentUser);
        } catch (err) {
          console.warn('Auto-login failed:', err.message);
          handleLogout();
        }
      }
      setLoading(false);
    };
    initializeUser();
  }, []);

  const handleLogout = () => {
    clearToken(); // ✅ fixed
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, setUser, logout: handleLogout }}>
      {!loading && children}
    </AuthContext.Provider>
  );
};
