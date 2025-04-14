from dotenv import dotenv_values


class Config:
    """환경 변수 설정을 관리하는 클래스"""

    env = dotenv_values()

    DATABASE_URL = env.get("DB_URL")
    TMDB_ACCESS_TOKEN = env.get("TMDB_ACCESS_TOKEN")


config = Config()
