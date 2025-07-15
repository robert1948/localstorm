
import { Routes, Route } from "react-router-dom";
import { AuthProvider, AuthContext } from "./context/AuthContext";
import { useContext } from "react";


function HomeWithAuth() {
  const { user, loading, error } = useContext(AuthContext);
  if (loading) return <div style={{padding: 32, fontSize: 24}}>Loading auth...</div>;
  if (error) return <div style={{padding: 32, fontSize: 24, color: 'red'}}>Auth error: {error.message || String(error)}</div>;
  return (
    <div style={{padding: 32, fontSize: 24}}>
      Hello, {user ? user.username : "guest"}! (Auth context loaded)
    </div>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <div className="min-h-screen bg-gray-100 text-gray-900">
        <Routes>
          <Route path="/" element={<HomeWithAuth />} />
        </Routes>
      </div>
    </AuthProvider>
  );
}
