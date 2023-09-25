# CoSIA back-end

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Contribute

### Install lib

1. Create env files in docker directory

```
# docker/env/db.env

POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=cosia_db
POSTGRES_PORT=5432
```

```
# docker/env/backend.env

POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_PORT=5432
```

2. Compose up with docker

```zsh
docker compose up -f docker/compose.dev.yml --build
```

3. Run migrations

```zsh
docker compose -f docker/compose.dev.yml run web python3 manage.py migrate
```

3. Create an admin superuser

```zsh
docker compose -f docker/compose.dev.yml run web python3 manage.py createsuperuser
```

Now, you can navigate on localhost:8000 :

- [rest api](localhost:8000/)
- [admin](localhost:8000/admin)

## Production settings

1. Compose up with docker

```zsh
docker compose up -f docker/compose.prod.yml --build
```

3. Run migrations

```zsh
docker compose -f docker/compose.prod.yml run web python3 manage.py migrate
```

3. Create an admin superuser

```zsh
docker compose -f docker/compose.prod.yml run web python3 manage.py createsuperuser
```

Now, you can navigate on localhost:1337 :

- [rest api](localhost:1337/)
- [admin](localhost:1337/admin)
