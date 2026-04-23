
from sqlalchemy import Column, String, Boolean

from backend.infrastracture.db.sqlalchemy.core.mixins import UUIDMixin, TimeStampMixin
from backend.infrastracture.db.sqlalchemy.core.models import Base


class FunnelModel(Base, UUIDMixin, TimeStampMixin):
    __tablename__ = 'funnels'

    name = Column(String(255), nullable=False)
    is_deleted = Column(Boolean, nullable=False, default=False)
