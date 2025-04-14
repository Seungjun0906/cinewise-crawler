from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession
from app.models.movie import movie_table
from app.models.movie_genre import movie_genre_table
from app.models.genre import genre_table
from app.services.tmdb_client import TMDBClient
from app.core.database import DatabaseManager


class MovieService:
    """TMDB 영화 데이터 동기화 서비스"""

    VOTE_COUNT_RANGES = [
        {"gte": 500},  # FIRST
        {"gte": 400, "lte": 500},  # SECOND
        {"gte": 300, "lte": 400},  # THIRD
        {"gte": 200, "lte": 300},  # FORTH
        {"gte": 100, "lte": 200},  # FIFTH
        {"gte": 80, "lte": 100},  # SIXTH
        {"gte": 60, "lte": 80},  # SEVENTH
        {"gte": 40, "lte": 60},  # EIGTHTH
        {"gte": 20, "lte": 40},  # NINETH
        {"gte": 10, "lte": 20},  # TENTH
        {
            "gte": 0,
        },  # ELEVENTH
    ]

    CONTENT_TYPE = "MOVIE"

    async def fetch_movies(self, client: TMDBClient, page: int, vote_count_range: dict):
        """TMDB API에서 영화 목록 가져오기"""
        url = f"{TMDBClient.BASE_URL}/discover/movie"
        params = {
            "language": "ko",  # Set language to Korean
            "page": page,  # Pagination
            "primary_release_date.gte": "2025-03-30",
        }

        if "gte" in vote_count_range:
            params["vote_count.gte"] = vote_count_range["gte"]

        if "lte" in vote_count_range:
            params["vote_count.lte"] = vote_count_range["lte"]

        print(f"Fetching page {page} with vote_count range {vote_count_range}")

        data = await client.fetch(url, params=params)

        return data.get("results", [])

    async def insert_movies(self, db: AsyncSession, movies: list):
        """DB에 영화 데이터 삽입 (UPSERT 적용)"""
        try:
            for movie in movies:
                record = {
                    "movie_id": movie["id"],
                    "title_ko": movie["title"],
                    "title_eng": movie["original_title"],
                    "overview_ko": movie["overview"],  # Korean overview
                    "overview_eng": None,  # You can fetch English overview if needed
                    "popularity": movie.get("popularity", None),
                    "poster_path": movie.get("poster_path", None),
                    "backdrop_path": movie.get("backdrop_path", None),
                    "released_at": movie.get("release_date", None) or None,
                    "adult": movie.get("adult", False),
                    "vote_count": movie.get("vote_count", None),
                    "vote_average": movie.get("vote_average", None),
                }
                # Statement for UPSERT (insert or update on conflict)
                stmt = (
                    insert(movie_table)
                    .values(record)
                    .on_conflict_do_update(
                        index_elements=[
                            "movie_id"
                        ],  # Index on movie_id for conflict resolution
                        set_={key: record[key] for key in record.keys()},
                    )
                )

                db.execute(stmt)  # Execute async statement

                # 2️⃣ 장르 정보 저장 (다대다 관계)
                genre_ids = movie.get("genre_ids", [])

                for genre_id in genre_ids:
                    # genre 테이블에 존재하는지 확인

                    result = db.execute(
                        select(1).where((genre_table.c.get("genre_id") == genre_id))
                    )

                    genre_exists = result.scalar() is not None

                    if genre_exists:
                        genre_stmt = (
                            insert(movie_genre_table)
                            .values(
                                {
                                    "movie_id": movie["id"],
                                    "genre_id": genre_id,
                                    "content_type": self.CONTENT_TYPE,
                                }
                            )
                            .on_conflict_do_nothing()
                        )
                        db.execute(genre_stmt)

            db.commit()  # Commit the transaction explicitly

        except Exception:
            db.rollback()  # Rollback if any error occurs
            raise

    async def fetch_and_insert_movies(self):
        """영화 데이터를 TMDB에서 가져와 DB에 저장"""
        async with TMDBClient() as client:
            db = DatabaseManager.get_session()

            try:
                for vote_range in self.VOTE_COUNT_RANGES:
                    page = 1
                    while page <= 500:
                        movies = await self.fetch_movies(client, page, vote_range)
                        if not movies:
                            break  # No more results, stop this range

                        await self.insert_movies(db, movies)
                        page += 1  # Next page

            finally:
                db.close()
