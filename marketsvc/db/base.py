import os

from sqlalchemy import URL, create_engine
from sqlalchemy.orm import DeclarativeBase

url_object = URL.create(
    "postgresql+psycopg2",
    username=os.environ.get("POSTGRES_USER"),
    password=os.environ.get("POSTGRES_PASSWORD"),
    host=os.environ.get("POSTGRES_DB"),
    database=os.environ.get("POSTGRES_DB"),
    port=os.environ.get("POSTGRES_PORT"),
)

engine = create_engine(url_object, echo=True)


class Base(DeclarativeBase):
    pass
