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

content_crew_table = Table(
    "content_crew",
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
    Column("department", String, nullable=False),
    Column("job", String(100), nullable=False),
    PrimaryKeyConstraint("id"),
    UniqueConstraint(
        "content_id", "content_type", "person_id", "job", name="uq_content_crew"
    ),
)
