import { Routes, Route } from "react-router-dom";

export default function App() {
  return (
    <div className="min-h-screen bg-gray-100 text-gray-900">
      <Routes>
        <Route path="/" element={<div style={{padding: 32, fontSize: 24}}>Hello, minimal route!</div>} />
      </Routes>
    </div>
  );
}
