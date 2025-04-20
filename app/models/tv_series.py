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

tv_series_table = Table(
    "tv_series",
    metadata,
    Column("tv_series_id", Integer, nullable=False),
    Column("title_ko", String(255), nullable=False),
    Column("title_eng", String(255), nullable=False),
    Column("overview_ko", Text, nullable=True),
    Column("overview_eng", Text, nullable=True),
    Column("popularity", Float, nullable=True),
    Column("poster_path", Text, nullable=True),
    Column("backdrop_path", Text, nullable=True),
    Column("first_air_date", Date, nullable=True),
    Column("last_air_date", Date, nullable=True),
    Column("adult", Boolean, default=False),
    Column("vote_count", Integer, nullable=True),
    Column("vote_average", Float, nullable=True),
    Column("number_of_seasons", Integer, nullable=True),
    Column("number_of_episodes", Integer, nullable=True),
    Column("status", String(50), nullable=True),
    PrimaryKeyConstraint("tv_series_id"),
)
