import React, { createContext, useContext, useState, useEffect, type ReactNode } from 'react';
import type { WpUser } from '../types';
import { fetchCurrentUser, getToken, login, register, logout as authLogout } from '../services/auth';

export interface AuthState {
    user: WpUser | null;
    isAuthenticated: boolean;
    isLoading: boolean;
    token: string | null;
}

interface AuthContextType extends AuthState {
    signIn: (email: string, password: string) => Promise<void>;
    signUp: (email: string, password: string, firstName: string, lastName: string) => Promise<void>;
    signOut: () => void;
}

const AuthContext = createContext<AuthContextType | null>(null);

export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
    const [state, setState] = useState<AuthState>({
        user: null, isAuthenticated: false, isLoading: true, token: null
    });

    useEffect(() => {
        const token = getToken();
        if (token) {
            fetchCurrentUser()
                .then(user => setState({ user, isAuthenticated: true, isLoading: false, token }))
                .catch(() => setState(s => ({ ...s, isLoading: false })));
        } else {
            setState(s => ({ ...s, isLoading: false }));
        }
    }, []);

    const signIn = async (email: string, password: string) => {
        const user = await login(email, password);
        setState({ user, isAuthenticated: true, isLoading: false, token: getToken() });
    };

    const signUp = async (email: string, password: string, firstName: string, lastName: string) => {
        const user = await register(email, password, firstName, lastName);
        setState({ user, isAuthenticated: true, isLoading: false, token: getToken() });
    };

    const signOut = () => {
        authLogout();
        setState({ user: null, isAuthenticated: false, isLoading: false, token: null });
    };

    return <AuthContext.Provider value={{ ...state, signIn, signUp, signOut }}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
    const ctx = useContext(AuthContext);
    if (!ctx) throw new Error('useAuth must be used within AuthProvider');
    return ctx;
};
