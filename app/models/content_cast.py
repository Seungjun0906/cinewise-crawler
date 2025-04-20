from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Table,
    PrimaryKeyConstraint,
    UniqueConstraint,
)
from app.core.database import DatabaseManager
import uuid

metadata = DatabaseManager.metadata

content_cast_table = Table(
    "content_cast",
    metadata,
    Column("id", String(36), nullable=False, default=lambda: str(uuid.uuid4())),
    Column("content_id", Integer, nullable=False),
    Column("content_type", String, nullable=False),
    Column(
        "person_id",
        Integer,
        ForeignKey("person.person_id", ondelete="CASCADE"),
        nullable=False,
    ),
    Column("character", String(255), nullable=True),
    Column("order", Integer, nullable=True),
    PrimaryKeyConstraint("id"),
    UniqueConstraint("content_id", "content_type", "person_id", name="uq_content_cast"),
)
