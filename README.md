# MemeArena

MemeArena is a fully functional, production-ready meme sharing platform built sequentially capitalizing on Django's extensive backend structure alongside highly resilient front-end mapping.

## Features
- **Algorithmic Feeds:** Content surfaced logically prioritizing interactions vs time decay matrices natively matching HN specifications.
- **Deep Threading:** Infinite recursive threaded discussion arrays encapsulated cleanly mapped via Alpine.js event togglers ensuring global DOM persistence effortlessly. 
- **REST API (`/api/v1/`):** A formalized Django REST Framework instance wrapping robust `ModelViewSets` targeting our structural components mapped via an automated `DefaultRouter()`.
- **Background Tasks:** Redis/Celery backend integrations mapping specific scheduling configurations securely tracking global analytical states locally.
- **Security:** In-depth model-level size checks preventing memory injections, alongside fully compliant CSRF architectures matching unified deployment constraints natively via Whitenoise arrays.

## Setup Guides

Ensure Docker alongside Docker-Compose are active on your system.

### 1. Build and Mount
```bash
docker compose up --build -d
```

### 2. Scaffold Data Sets (First Run)
Execute internal mappings setting base database connections.
```bash
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
```

### 3. Analytics Hooks
Manually trigger algorithmic selections (otherwise automated precisely every 24-hours internally):
```bash
docker compose exec web python manage.py shell -c "from memes.tasks import pick_meme_of_the_day; pick_meme_of_the_day()"
```

## Internal Architecture Route Endpoints
- **Application Index:** `localhost:8000`
- **Internal CMS Interface:** `localhost:8000/admin/`
- **API Interface:** `localhost:8000/api/v1/`
