import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { UserRoundPlus } from 'lucide-react';
import AuthShell from '../components/AuthShell';
import StatusMessage from '../components/StatusMessage';
import { useAuth } from '../context/AuthContext';

export default function Register() {
  const { register } = useAuth();
  const navigate = useNavigate();
  const [form, setForm] = useState({ name: '', email: '', mobile: '', password: '', confirmPassword: '' });
  const [error, setError] = useState('');
  const [busy, setBusy] = useState(false);
  function update(field, value) { setForm((current) => ({ ...current, [field]: value })); }
  async function submit(event) {
    event.preventDefault(); setError('');
    if (form.password !== form.confirmPassword) { setError('Passwords do not match.'); return; }
    setBusy(true);
    try { await register(form); navigate('/images', { replace: true }); }
    catch (err) { setError(err.message); }
    finally { setBusy(false); }
  }
  return <AuthShell><div className="auth-heading"><span className="auth-icon blue"><UserRoundPlus size={22} /></span><small>START ORGANIZED</small><h1>Create your account</h1><p>Build your private home for important files.</p></div><form className="form-card" onSubmit={submit}>{error && <StatusMessage type="error">{error}</StatusMessage>}<label>Full name<input value={form.name} required autoComplete="name" placeholder="Jane Doe" onChange={(e) => update('name', e.target.value)} /></label><label>Email<input type="email" value={form.email} required autoComplete="email" placeholder="jane@example.com" onChange={(e) => update('email', e.target.value)} /></label><label>Mobile number<input value={form.mobile} required autoComplete="tel" placeholder="+1 555 000 1234" onChange={(e) => update('mobile', e.target.value)} /></label><div className="form-two"><label>Password<input type="password" value={form.password} required minLength="8" autoComplete="new-password" placeholder="8+ characters" onChange={(e) => update('password', e.target.value)} /></label><label>Confirm password<input type="password" value={form.confirmPassword} required autoComplete="new-password" placeholder="Repeat password" onChange={(e) => update('confirmPassword', e.target.value)} /></label></div><button className="button button-dark button-full" disabled={busy}>{busy ? 'Creating account...' : 'Create account'}</button><p className="form-foot">Already have an account? <Link to="/login">Sign in</Link></p></form></AuthShell>;
}
