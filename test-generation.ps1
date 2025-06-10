Write-Host "🧪 콘텐츠 생성 테스트..." -ForegroundColor Yellow

$headers = @{
    "Content-Type" = "application/json"
}

$body = @{
    topic = "2025년 2월 재물운"
    content_type = "both"
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri "http://localhost:8000/api/content/generate" `
        -Method Post `
        -Headers $headers `
        -Body $body
    
    Write-Host "✅ 태스크 ID: $($response.task_id)" -ForegroundColor Green
    Write-Host "📊 상태: $($response.status)" -ForegroundColor Cyan
    Write-Host "`n💡 대시보드에서 진행 상황을 확인하세요: http://localhost:3000" -ForegroundColor Yellow
}
catch {
    Write-Host "❌ 오류 발생: $_" -ForegroundColor Red
}
