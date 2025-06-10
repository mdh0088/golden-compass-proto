# Golden Compass Backend

황금나침반 콘텐츠 생성 시스템 백엔드

## 개발 환경 설정

```bash
# UV 설치
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# 가상환경 생성
uv venv --python 3.12

# 의존성 설치
uv pip sync pyproject.toml
