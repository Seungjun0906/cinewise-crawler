from sqlalchemy import Column, Integer, Table, PrimaryKeyConstraint, String
from sqlalchemy import ForeignKey

from app.core.database import DatabaseManager

metadata = DatabaseManager.metadata

movie_genre_table = Table(
    "movie_genre",
    metadata,
    Column(
        "movie_id",
        Integer,
        ForeignKey("movie.movie_id", ondelete="CASCADE"),
        nullable=False,
    ),
    Column(
        "genre_id",
        Integer,
        ForeignKey("genre.genre_id", ondelete="CASCADE"),
        nullable=False,
    ),
    Column("content_type", String, nullable=False),
    PrimaryKeyConstraint("movie_id", "genre_id"),
)
