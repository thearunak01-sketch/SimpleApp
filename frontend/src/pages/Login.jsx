import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { LockKeyhole } from 'lucide-react';
import AuthShell from '../components/AuthShell';
import StatusMessage from '../components/StatusMessage';
import { useAuth } from '../context/AuthContext';

export default function Login() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [form, setForm] = useState({ email: '', password: '' });
  const [error, setError] = useState('');
  const [busy, setBusy] = useState(false);

  async function submit(event) {
    event.preventDefault(); setError(''); setBusy(true);
    try { await login(form.email, form.password); navigate('/images', { replace: true }); }
    catch (err) { setError(err.message); }
    finally { setBusy(false); }
  }

  return <AuthShell><div className="auth-heading"><span className="auth-icon green"><LockKeyhole size={22} /></span><small>PRIVATE WORKSPACE</small><h1>Welcome back</h1><p>Sign in to access your images and documents.</p></div><form className="form-card" onSubmit={submit}>{error && <StatusMessage type="error">{error}</StatusMessage>}<label>Email<input type="email" value={form.email} required autoComplete="email" placeholder="jane@example.com" onChange={(e) => setForm({ ...form, email: e.target.value })} /></label><label>Password<input type="password" value={form.password} required autoComplete="current-password" placeholder="Your password" onChange={(e) => setForm({ ...form, password: e.target.value })} /></label><button className="button button-dark button-full" disabled={busy}>{busy ? 'Signing in...' : 'Sign in'}</button><p className="form-foot">New here? <Link to="/register">Create an account</Link></p></form></AuthShell>;
}
