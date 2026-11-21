import { Link } from 'react-router-dom';
import { ArrowLeft, FileText, Image as ImageIcon, Sparkles } from 'lucide-react';

export default function PublicNav() {
  return (
    <header className="public-nav">
      <div className="nav-inner wide">
        <Link to="/" className="brand"><span className="brand-mark"><Sparkles size={18} /></span><span>Media Vault</span></Link>
        <nav className="public-links">
          <Link to="/images"><ImageIcon size={15} /> Images</Link>
          <Link to="/documents"><FileText size={15} /> Documents</Link>
        </nav>
        <Link to="/" className="back-link"><ArrowLeft size={15} /> Back home</Link>
      </div>
    </header>
  );
}
