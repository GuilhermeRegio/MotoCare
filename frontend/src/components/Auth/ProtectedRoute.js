import React from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';

const ProtectedRoute = ({ children }) => {
  const { isAuthenticated, loading, user } = useAuth();

  console.log('=== ProtectedRoute Debug ===');
  console.log('Loading:', loading);
  console.log('IsAuthenticated:', isAuthenticated);
  console.log('User:', user);
  console.log('Children:', children);

  if (loading) {
    console.log('Showing loading spinner...');
    return (
      <div className="d-flex justify-content-center align-items-center min-vh-100">
        <div className="spinner-border text-primary" role="status">
          <span className="visually-hidden">Carregando...</span>
        </div>
      </div>
    );
  }

  if (!isAuthenticated) {
    console.log('Not authenticated, redirecting to login...');
    return <Navigate to="/login" replace />;
  }

  console.log('Authenticated, rendering children...');
  return children;
};

export default ProtectedRoute;
