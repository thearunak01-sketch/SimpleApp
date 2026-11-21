import { useState } from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import { FileText, Image as ImageIcon, LayoutDashboard, LogOut, Menu, X } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

const items = [
  { to: '/images', label: 'Images', icon: ImageIcon },
  { to: '/documents', label: 'Document Vault', icon: FileText },
];

export default function DashboardLayout({ children }) {
  const { user, logout } = useAuth();
  const [open, setOpen] = useState(false);
  const navigate = useNavigate();

  async function handleLogout() {
    await logout();
    navigate('/login', { replace: true });
  }

  return <div className="dashboard-shell">
    <header className="dashboard-header">
      <div className="dashboard-header-inner">
        <button className="mobile-menu" onClick={() => setOpen(!open)} aria-label="Toggle menu">{open ? <X size={20} /> : <Menu size={20} />}</button>
        <NavLink to="/images" className="brand"><span className="brand-mark"><LayoutDashboard size={17} /></span><span>Media Vault</span></NavLink>
        <div className="account-area"><div className="account-copy"><strong>{user?.name}</strong><span>{user?.email} · {user?.mobile}</span></div><button className="logout" onClick={handleLogout}><LogOut size={16} /> Log out</button></div>
      </div>
    </header>
    <div className="dashboard-body">
      <aside className={`sidebar ${open ? 'sidebar-open' : ''}`}><nav>{items.map(({ to, label, icon: Icon }) => <NavLink key={to} to={to} onClick={() => setOpen(false)} className={({ isActive }) => `side-link ${isActive ? 'active' : ''}`}><Icon size={19} />{label}</NavLink>)}</nav></aside>
      {open && <div className="sidebar-backdrop" onClick={() => setOpen(false)} />}
      <main className="dashboard-main">{children}</main>
    </div>
  </div>;
}
