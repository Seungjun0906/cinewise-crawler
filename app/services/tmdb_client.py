import aiohttp
import asyncio
import backoff
from app.core.config import config


class TMDBClient:
    """TMDB API 비동기 클라이언트"""

    BASE_URL = "https://api.themoviedb.org/3"
    semaphore = asyncio.Semaphore(40)

    def __init__(self):
        """TMDB API 클라이언트 초기화"""
        self.headers = {
            "Authorization": f"Bearer {config.TMDB_ACCESS_TOKEN}",
            "Accept": "application/json",
        }
        self.session = None  # 세션을 동적으로 관리

    async def __aenter__(self):
        """비동기 컨텍스트 매니저 (자동 세션 생성)"""
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """비동기 컨텍스트 매니저 (자동 세션 종료)"""
        if self.session:
            await self.session.close()

    async def fetch(self, url: str, params: dict = None):
        """비동기 GET 요청 (재시도 로직 포함)"""
        async with self.semaphore:  # 동시 요청 제한
            async with self.session.get(
                url, headers=self.headers, params=params
            ) as res:
                if res.status == 429:  # 요청 제한 초과 시 대기 후 재시도
                    await asyncio.sleep(10)
                    return await self.fetch(url, params)

                res.raise_for_status()
                return await res.json()
