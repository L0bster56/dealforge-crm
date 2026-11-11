

from sqlalchemy import Column, String, Boolean, CheckConstraint, Index, text, Integer, UUID, ForeignKey

from backend.infrastracture.db.sqlalchemy.core.mixins import UUIDMixin, TimeStampMixin
from backend.infrastracture.db.sqlalchemy.core.models import Base


class LeadCustomFieldModel(Base, UUIDMixin, TimeStampMixin):
    __tablename__ = 'lead_custom_field'

    name = Column(String(512))
    field_type = Column(String(20))
    is_deleted = Column(Boolean, default=False)

    __table_args__ = (
        CheckConstraint(
            "field_type IN ('text', 'number', 'date', 'select_one', 'select_all', 'boolean')",
            name="ck_lead_custom_field_type"
        ),
        Index(
            "uq_lead_custom_fields_active",
            "name",
            unique=True,
            postgresql_where=text("is_deleted = False"),
        )
    )

class LeadCustomFieldEnumModel(Base, UUIDMixin):
    __tablename__ = 'lead_custom_field_enum'

    custom_field_id = Column(UUID(as_uuid=True), ForeignKey('lead_custom_field.id', ondelete="CASCADE"), nullable=False)
    value = Column(String(255), nullable=False)