# MedicareCallForge - Verify Both Revenue Streams (Easy Local Verification)
# Run this after starting the service to confirm both monetization paths work end-to-end.

Write-Host "=== MedicareCallForge - Dual Stream Verification ===" -ForegroundColor Cyan
Write-Host ""

$serviceRunning = $false
try {
    $health = Invoke-RestMethod -Uri "http://localhost:8000/health" -Method Get -TimeoutSec 5
    if ($health.status -eq "healthy") {
        $serviceRunning = $true
        Write-Host "Service is running and healthy." -ForegroundColor Green
    }
} catch {
    Write-Host "ERROR: Service not running on http://localhost:8000" -ForegroundColor Red
    Write-Host "Please start it first with:" -ForegroundColor Yellow
    Write-Host "  cd C:\Users\lang2\MedicareCallForge" -ForegroundColor Yellow
    Write-Host "  uvicorn src.medicare_call_forge.app:app --reload" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "Running dual-stream simulator..." -ForegroundColor Cyan
python examples/full_flow_simulator.py

Write-Host ""
Write-Host "=== Verification Complete ===" -ForegroundColor Green
Write-Host "If you saw one path routed to 'enroll_in_house' and one to 'sell_call', both streams are working." -ForegroundColor White
Write-Host ""
Write-Host "Next steps for real pilot:" -ForegroundColor Yellow
Write-Host "1. Wire real GHL + Twilio webhooks" -ForegroundColor Yellow
Write-Host "2. Connect live agent handoff" -ForegroundColor Yellow
Write-Host "3. Replace economics stub with your real PNL models" -ForegroundColor Yellow
Write-Host "4. Execute red-team mitigations before turning on budget" -ForegroundColor Yellow
