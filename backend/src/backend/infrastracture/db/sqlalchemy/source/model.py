from sqlalchemy import Column, String, Boolean
from sqlalchemy.dialects.postgresql import JSONB

from backend.infrastracture.db.sqlalchemy.core.mixins import UUIDMixin, TimeStampMixin
from backend.infrastracture.db.sqlalchemy.core.models import Base


class SourceModel(Base, UUIDMixin, TimeStampMixin):
    __tablename__ = 'sources'

    name = Column(String(255), nullable=False)
    source_type = Column(String(100), nullable=False)
    config = Column(JSONB, nullable=False, default=dict)
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)