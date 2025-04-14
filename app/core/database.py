from contextlib import contextmanager
from sqlalchemy import create_engine, MetaData, Engine
from sqlalchemy.orm import sessionmaker, Session
from app.core.config import config


# 권장 방식
# # DB 엔진 생성
# engine = create_engine(config.DATABASE_URL)

# # 세션 팩토리 생성
# Session = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# # DB 스키마 정보를 저장하고 관리하는 객체
# metadata = MetaData()


class DatabaseManager:
    """DB 연결 및 세션 관리를 담당하는 클래스"""

    _engine: "Engine | None" = None
    _SessionLocal: "sessionmaker[Session] | None" = None
    metadata = MetaData()

    @classmethod
    def init(self) -> None:
        """데이터베이스 엔진 및 세션 팩토리를 초기화"""
        if self._engine is None:
            self._engine = create_engine(config.DATABASE_URL)
            self._SessionLocal = sessionmaker(
                bind=self._engine, autoflush=False, autocommit=False
            )

    @classmethod
    def get_session(self) -> Session:
        """새로운 데이터베이스 세션을 생성"""
        if self._SessionLocal is None:
            self.init()

        if self._SessionLocal is None:  # 여전히 None이면 예외 발생
            raise RuntimeError("DatabaseManager is not initialized properly.")

        # pylint: disable=E1102
        return self._SessionLocal()

    @classmethod
    @contextmanager
    def session_scope(self):
        """데이터베이스 세션을 컨텍스트 매니저로 제공"""
        session = self.get_session()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()


# 초기화 실행
DatabaseManager.init()
