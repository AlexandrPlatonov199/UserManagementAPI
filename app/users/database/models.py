from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Base class for SQLAlchemy models.

    This class is used as a base class for all SQLAlchemy models in the application. It defines a mapping of Python
    types to SQLAlchemy types, which allows the models to be defined using Python types.

    Attributes:
        type_annotation_map (dict): A mapping of Python types to SQLAlchemy types.
    """
    type_annotation_map = {
        datetime: DateTime(timezone=True),
    }


class User(Base):
    """Model for users.

    This class is used to represent users in the database. It defines the columns in the `users` table, and maps them
    to Python attributes.

    Attributes:
        id (Mapped[int]): The unique identifier for the user.
        username (Mapped[str]): The username for the user. This must be unique.
        email (Mapped[str]): The email address for the user. This must be unique.
        registration_date (Mapped[datetime]): The date and time when the user registered.
        updated_registration_date (Mapped[datetime]): The date and time when the user was last updated.
    """
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    registration_date: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_registration_date: Mapped[datetime] = mapped_column(default=datetime.now, onupdate=datetime.now)
