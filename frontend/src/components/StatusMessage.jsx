import { CheckCircle2, XCircle } from 'lucide-react';

export default function StatusMessage({ type, children }) {
  const Icon = type === 'success' ? CheckCircle2 : XCircle;
  return <div className={`status ${type}`}><Icon size={17} /> <span>{children}</span></div>;
}
