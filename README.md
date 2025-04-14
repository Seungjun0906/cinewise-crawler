# Cinewise Crawler

영화 정보를 TMDB API에서 수집하여 데이터베이스에 저장하는 크롤러 애플리케이션입니다.

## 기능

- TMDB API를 통한 영화 데이터 수집
- 장르 정보 수집 및 관리
- PostgreSQL 데이터베이스에 데이터 저장
- 비동기 API 요청 처리

## 프로젝트 구조

```
cinewise-crawler/
├── app/
│ ├── core/ # 설정 및 데이터베이스 연결
│ ├── models/ # 데이터 모델
│ ├── repositories/ # 데이터 저장소
│ ├── services/ # 비즈니스 로직
│ └── main.py # 애플리케이션 진입점
├── scripts/ # 유틸리티 스크립트
├── .env # 환경 변수 (git에서 제외됨)
└── Pipfile # 의존성 관리
```

## 기술 스택

- Python 3.8+
- SQLAlchemy (데이터베이스 ORM)
- aiohttp (비동기 HTTP 요청)
- PostgreSQL (데이터베이스)
