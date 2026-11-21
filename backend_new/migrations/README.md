# Flask-Migrate migrations

Run migrations from the `backend` directory after setting `DATABASE_URL`:

```bash
flask --app run.py db upgrade
```

Create a new migration after model changes with `flask --app run.py db migrate -m "describe change"`, then review it before applying.
