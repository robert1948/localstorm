import { useContext } from 'react';
import { Navigate } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';

export default function ProtectedRoute({ children }) {
  const { user } = useContext(AuthContext);

  if (user === undefined) {
    return <div className="p-4 text-center">Checking authentication...</div>; // or show spinner
  }

  return user ? children : <Navigate to="/login" />;
}
