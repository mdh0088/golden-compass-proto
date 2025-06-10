FROM python:3.12-slim

WORKDIR /app

# UV 설치
RUN pip install uv

# 시스템 의존성 설치
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libpq-dev \
    gcc \
    git \
    && rm -rf /var/lib/apt/lists/*

# 프로젝트 파일 복사
COPY pyproject.toml .
COPY README.md .

# UV로 의존성 설치
RUN uv venv
RUN uv pip sync pyproject.toml

# 애플리케이션 코드 복사
COPY . .

# 환경변수 설정
ENV PATH="/app/.venv/bin:$PATH"

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
