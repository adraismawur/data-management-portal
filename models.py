from datetime import datetime
from typing import List

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Table, create_engine
from sqlalchemy.orm import (
    Mapped,
    foreign,
    relationship,
    remote,
    scoped_session,
    sessionmaker,
    mapped_column,
)
from sqlalchemy.orm import DeclarativeBase

engine = create_engine("sqlite:///tmp/", echo=True)
db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)


class Base(DeclarativeBase):
    pass


class Document(Base):
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    form_type: Mapped[str] = mapped_column()
    content: Mapped[str] = mapped_column()
    signed: Mapped[bool] = mapped_column()
    version: Mapped[int] = mapped_column()
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))


projects_users_association = Table(
    "projects_users",
    Base.metadata,
    Column("project_id", ForeignKey("projects.id")),
    Column("user_id", ForeignKey("users.id")),
)


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str] = mapped_column()
    users: Mapped[List[User]] = relationship(secondary=projects_users_association)

    dmp: Mapped[Document | None] = relationship(
        "Document",
        primaryjoin="and_(Project.id == Document.project_id, Document.form_type=='DMP')",
    )

    pcf: Mapped[Document | None] = relationship(
        "Document",
        primaryjoin="and_(Project.id == Document.project_id, Document.form_type=='PCF')",
    )

    iaf: Mapped[List[Document] | None] = relationship(
        "Document",
        primaryjoin="and_(Project.id == Document.project_id, Document.form_type=='IAF')",
    )

    def __init__(self, title: str, description: str):
        self.title = title
        self.description = description

    @staticmethod
    def from_form(form) -> Project:
        if "title" not in form:
            return None

        if "description" not in form:
            return None

        return Project(form.title.data, form.description.data)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column()
    role: Mapped[int] = mapped_column()

    is_authenticated: bool = False
    is_active = True
    is_anonymous = False

    def get_id(self):
        return str(self.id)

    def __init__(self, name, email, role):
        self.name = name
        self.email = email
        self.role = role


class TestLogin(Base):
    __tablename__ = "test_logins"

    id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    user_name: Mapped[str] = mapped_column()


class Archival(Base):
    __tablename__ = "archivals"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )
    status: Mapped[str] = mapped_column()
    created_at: Mapped[datetime] = mapped_column()
    updated_at: Mapped[datetime] = mapped_column()
    completed_at: Mapped[datetime] = mapped_column()

    def __init__(self):
        self.status = "created"
        self.created_at = datetime.now()


db = SQLAlchemy(model_class=Base)
