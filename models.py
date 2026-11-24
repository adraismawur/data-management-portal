from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, mapped_column
from sqlalchemy.orm import DeclarativeBase
from app import db

engine = create_engine("sqlite:///tmp/", echo=True)
db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)


class Base(DeclarativeBase):
    pass


class Project(Base):
    __tablename__ = "project"

    id = mapped_column("id", int, primary_key=True, autoincrement=True)
    title = mapped_column("title", str, unique=True)

    def __init__(self, title: str):
        self.title = title
