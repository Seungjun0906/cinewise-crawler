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

content_production_company_table = Table(
    "content_production_company",
    metadata,
    Column("id", String(36), nullable=False, default=lambda: str(uuid.uuid4())),
    Column("content_id", Integer, nullable=False),
    Column("content_type", String, nullable=False),
    Column(
        "company_id",
        Integer,
        ForeignKey("production_company.company_id", ondelete="CASCADE"),
        nullable=False,
    ),
    PrimaryKeyConstraint("id"),
    UniqueConstraint(
        "content_id", "content_type", "company_id", name="uq_content_production_company"
    ),
)
