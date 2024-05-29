from sqlalchemy import create_engine
from sqlmodel import Session
# database creation (change from sqlite to PostgreSQL or whatever)
engine = create_engine(
    "sqlite:///recruitment.db",
    connect_args={"check_same_thread": False},
    echo=True,
)


def get_session():
    with Session(engine) as session:
        yield session
