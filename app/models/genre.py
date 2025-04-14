from sqlalchemy import Column, Integer, String, Table, PrimaryKeyConstraint
from app.core.database import DatabaseManager

metadata = DatabaseManager.metadata

genre_table = Table(
    "genre",
    metadata,
    Column("genre_id", Integer, nullable=False),
    Column("content_type", String, nullable=False),  # CHECK 제약 조건 적용 필요
    Column("genre_name_ko", String, nullable=False),
    Column("genre_name_eng", String, nullable=True),
    PrimaryKeyConstraint("genre_id", "content_type"),
)
