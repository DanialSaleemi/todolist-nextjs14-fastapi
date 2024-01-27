import os
from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.engine.url import URL as Url
from api._schema import Base, metadata


# conn_str : str | Url | None = os.environ.get("DATABASE_URL")
conn_str = "postgresql://DanialSaleemi:cwZvDMUL6X5x@ep-raspy-morning-289107.us-east-2.aws.neon.tech/neondb?sslmode=require"

if conn_str is not None:
    engine : Engine = create_engine(conn_str, echo=True)
    Base.metadata.create_all(engine)
    
else:
    print("No connection string found") 
