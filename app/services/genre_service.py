from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.genre import genre_table
from app.services.tmdb_client import TMDBClient
from app.core.database import DatabaseManager


class GenreService:
    """TMDB 장르 데이터 동기화 서비스"""

    async def fetch_genres(self, client: TMDBClient, content_type: str):
        """TMDB API에서 장르 목록 가져오기"""
        url = f"{TMDBClient.BASE_URL}/genre/{content_type}/list"

        data = await client.fetch(url, params={"language": "ko"})

        return data.get("genres", [])

    async def insert_genres(self, db: AsyncSession, genres: list, content_type: str):
        """DB에 장르 데이터 삽입 (UPSERT 적용)"""
        # txn = await db.begin()  # 명시적으로 트랜잭션 시작

        try:
            for genre in genres:
                record = {
                    "genre_id": genre["id"],
                    "genre_name_ko": genre["name"],
                    "genre_name_eng": None,
                    "content_type": content_type,
                }
                # statement
                stmt = (
                    insert(genre_table)
                    .values(record)
                    .on_conflict_do_update(
                        index_elements=["genre_id", "content_type"],
                        set_={"genre_name_ko": record["genre_name_ko"]},
                    )
                )

                db.execute(stmt)

            db.commit()  # 명시적 커밋

        except Exception:
            db.rollback()  # 오류 발생 시 롤백
            raise

    async def fetch_and_insert_genres(self):
        """장르 데이터를 TMDB에서 가져와 DB에 저장"""
        async with TMDBClient() as client:
            db = DatabaseManager.get_session()

            try:
                movie_genres = await self.fetch_genres(client, "movie")
                tv_genres = await self.fetch_genres(client, "tv")

                await self.insert_genres(db, movie_genres, "MOVIE")
                await self.insert_genres(db, tv_genres, "TV_SHOW")

            finally:
                db.close()
