import React from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';

interface ProtectedRouteProps { children: React.ReactNode; }

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ children }) => {
    const { isAuthenticated, isLoading } = useAuth();
    const location = useLocation();

    if (isLoading) return <div className="flex items-center justify-center h-screen bg-brand-primary font-display text-2xl animate-pulse">Loading...</div>;
    if (!isAuthenticated) return <Navigate to="/account/login" state={{ from: location }} replace />;
    return <>{children}</>;
};

export default ProtectedRoute;
