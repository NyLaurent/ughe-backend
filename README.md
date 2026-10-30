# UGHE Test Web App — Backend

Django REST Framework API and Django Admin for the UGHE homepage. PostgreSQL
stores editable site settings, navigation, carousel slides, and statistics.

## Repositories

- **Backend:** [NyLaurent/ughe-backend](https://github.com/NyLaurent/ughe-backend)
- **Frontend:** [NyLaurent/ughe-frontend](https://github.com/NyLaurent/ughe-frontend)

The full Docker setup requires both repositories as sibling folders named
`backend` and `frontend`.

## Run the full app with Docker (recommended)

### Requirements

Git, Docker Desktop/Engine with Compose, internet access for the first build,
and ports `3000` and `8000` available.

### 1. Clone both repositories

Run the matching block from the parent directory where you want the project:

<details>
<summary><strong>Windows PowerShell</strong></summary>

```powershell
New-Item -ItemType Directory -Force ughe-test-web-app
Set-Location ughe-test-web-app
git clone https://github.com/NyLaurent/ughe-frontend.git frontend
git clone https://github.com/NyLaurent/ughe-backend.git backend
Set-Location backend
```

</details>

<details>
<summary><strong>Windows Command Prompt (CMD)</strong></summary>

```bat
mkdir ughe-test-web-app
cd /d ughe-test-web-app
git clone https://github.com/NyLaurent/ughe-frontend.git frontend
git clone https://github.com/NyLaurent/ughe-backend.git backend
cd backend
```

</details>

<details>
<summary><strong>macOS / Linux (Bash or Zsh)</strong></summary>

```bash
mkdir -p ughe-test-web-app
cd ughe-test-web-app
git clone https://github.com/NyLaurent/ughe-frontend.git frontend
git clone https://github.com/NyLaurent/ughe-backend.git backend
cd backend
```

</details>

The sibling folder names matter: the Compose file builds this backend and the
frontend from their relative paths.

### 2. Create the shared `.env` and start Docker

Run from the `backend` folder. If the parent `.env` already exists, keep it
and check that its database credentials match the PostgreSQL volume.

<details>
<summary><strong>Windows PowerShell</strong></summary>

```powershell
Copy-Item .env.example ..\.env
docker compose -p ughe -f docker-compose.yml --env-file ..\.env up --build -d
```

</details>

<details>
<summary><strong>Windows Command Prompt (CMD)</strong></summary>

```bat
copy .env.example ..\.env
docker compose -p ughe -f docker-compose.yml --env-file ..\.env up --build -d
```

</details>

<details>
<summary><strong>macOS / Linux (Bash or Zsh)</strong></summary>

```bash
cp .env.example ../.env
docker compose -p ughe -f docker-compose.yml --env-file ../.env up --build -d
```

</details>

Skip the copy command when `.env` already exists. On first startup, Docker
starts PostgreSQL, Django applies migrations and seeds empty content tables,
then the API and frontend start.

| What | URL |
| --- | --- |
| Django Admin | [http://localhost:8000/admin/](http://localhost:8000/admin/) |
| Homepage API | [http://localhost:8000/api/home/](http://localhost:8000/api/home/) |
| Next.js homepage | [http://localhost:3000](http://localhost:3000) |

### Local sample credentials

The sample values are for local testing. The shared parent `.env` contains the
settings Docker actually uses.

- **Django Admin:** `ughe-admin` / `UGHE-Local-Only-2026!`
- **PostgreSQL:** database `ughe`, user `postgres`, sample password
  `ughe-local-only-password`

These are separate accounts. PostgreSQL does not change credentials on an
existing data volume when `.env` changes. The admin bootstrap creates a user
once and does not reset its password on subsequent starts.

### Useful Docker commands

Run from this repository's `backend` folder:

<details>
<summary><strong>PowerShell / Command Prompt</strong></summary>

```powershell
docker compose -p ughe -f docker-compose.yml --env-file ..\.env ps
docker compose -p ughe -f docker-compose.yml --env-file ..\.env logs -f
docker compose -p ughe -f docker-compose.yml --env-file ..\.env exec backend python manage.py check
docker compose -p ughe -f docker-compose.yml --env-file ..\.env exec backend python manage.py test
docker compose -p ughe -f docker-compose.yml --env-file ..\.env down
```

</details>

<details>
<summary><strong>macOS / Linux (Bash or Zsh)</strong></summary>

```bash
docker compose -p ughe -f docker-compose.yml --env-file ../.env ps
docker compose -p ughe -f docker-compose.yml --env-file ../.env logs -f
docker compose -p ughe -f docker-compose.yml --env-file ../.env exec backend python manage.py check
docker compose -p ughe -f docker-compose.yml --env-file ../.env exec backend python manage.py test
docker compose -p ughe -f docker-compose.yml --env-file ../.env down
```

</details>

`down` preserves data. `down -v` deletes the database and uploaded-media
volumes.

## Local Python development (without Docker)

Requires Python and a configured local database. If `POSTGRES_DB` is unset,
Django uses SQLite. Run from this repository's directory.

<details>
<summary><strong>Windows PowerShell</strong></summary>

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:UGHE_ADMIN_USERNAME = "ughe-admin"
$env:UGHE_ADMIN_PASSWORD = "UGHE-Local-Only-2026!"
python manage.py migrate
python manage.py test
python manage.py ensure_admin
python manage.py seed_demo
python manage.py runserver
```

</details>

<details>
<summary><strong>Windows Command Prompt (CMD)</strong></summary>

```bat
python -m venv venv
venv\Scripts\activate.bat
pip install -r requirements.txt
set UGHE_ADMIN_USERNAME=ughe-admin
set UGHE_ADMIN_PASSWORD=UGHE-Local-Only-2026!
python manage.py migrate
python manage.py test
python manage.py ensure_admin
python manage.py seed_demo
python manage.py runserver
```

</details>

<details>
<summary><strong>macOS / Linux (Bash or Zsh)</strong></summary>

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export UGHE_ADMIN_USERNAME=ughe-admin
export UGHE_ADMIN_PASSWORD='UGHE-Local-Only-2026!'
python manage.py migrate
python manage.py test
python manage.py ensure_admin
python manage.py seed_demo
python manage.py runserver
```

</details>

The commands above use local-only sample admin credentials. Change them for
your own local environment if needed. Local API and admin URLs are
[http://localhost:8000/api/home/](http://localhost:8000/api/home/) and
[http://localhost:8000/admin/](http://localhost:8000/admin/).

## Django Admin content

- **Site settings:** site name and logo; facts eyebrow and heading.
- **Navigation items:** header and primary links, order, active state, dropdown
  indicator, search button, and staff login action.
- **Slides:** caption, button, order, active state, and uploaded image or video.
  Supported images: JPG/JPEG, PNG, GIF, WebP. Supported videos: MP4, WebM,
  Ogg/OGV.
- **Facts and statistics:** displayed value, description, order, and visibility.

The public API returns active content only. Uploaded media persists in the
Docker `media_data` volume.

For frontend-specific details, see the
[frontend repository guide](https://github.com/NyLaurent/ughe-frontend#readme).

## Security

Never commit a real `.env`. Replace sample passwords and the Django secret,
disable `DEBUG`, configure allowed hosts and CORS, and use HTTPS, durable media
storage, and a production-capable Django server before public deployment.
