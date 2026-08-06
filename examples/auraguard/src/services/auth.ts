import type { AuthResponse, WpUser, WooOrder } from '../types';
import { MOCK_USER, MOCK_CREDENTIALS, mockOrders } from '../data/mockData';

const WOO_URL = import.meta.env.VITE_WOO_URL;
const TOKEN_KEY = 'auth_token';

export const getToken = (): string | null => localStorage.getItem(TOKEN_KEY);
export const setToken = (token: string): void => localStorage.setItem(TOKEN_KEY, token);
export const clearToken = (): void => localStorage.removeItem(TOKEN_KEY);

const authHeaders = () => ({
    'Authorization': `Bearer ${getToken()}`,
    'Content-Type': 'application/json',
});

export const login = async (email: string, password: string): Promise<WpUser> => {
    if (!WOO_URL) {
        if (email === MOCK_CREDENTIALS.email && password === MOCK_CREDENTIALS.password) {
            setToken('mock_jwt_token_for_demo');
            return MOCK_USER;
        }
        throw new Error('Invalid credentials. Use demo@example.com / demo1234');
    }
    const res = await fetch(`${WOO_URL}/wp-json/simple-jwt-login/v1/auth`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
    });
    if (!res.ok) throw new Error('Login failed');
    const data: AuthResponse = await res.json();
    setToken(data.data.jwt);
    return fetchCurrentUser();
};

export const register = async (
    email: string, password: string, firstName: string, lastName: string
): Promise<WpUser> => {
    if (!WOO_URL) {
        setToken('mock_jwt_token_for_demo');
        return { ...MOCK_USER, email, name: `${firstName} ${lastName}`, first_name: firstName, last_name: lastName };
    }
    const res = await fetch(`${WOO_URL}/wp-json/simple-jwt-login/v1/users`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password, first_name: firstName, last_name: lastName }),
    });
    if (!res.ok) throw new Error('Registration failed');
    const data: AuthResponse = await res.json();
    setToken(data.data.jwt);
    return fetchCurrentUser();
};

export const fetchCurrentUser = async (): Promise<WpUser> => {
    if (!WOO_URL || getToken() === 'mock_jwt_token_for_demo') return MOCK_USER;
    const res = await fetch(`${WOO_URL}/wp-json/wp/v2/users/me?context=edit`, {
        headers: authHeaders(),
    });
    if (!res.ok) { clearToken(); throw new Error('Session expired'); }
    return res.json();
};

export const updateProfile = async (data: Partial<WpUser>): Promise<WpUser> => {
    if (!WOO_URL) return { ...MOCK_USER, ...data } as WpUser;
    const res = await fetch(`${WOO_URL}/wp-json/wp/v2/users/me`, {
        method: 'PUT',
        headers: authHeaders(),
        body: JSON.stringify(data),
    });
    if (!res.ok) throw new Error('Update failed');
    return res.json();
};

export const fetchMyOrders = async (): Promise<WooOrder[]> => {
    if (!WOO_URL) return mockOrders;
    const res = await fetch(`${WOO_URL}/wp-json/wc/v3/orders?customer=me&per_page=10`, {
        headers: authHeaders(),
    });
    if (!res.ok) return [];
    return res.json();
};

export const logout = (): void => clearToken();
