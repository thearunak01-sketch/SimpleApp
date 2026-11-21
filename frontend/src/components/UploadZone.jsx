import { UploadCloud, LoaderCircle } from 'lucide-react';

export default function UploadZone({ accept, onChange, busy, label, hint }) {
  return <label className={`upload-zone ${busy ? 'busy' : ''}`}>
    <input type="file" accept={accept} multiple onChange={(event) => { if (event.target.files?.length) onChange(event.target.files); event.target.value = ''; }} disabled={busy} />
    {busy ? <LoaderCircle className="spin upload-icon" /> : <UploadCloud className="upload-icon" />}
    <strong>{busy ? 'Uploading...' : label}</strong>
    <span>{hint}</span>
  </label>;
}
