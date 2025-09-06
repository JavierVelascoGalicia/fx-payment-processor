
from sqlmodel import create_engine, Session, SQLModel
import os

engine = create_engine(os.environ["DATABASE_URL"])


def create_all_tables():
    SQLModel.metadata.create_all(engine, checkfirst=True)


def drop_all_tables():
    SQLModel.metadata.drop_all(engine)


async def get_db_session():
    # Return the session each time is called
    with Session(engine) as session:
        yield session
