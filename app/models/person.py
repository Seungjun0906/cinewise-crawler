from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Date,
    Text,
    Table,
    PrimaryKeyConstraint,
)
from app.core.database import DatabaseManager

metadata = DatabaseManager.metadata

person_table = Table(
    "person",
    metadata,
    Column("person_id", Integer, nullable=False),
    Column("name_ko", String(255), nullable=False),
    Column("name_eng", String(255), nullable=False),
    Column("profile_path", Text, nullable=True),
    Column("birthday", Date, nullable=True),
    Column("deathday", Date, nullable=True),
    Column("gender", Integer, nullable=True),  # 1: female, 2: male
    Column("biography", Text, nullable=True),
    Column("place_of_birth", String(255), nullable=True),
    Column("popularity", Float, nullable=True),
    PrimaryKeyConstraint("person_id"),
)
