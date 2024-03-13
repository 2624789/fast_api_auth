# Environment Variables

  * DATABASE_USER
  * DATABASE_PASSWORD
  * DATABASE_NAME
  * DATABASE_HOST
  * DATABASE_PORT

# Migrations

## Run migrations

    $ pipenv run alembic upgrade head

## Generate migrations

    $ pipenv run alembic revision -m "add demo users"
    $ pipenv run alembic revision --autogenerate -m "create table users"

# Run

using `pipenv` for development

    $ pipenv install
    $ pipenv run uvicorn app.main:app --reload
