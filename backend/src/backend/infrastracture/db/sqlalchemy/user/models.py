from sqlalchemy import Column, String, DateTime

from src.backend.infrastracture.db.sqlalchemy.core.mixins import UUIDMixin, TimeStampMixin, ActiveMixin
from src.backend.infrastracture.db.sqlalchemy.core.models import Base


class UserModel(Base, UUIDMixin, TimeStampMixin, ActiveMixin):
    __tablename__ = "users"

    first_name =Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    email = Column(String(320), nullable=False, unique=True)
    username = Column(String(255), nullable=False, unique=True)
    password_hash = Column(String, nullable=False)
    role = Column(String(30), nullable=False)
    last_interaction = Column(DateTime, nullable=True)