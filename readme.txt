UGHE Test Web App - Django backend
==================================

This service provides the public homepage content API and Django Admin.
PostgreSQL is configured with environment variables; without POSTGRES_DB,
Django uses SQLite for local development and tests.

Run all services from the project root using Docker Compose. See ../readme.txt
for the complete setup and operating guide.

Local Docker setup
------------------
1. Copy the project-root .env.example to .env.
2. Set the database and Django admin credentials in .env.
3. Run `docker compose up --build`.
4. Admin: http://localhost:8000/admin/
5. Public API: http://localhost:8000/api/home/

Local Python setup without Docker
---------------------------------
Create and activate a Python virtual environment, then install:

    pip install -r requirements.txt

Set UGHE_ADMIN_USERNAME and UGHE_ADMIN_PASSWORD. For PostgreSQL, set
POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, and
POSTGRES_PORT. If POSTGRES_DB is unset, SQLite is used. Then run:

    python manage.py migrate
    python manage.py ensure_admin
    python manage.py seed_demo
    python manage.py runserver

Run tests with `python manage.py test`.

The database models and admin cover site settings, navigation items, image/video
slides, and fact/stat items. The public API returns only active content. Uploaded
media is stored under MEDIA_ROOT; production deployments should use durable
media storage and a production WSGI/ASGI server.
