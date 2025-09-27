# Simple test script for workflow validation
Write-Host "🔧 Testing Automated yt-dlp Workflows" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Green

# Test 1: Unit Tests (Always works)
Write-Host "`n🧪 Running workflow logic unit tests..." -ForegroundColor Blue
try {
    uv run python -m pytest tests/workflows/test_ytdlp_logic.py -v
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Unit tests passed!" -ForegroundColor Green
        $unitTestsPass = $true
    } else {
        Write-Host "❌ Unit tests failed" -ForegroundColor Red
        $unitTestsPass = $false
    }
} catch {
    Write-Host "❌ Error running unit tests" -ForegroundColor Red
    $unitTestsPass = $false
}

# Test 2: Check act availability
Write-Host "`n🎬 Checking act availability..." -ForegroundColor Blue
try {
    $actVersion = act --version 2>$null
    if ($actVersion) {
        Write-Host "✅ act is available: $actVersion" -ForegroundColor Green
        $actAvailable = $true
    } else {
        Write-Host "❌ act not found" -ForegroundColor Red
        $actAvailable = $false
    }
} catch {
    Write-Host "❌ act not installed or PATH not updated" -ForegroundColor Red
    Write-Host "   Install: winget install nektos.act" -ForegroundColor Yellow
    Write-Host "   Then restart terminal!" -ForegroundColor Yellow
    $actAvailable = $false
}

# Test 3: Check Docker (needed for act)
Write-Host "`n🐳 Checking Docker..." -ForegroundColor Blue
try {
    $dockerVersion = docker --version 2>$null
    if ($dockerVersion) {
        Write-Host "✅ Docker available: $dockerVersion" -ForegroundColor Green
        $dockerAvailable = $true
    } else {
        Write-Host "⚠️  Docker not found - act testing unavailable" -ForegroundColor Yellow
        $dockerAvailable = $false
    }
} catch {
    Write-Host "⚠️  Docker not installed - act testing unavailable" -ForegroundColor Yellow
    Write-Host "   Install: https://www.docker.com/products/docker-desktop/" -ForegroundColor White
    $dockerAvailable = $false
}

# Test 4: Try act if available
if ($actAvailable -and $dockerAvailable) {
    Write-Host "`n🚀 Testing with act..." -ForegroundColor Blue
    Write-Host "Available jobs:" -ForegroundColor Cyan
    act --list | Where-Object { $_ -like "*test-version-logic*" }

    Write-Host "`nRunning workflow test..." -ForegroundColor Blue
    try {
        act -j test-version-logic
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Act test passed!" -ForegroundColor Green
            $actTestPass = $true
        } else {
            Write-Host "❌ Act test failed" -ForegroundColor Red
            $actTestPass = $false
        }
    } catch {
        Write-Host "❌ Act test error" -ForegroundColor Red
        $actTestPass = $false
    }
} else {
    Write-Host "`n⚠️  Skipping act tests (requirements not met)" -ForegroundColor Yellow
    $actTestPass = $null
}

# Summary
Write-Host "`n📊 Test Summary:" -ForegroundColor Magenta
Write-Host "=================" -ForegroundColor Magenta
Write-Host "Unit Tests:     $(if ($unitTestsPass) { '✅ PASS' } else { '❌ FAIL' })" -ForegroundColor $(if ($unitTestsPass) { 'Green' } else { 'Red' })
Write-Host "Act Available:  $(if ($actAvailable) { '✅ YES' } else { '❌ NO' })" -ForegroundColor $(if ($actAvailable) { 'Green' } else { 'Red' })
Write-Host "Docker Ready:   $(if ($dockerAvailable) { '✅ YES' } else { '⚠️  NO' })" -ForegroundColor $(if ($dockerAvailable) { 'Green' } else { 'Yellow' })
if ($actTestPass -ne $null) {
    Write-Host "Act Testing:    $(if ($actTestPass) { '✅ PASS' } else { '❌ FAIL' })" -ForegroundColor $(if ($actTestPass) { 'Green' } else { 'Red' })
}

Write-Host "`n🎯 Recommendation:" -ForegroundColor Blue
if ($unitTestsPass) {
    Write-Host "✅ Workflow logic is validated - ready to deploy!" -ForegroundColor Green
    Write-Host "   The unit tests cover all the workflow logic completely." -ForegroundColor White
} else {
    Write-Host "❌ Fix unit test failures before deploying." -ForegroundColor Red
}

if (-not $actAvailable -or -not $dockerAvailable) {
    Write-Host "`n💡 For full act testing (optional):" -ForegroundColor Cyan
    if (-not $actAvailable) { Write-Host "   - Restart terminal after act installation" -ForegroundColor White }
    if (-not $dockerAvailable) { Write-Host "   - Install Docker Desktop" -ForegroundColor White }
}
