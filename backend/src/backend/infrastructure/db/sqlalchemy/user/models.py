from sqlalchemy import Column, String, DateTime

from src.backend.infrastructure.db.sqlalchemy.core.mixins import UUIDMixin, TimestampMixin, ActiveMixin
from src.backend.infrastructure.db.sqlalchemy.core.models import Base


class UserModel(Base,UUIDMixin,ActiveMixin,TimestampMixin):
    __tablename__ = 'users'

    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    email = Column(String(320), nullable=False, unique=True)
    username = Column(String(255), nullable=False, unique=True)
    password_hash = Column(String, nullable=False)
    last_interaction = Column(DateTime, nullable=True)