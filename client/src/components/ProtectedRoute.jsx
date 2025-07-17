import { Navigate } from 'react-router-dom';
import useAuth from '../hooks/useAuth';

export default function ProtectedRoute({ children }) {
  const { user } = useAuth();

  // Optional: Show loading if user is still undefined (e.g., loading from localStorage later)
  if (user === undefined) {
    return <div className="p-4 text-center">Checking authentication...</div>;
  }

  // If user is not logged in (null), redirect to login
  if (!user) {
    return <Navigate to="/login" replace />;
  }

  // Authenticated → allow access
  return children;
}
