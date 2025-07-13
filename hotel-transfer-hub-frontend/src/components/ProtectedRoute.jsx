// src/components/ProtectedRoute.jsx
import React from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const ProtectedRoute = ({ children }) => {
  const { isAuthenticated } = useAuth();
  const location = useLocation();

  console.log('ProtectedRoute - isAuthenticated:', isAuthenticated);
  console.log('ProtectedRoute - current location:', location.pathname);

  if (!isAuthenticated) {
    console.log('ProtectedRoute - redirecting to login');
    // Перенаправляем на страницу входа, если пользователь не аутентифицирован
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  console.log('ProtectedRoute - rendering protected content');
  return children;
};

export default ProtectedRoute; 