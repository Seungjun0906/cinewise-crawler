from sqlalchemy import Column, Integer, String, Text, Table, PrimaryKeyConstraint
from app.core.database import DatabaseManager

metadata = DatabaseManager.metadata

production_company_table = Table(
    "production_company",
    metadata,
    Column("company_id", Integer, nullable=False),
    Column("name", String(255), nullable=False),
    Column("logo_path", Text, nullable=True),
    Column("origin_country", String(10), nullable=True),
    PrimaryKeyConstraint("company_id"),
)
