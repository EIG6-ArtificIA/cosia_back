# CoSIA back-end

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Install lib

1. Create env files

```
# env/db.env

POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=cosia_db
POSTGRES_PORT=5432
```

```
# env/backend.env

POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_PORT=5432
```

2. Compose up with docker

```zsh
docker compose up --build
```

3. Run migrations

```zsh
docker compose run backend python3 manage.py migrate
```

3. Create an admin superuser

```zsh
docker compose run backend python3 manage.py createsuperuser
```
