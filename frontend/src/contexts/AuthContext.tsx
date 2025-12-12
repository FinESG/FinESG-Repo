import React, { createContext, useContext, useState, useCallback, useEffect } from 'react';

interface User {
  email: string;
}

interface AuthContextType {
  isAuthenticated: boolean;
  user: User | null;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  checkAuth: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

const API_BASE = 'http://127.0.0.1:8080';

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState<User | null>(null);

  // Check if user was previously authenticated
  useEffect(() => {
    const storedAuth = localStorage.getItem('isAuthenticated');
    const storedEmail = localStorage.getItem('userEmail');
    if (storedAuth === 'true' && storedEmail) {
      setIsAuthenticated(true);
      setUser({ email: storedEmail });
    }
  }, []);

  const checkAuth = useCallback(() => {
    const storedAuth = localStorage.getItem('isAuthenticated');
    return storedAuth === 'true';
  }, []);

  const login = useCallback(async (email: string, password: string) => {
    const response = await fetch(`${API_BASE}/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
      credentials: 'include', // Important for cookies
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Login failed');
    }

    // Store auth state
    localStorage.setItem('isAuthenticated', 'true');
    localStorage.setItem('userEmail', email);
    setIsAuthenticated(true);
    setUser({ email });
  }, []);

  const register = useCallback(async (email: string, password: string) => {
    const response = await fetch(`${API_BASE}/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
      credentials: 'include',
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Registration failed');
    }

    // Auto-login after registration
    await login(email, password);
  }, [login]);

  const logout = useCallback(async () => {
    try {
      await fetch(`${API_BASE}/logout`, {
        method: 'POST',
        credentials: 'include',
      });
    } catch (error) {
      console.error('Logout error:', error);
    }

    // Clear auth state
    localStorage.removeItem('isAuthenticated');
    localStorage.removeItem('userEmail');
    setIsAuthenticated(false);
    setUser(null);
  }, []);

  return (
    <AuthContext.Provider value={{
      isAuthenticated,
      user,
      login,
      register,
      logout,
      checkAuth,
    }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
};
