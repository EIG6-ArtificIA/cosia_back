# CoSIA back-end

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Contribute

### Install lib

1. Create .env file in docker directory

```bash
# .env

PGPASSWORD = postgres
PGDATABASE = cosia_db
S3_ACCESS_KEY_ID = # get rw s3 access key
S3_SECRET_ACCESS_KEY = # get rw s3 secret key
S3_HOST = ...
S3_REGION_NAME = ...
S3_BUCKET = ...
```

2. Compose up with docker

```zsh
docker compose -f docker/compose.dev.yml up --build
```

3. Run migrations

```zsh
docker compose -f docker/compose.dev.yml run web python3 manage.py migrate
```

3. Create an admin superuser

```zsh
docker compose -f docker/compose.dev.yml run web python3 manage.py createsuperuser
```

4. Load departments

```zsh
docker compose -f docker/compose.dev.yml exec web python3 manage.py shell
```

Then

```python
from predictions_map import load
load.department_load()
load.department_data_load()
load.dom_tom_load()
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

## Tests

```zsh
docker compose up -f docker/compose.dev.yml run web python3 test
```
