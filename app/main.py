import sys
import os
import asyncio


from app.services.genre_service import GenreService
from app.services.movie_service import MovieService

sys.path.append(os.path.abspath(os.path.dirname(__file__)))  # 현재 디렉토리 추가


async def main():
    # genre_service = GenreService()
    # await genre_service.fetch_and_insert_genres()

    movie_service = MovieService()
    await movie_service.fetch_and_insert_movies()
    print("🎬 Genres updated successfully!")


if __name__ == "__main__":
    asyncio.run(main())
