import { createContext, useContext, useEffect, useMemo, useState } from 'react';
import api, { apiError } from '../services/api';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get('/profile')
      .then(({ data }) => setUser(data.user))
      .catch(() => setUser(null))
      .finally(() => setLoading(false));
  }, []);

  async function login(email, password) {
    try {
      const { data } = await api.post('/auth/login', { email, password });
      setUser(data.user);
    } catch (error) {
      throw new Error(apiError(error, 'Unable to sign in.'));
    }
  }

  async function register(form) {
    try {
      await api.post('/auth/register', form);
      await login(form.email, form.password);
    } catch (error) {
      throw new Error(apiError(error, 'Unable to create your account.'));
    }
  }

  async function logout() {
    try {
      await api.post('/auth/logout');
    } finally {
      setUser(null);
    }
  }

  const value = useMemo(() => ({ user, loading, login, register, logout }), [user, loading]);
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  return useContext(AuthContext);
}
