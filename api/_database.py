import os
from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.engine.url import URL as Url
from api._schema import Base
from dotenv import load_dotenv


# load database connection string from .env
_ : bool = load_dotenv()
conn_str : str | None = os.getenv("DATABASE_URL")
# print(conn_str)
if conn_str is not None:
    engine : Engine = create_engine(conn_str)
else:
    raise Exception("DATABASE_URL not found")


Base.metadata.create_all(engine)
