import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import ProtectedRoute from './components/ProtectedRoute';
import DashboardLayout from './components/DashboardLayout';
import Landing from './pages/Landing';
import Login from './pages/Login';
import Register from './pages/Register';
import Images from './pages/Images';
import DocumentVault from './pages/DocumentVault';

function AppRoutes() {
  return <Routes>
    <Route path="/" element={<Landing />} />
    <Route path="/login" element={<Login />} />
    <Route path="/register" element={<Register />} />
    <Route path="/images" element={<ProtectedRoute><DashboardLayout><Images /></DashboardLayout></ProtectedRoute>} />
    <Route path="/documents" element={<ProtectedRoute><DashboardLayout><DocumentVault /></DashboardLayout></ProtectedRoute>} />
    <Route path="*" element={<Navigate to="/" replace />} />
  </Routes>;
}

export default function App() { return <AuthProvider><BrowserRouter><AppRoutes /></BrowserRouter></AuthProvider>; }
