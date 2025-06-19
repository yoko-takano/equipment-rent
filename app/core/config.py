from tortoise.contrib.fastapi import register_tortoise
from fastapi import FastAPI

def init_db(app: FastAPI):
    register_tortoise(
        app,
        db_url="postgres://rentdb:rentdb@rent-postgres:5432/rent",
        modules={"models": ["app.database.models"]},
        generate_schemas=True,
        add_exception_handlers=True,
    )
