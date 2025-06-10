Write-Host "Running content generation test..." -ForegroundColor Yellow

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

    Write-Host "Task ID: $($response.task_id)" -ForegroundColor Green
    Write-Host "Status: $($response.status)" -ForegroundColor Cyan
    Write-Host "Check the dashboard for progress: http://localhost:3000" -ForegroundColor Yellow
}
catch {
    Write-Host "Error occurred: $_" -ForegroundColor Red
}

