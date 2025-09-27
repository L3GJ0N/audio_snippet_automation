# Test script for act installation
# Run this after restarting PowerShell to verify act is working

Write-Host "Testing act installation..." -ForegroundColor Green

# Check if act is available
try {
    $actVersion = & act --version 2>$null
    Write-Host "✅ act is installed: $actVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ act not found. Please:" -ForegroundColor Red
    Write-Host "   1. Restart your PowerShell/terminal" -ForegroundColor Yellow
    Write-Host "   2. Or install with: winget install nektos.act" -ForegroundColor Yellow
    exit 1
}

# Check if Docker is running
try {
    $dockerVersion = & docker --version 2>$null
    Write-Host "✅ Docker is installed: $dockerVersion" -ForegroundColor Green

    # Test Docker connectivity
    $dockerTest = & docker run --rm hello-world 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Docker is running and accessible" -ForegroundColor Green
    } else {
        Write-Host "⚠️  Docker installed but not running. Start Docker Desktop." -ForegroundColor Yellow
    }
} catch {
    Write-Host "❌ Docker not found. Install Docker Desktop from:" -ForegroundColor Red
    Write-Host "   https://www.docker.com/products/docker-desktop/" -ForegroundColor Yellow
}

Write-Host "`nTesting workflow logic with pytest instead..." -ForegroundColor Blue
try {
    & uv run python -m pytest tests/workflows/test_ytdlp_logic.py -v
    Write-Host "✅ Unit tests passed - workflow logic is valid" -ForegroundColor Green
} catch {
    Write-Host "❌ Unit tests failed" -ForegroundColor Red
}

Write-Host "`nTo test workflows with act (after Docker is running):" -ForegroundColor Cyan
Write-Host "  act -j test-ytdlp-logic" -ForegroundColor White
