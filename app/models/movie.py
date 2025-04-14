from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Boolean,
    Date,
    Text,
    Table,
    PrimaryKeyConstraint,
)
from app.core.database import DatabaseManager

metadata = DatabaseManager.metadata

movie_table = Table(
    "movie",
    metadata,
    Column("movie_id", Integer, nullable=False),
    Column("title_ko", String(255), nullable=False),
    Column("title_eng", String(255), nullable=False),
    Column("overview_ko", Text, nullable=True),
    Column("overview_eng", Text, nullable=True),
    Column("popularity", Float, nullable=True),
    Column("poster_path", Text, nullable=True),
    Column("backdrop_path", Text, nullable=True),
    Column("released_at", Date, nullable=True),
    Column("adult", Boolean, default=False),
    Column("vote_count", Integer, nullable=True),
    Column("vote_average", Float, nullable=True),
    PrimaryKeyConstraint("movie_id"),
)
