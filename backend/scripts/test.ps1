# 테스트 실행 스크립트
Write-Host "🧪 Running tests..." -ForegroundColor Yellow

# 가상환경 활성화
if (-not $env:VIRTUAL_ENV) {
    & .\.venv\Scripts\Activate.ps1
}

# 린터 실행
Write-Host "🔍 Running linters..." -ForegroundColor Cyan
ruff check app tests
black --check app tests

# 타입 체크
Write-Host "📝 Type checking..." -ForegroundColor Cyan
mypy app

# 테스트 실행
Write-Host "🧪 Running pytest..." -ForegroundColor Cyan
pytest -v
