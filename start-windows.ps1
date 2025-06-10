Write-Host "Starting Golden Compass Prototype..." -ForegroundColor Yellow

# Check if Docker Desktop is running
$docker = Get-Process "Docker Desktop" -ErrorAction SilentlyContinue
if (-not $docker) {
    Write-Host "Docker Desktop is not running. Please start Docker Desktop first." -ForegroundColor Red
    exit 1
}

# Check for .env file
if (-not (Test-Path .env)) {
    Write-Host ".env file not found. Copying from .env.example..." -ForegroundColor Yellow
    Copy-Item .env.example .env
    Write-Host "Please configure your API keys in the .env file." -ForegroundColor Red
    exit 1
}

# Create media directories
Write-Host "Creating media directories..." -ForegroundColor Cyan
New-Item -ItemType Directory -Force -Path .\media\shorts | Out-Null
New-Item -ItemType Directory -Force -Path .\media\longform | Out-Null
New-Item -ItemType Directory -Force -Path .\media\thumbnails | Out-Null

# Stop existing containers
Write-Host "Stopping existing containers..." -ForegroundColor Cyan
docker-compose down

# Build and start containers
Write-Host "Building and starting containers..." -ForegroundColor Cyan
docker-compose up -d --build

# Wait for services to initialize
Write-Host "Waiting for services to start..." -ForegroundColor Cyan
Start-Sleep -Seconds 15

# Show container status
Write-Host "`nContainer Status:" -ForegroundColor Green
docker ps --format "table {{.Names}}\t{{.Status}}"

Write-Host "`nGolden Compass is running." -ForegroundColor Green
Write-Host "Dashboard: http://localhost:3000" -ForegroundColor Yellow
Write-Host "API Docs: http://localhost:8000/docs" -ForegroundColor Yellow
Write-Host "`nTo stop services: .\stop-windows.ps1" -ForegroundColor Cyan

