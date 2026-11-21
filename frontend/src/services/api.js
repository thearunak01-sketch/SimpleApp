import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000/api',
  withCredentials: true,
});

function readCookie(name) {
  const value = document.cookie.split('; ').find((row) => row.startsWith(`${name}=`));
  return value ? decodeURIComponent(value.split('=').slice(1).join('=')) : '';
}

api.interceptors.request.use((config) => {
  const csrfToken = readCookie('csrf_access_token');
  if (csrfToken) config.headers['X-CSRF-TOKEN'] = csrfToken;
  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401 && !['/login', '/register'].includes(window.location.pathname)) {
      window.location.assign('/login');
    }
    return Promise.reject(error);
  },
);

export function apiError(error, fallback = 'Something went wrong.') {
  return error.response?.data?.error || error.message || fallback;
}

export default api;
