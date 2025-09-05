
from sqlmodel import create_engine, Session
import os

engine = create_engine(os.environ["DATABASE_URL"])


async def get_db_session():
    # Return the session each time is called
    with Session(engine) as session:
        yield session
