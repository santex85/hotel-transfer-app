// src/context/AuthContext.jsx
import React, { createContext, useContext, useState, useEffect } from 'react';
import apiClient from '../services/api';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [token, setToken] = useState(localStorage.getItem('token'));

  useEffect(() => {
    if (token) {
      console.log('Setting token in localStorage and headers:', token);
      localStorage.setItem('token', token);
      // Применяем токен ко всем последующим запросам
      apiClient.defaults.headers.common['Authorization'] = `Bearer ${token}`;
    } else {
      console.log('Removing token from localStorage and headers');
      localStorage.removeItem('token');
      delete apiClient.defaults.headers.common['Authorization'];
    }
  }, [token]);

  const login = (newToken) => {
    console.log('Login function called with token:', newToken);
    setToken(newToken);
  };

  const logout = () => {
    console.log('Logout function called');
    setToken(null);
  };

  const authContextValue = {
    isAuthenticated: !!token,
    login,
    logout,
  };

  console.log('AuthContext state - isAuthenticated:', !!token);

  return (
    <AuthContext.Provider value={authContextValue}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  return useContext(AuthContext);
}; 