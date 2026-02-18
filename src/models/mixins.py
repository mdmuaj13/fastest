from datetime import datetime, timezone
import sqlalchemy as sa


class TimestampMixin:
    created_at = sa.Column(
        sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()
    )
    updated_at = sa.Column(
        sa.DateTime(timezone=True),
        nullable=False,
        server_default=sa.func.now(),
        onupdate=sa.func.now(),
    )

class SoftDeleteMixin:
    deleted_at = sa.Column(sa.DateTime(timezone=True), nullable=True)

    def soft_delete(self):
        self.deleted_at = datetime.now(timezone.utc)

    @classmethod
    def not_deleted(cls):
        return cls.deleted_at.is_(None)