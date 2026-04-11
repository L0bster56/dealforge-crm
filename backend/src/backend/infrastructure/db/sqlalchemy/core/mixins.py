import datetime
import uuid

from sqlalchemy import Column, BigInteger, UUID, DateTime, Boolean


class UUIDMixin:
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

class IntIdMixin:
    id = Column(BigInteger, primary_key=True, autoincrement=True)

class TimestampMixin:
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)

class ActiveMixin:
    is_active = Column(Boolean, default=True)