import { Link } from 'react-router-dom';
import { ArrowRight, Check, FileText, Image as ImageIcon, LockKeyhole, ShieldCheck, Sparkles, UploadCloud } from 'lucide-react';
import PublicNav from '../components/PublicNav';

const features = [
  { icon: ImageIcon, title: 'Image gallery', text: 'Keep your visual library organized, easy to preview, and ready wherever you work.' },
  { icon: FileText, title: 'Document vault', text: 'Store PDFs, text files, and office documents in one private workspace.' },
  { icon: ShieldCheck, title: 'Private by default', text: 'JWT-protected access and owner checks keep every file tied to its account.' },
];

export default function Landing() {
  return <div className="landing-page"><PublicNav /><main>
    <section className="hero wide">
      <div className="glow glow-blue hero-glow" /><div className="glow glow-green hero-glow-two" />
      <div className="hero-grid">
        <div className="hero-copy"><div className="eyebrow"><span className="status-dot" /> Your files, beautifully organized</div><h1>A calmer home for your <em>digital life.</em></h1><p>Media Vault brings your images and important documents together in one focused, private workspace. Upload once, find anything, and stay in control.</p><div className="hero-actions"><Link to="/register" className="button button-dark">Create your vault <ArrowRight size={16} /></Link><Link to="/login" className="button button-light">I already have an account</Link></div><div className="micro-proof"><span><LockKeyhole size={15} /> Private by default</span><span><Check size={15} /> Simple to use</span></div></div>
        <div className="workspace-preview"><div className="preview-window"><div className="preview-heading"><div><small>YOUR WORKSPACE</small><h2>Everything in its place.</h2></div><span className="preview-icon"><UploadCloud size={18} /></span></div><div className="preview-grid"><div className="preview-tile"><div className="tile-image tile-sky"><ImageIcon size={19} /></div><strong>Image gallery</strong><small>Preview every moment</small></div><div className="preview-tile"><div className="tile-image tile-warm"><FileText size={19} /></div><strong>Document vault</strong><small>Keep life on file</small></div></div><div className="protected-row"><div className="progress"><span /></div><small>Protected</small></div></div></div>
      </div>
    </section>
    <section id="features" className="feature-section"><div className="wide feature-grid">{features.map(({ icon: Icon, title, text }) => <article className="feature-card" key={title}><span className="feature-icon"><Icon size={19} /></span><h2>{title}</h2><p>{text}</p></article>)}</div></section>
    <section className="wide benefit-section"><div><p className="section-kicker">A better way to manage files</p><h2>Less hunting. More doing.</h2><p className="benefit-copy">Designed for the files you care about most, Media Vault keeps your everyday workflow clear without adding clutter.</p><ul>{['Private storage for every upload', 'Fast previews and one-click downloads', 'Automatic image optimization', 'Access from any screen'].map((text) => <li key={text}><span><Check size={14} /></span>{text}</li>)}</ul></div><div className="cta-panel"><small>READY WHEN YOU ARE</small><h2>Start your private vault today.</h2><p>Create an account in a minute and give your images and documents the home they deserve.</p><Link to="/register" className="button button-light">Get started free <ArrowRight size={16} /></Link></div></section>
  </main><footer className="footer"><div className="wide"><span className="brand"><span className="brand-mark"><Sparkles size={16} /></span> Media Vault</span><span>Securely organize what matters.</span></div></footer></div>;
}
