# 개발 서버 실행 스크립트
Write-Host "🚀 Starting Golden Compass Backend..." -ForegroundColor Yellow

# 가상환경 활성화 확인
if (-not $env:VIRTUAL_ENV) {
    Write-Host "🔄 Activating virtual environment..." -ForegroundColor Cyan
    & .\.venv\Scripts\Activate.ps1
}

# 환경 변수 로드
if (Test-Path ..\.env) {
    Write-Host "📝 Loading environment variables..." -ForegroundColor Cyan
    Get-Content ..\.env | ForEach-Object {
        if ($_ -match '^([^=]+)=(.*)$') {
            [System.Environment]::SetEnvironmentVariable($matches[1], $matches[2])
        }
    }
}

# 데이터베이스 마이그레이션
Write-Host "🗄️ Running database migrations..." -ForegroundColor Cyan
alembic upgrade head

# 개발 서버 시작
Write-Host "✅ Starting development server..." -ForegroundColor Green
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
