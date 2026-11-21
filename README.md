# Media Vault

A full-stack image and document management system with a JavaScript React frontend and modular Flask REST API.

## Architecture

- `frontend/` - React JavaScript SPA built with Vite and Axios.
- `backend/` - Flask REST API with SQLAlchemy, Flask-Migrate, JWT cookie authentication, Pillow, and boto3.
- PostgreSQL stores users and file metadata. File binaries live in a private S3 bucket.
- JWT access tokens are stored in HttpOnly cookies. The frontend sends the readable CSRF cookie back on state-changing requests.

## Backend setup

1. Create a PostgreSQL database and a private S3 bucket.
2. Copy `backend/.env.example` to `backend/.env` and fill in the values.
3. Create a virtual environment and install dependencies:

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate # macOS/Linux
pip install -r requirements.txt
```

4. Apply the SQLAlchemy schema with Flask-Migrate:

```bash
flask --app run.py db upgrade
```

5. Start the API:

```bash
python run.py
```

The API runs at `http://localhost:5000`.

## Frontend setup

1. Copy `frontend/.env.example` to `frontend/.env` if the API is not at the default URL.
2. Install and run the SPA:

```bash
cd frontend
npm install
npm run dev
```

The frontend runs at `http://localhost:5173`.

## API overview

- `POST /api/auth/register` - create a user with a Werkzeug password hash.
- `POST /api/auth/login` - issue an HttpOnly JWT cookie.
- `POST /api/auth/logout` - clear the JWT cookies.
- `GET /api/profile` - return the authenticated user's profile.
- `POST /api/images/upload` - upload one processed image.
- `POST /api/images/upload-multiple` - upload multiple processed images.
- `GET /api/images?page=1&per_page=9` - owner-scoped, database-level pagination and signed image URLs.
- `POST /api/documents/upload` - upload one document.
- `POST /api/documents/upload-multiple` - upload multiple documents.
- `GET /api/documents?page=1&per_page=10` - owner-scoped, database-level pagination.
- `GET /api/documents/<id>/download` - issue an owner-checked signed S3 download URL.

Upload forms use multipart field names `file` for single uploads and `files` for multiple uploads.
