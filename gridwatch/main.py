from fastapi import FastAPI

from gridwatch import database

# TODO: this is only here to make sure that entities are registered before creating tables, this will happen automatically later
from gridwatch.models import customers  # noqa

app = FastAPI()

# NOTE: This should happen with a migration tool like alembic. For now, this suffices
database.create_tables_if_not_existent()


@app.get("/")
async def root():
    return {"message": "Hello World"}
