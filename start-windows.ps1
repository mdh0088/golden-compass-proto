Write-Host "🧭 황금나침반 프로토타입 시작..." -ForegroundColor Yellow

# Docker Desktop 실행 확인
$docker = Get-Process "Docker Desktop" -ErrorAction SilentlyContinue
if (-not $docker) {
    Write-Host "❌ Docker Desktop이 실행되지 않았습니다. Docker Desktop을 먼저 실행해주세요." -ForegroundColor Red
    exit 1
}

# .env 파일 확인
if (-not (Test-Path .env)) {
    Write-Host "⚠️  .env 파일이 없습니다. .env.example을 복사합니다..." -ForegroundColor Yellow
    Copy-Item .env.example .env
    Write-Host "📝 .env 파일에 API 키를 설정해주세요!" -ForegroundColor Red
    exit 1
}

# 미디어 디렉토리 생성
Write-Host "📁 디렉토리 생성 중..." -ForegroundColor Cyan
New-Item -ItemType Directory -Force -Path .\media\shorts | Out-Null
New-Item -ItemType Directory -Force -Path .\media\longform | Out-Null
New-Item -ItemType Directory -Force -Path .\media\thumbnails | Out-Null

# 이전 컨테이너 정리
Write-Host "🧹 이전 컨테이너 정리 중..." -ForegroundColor Cyan
docker-compose down

# 빌드 및 시작
Write-Host "🔨 컨테이너 빌드 및 시작 중..." -ForegroundColor Cyan
docker-compose up -d --build

# 잠시 대기
Write-Host "⏳ 서비스 시작 대기 중..." -ForegroundColor Cyan
Start-Sleep -Seconds 15

# 상태 확인
Write-Host "`n📊 컨테이너 상태:" -ForegroundColor Green
docker ps --format "table {{.Names}}\t{{.Status}}"

Write-Host "`n✅ 황금나침반이 실행되었습니다!" -ForegroundColor Green
Write-Host "📊 대시보드: http://localhost:3000" -ForegroundColor Yellow
Write-Host "📡 API 문서: http://localhost:8000/docs" -ForegroundColor Yellow
Write-Host "`n💡 종료하려면: .\stop-windows.ps1" -ForegroundColor Cyan
