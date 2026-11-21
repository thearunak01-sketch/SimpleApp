import PublicNav from './PublicNav';

export default function AuthShell({ children }) {
  return <div className="auth-page"><PublicNav /><main className="auth-main"><div className="glow glow-green" /><div className="glow glow-blue" /><div className="auth-card-wrap">{children}</div></main></div>;
}
