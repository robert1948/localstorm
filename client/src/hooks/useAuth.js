import { useContext } from 'react';
import { AuthContext } from '../context/AuthContext';

export default function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    console.error('❌ useAuth() was called outside of AuthProvider!');
    console.trace();  // ✅ Add this line to see where it's being called
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
