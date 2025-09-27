# Test script for workflow validation
# This provides multiple ways to test the automated yt-dlp workflows

param(
    [string]$TestType = "unit"  # unit, act, all
)

function Test-WorkflowLogic {
    Write-Host "🧪 Testing workflow logic with unit tests..." -ForegroundColor Green

    try {
        $result = & uv run python -m pytest tests/workflows/test_ytdlp_logic.py -v --tb=short
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ All workflow logic tests passed!" -ForegroundColor Green
            return $true
        } else {
            Write-Host "❌ Workflow logic tests failed" -ForegroundColor Red
            return $false
        }
    } catch {
        Write-Host "❌ Error running workflow tests: $_" -ForegroundColor Red
        return $false
    }
}

function Test-ActAvailability {
    Write-Host "🔍 Checking act availability..." -ForegroundColor Blue

    try {
        $actVersion = & act --version 2>$null
        Write-Host "✅ act is installed: $actVersion" -ForegroundColor Green
        return $true
    } catch {
        Write-Host "❌ act not found. Install with: winget install nektos.act" -ForegroundColor Red
        Write-Host "   Then restart your terminal!" -ForegroundColor Yellow
        return $false
    }
}

function Test-DockerAvailability {
    Write-Host "🐳 Checking Docker availability..." -ForegroundColor Blue

    try {
        $dockerVersion = & docker --version 2>$null
        Write-Host "✅ Docker is installed: $dockerVersion" -ForegroundColor Green

        # Test Docker connectivity
        $dockerTest = & docker run --rm hello-world 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Docker is running and accessible" -ForegroundColor Green
            return $true
        } else {
            Write-Host "⚠️  Docker installed but not running. Start Docker Desktop." -ForegroundColor Yellow
            return $false
        }
    } catch {
        Write-Host "⚠️  Docker not found. Install Docker Desktop for act testing:" -ForegroundColor Yellow
        Write-Host "   https://www.docker.com/products/docker-desktop/" -ForegroundColor White
        return $false
    }
}

function Test-WithAct {
    Write-Host "🎬 Testing workflows with act..." -ForegroundColor Green

    if (-not (Test-ActAvailability)) { return $false }
    if (-not (Test-DockerAvailability)) { return $false }

    Write-Host "📋 Available jobs:" -ForegroundColor Cyan
    & act --list

    Write-Host "`n🚀 Testing workflow logic job..." -ForegroundColor Blue
    try {
        & act -j test-version-logic
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Act workflow test passed!" -ForegroundColor Green
            return $true
        } else {
            Write-Host "❌ Act workflow test failed" -ForegroundColor Red
            return $false
        }
    } catch {
        Write-Host "❌ Error running act: $_" -ForegroundColor Red
        return $false
    }
}

# Main execution
Write-Host "🔧 Workflow Testing Suite" -ForegroundColor Magenta
Write-Host "========================" -ForegroundColor Magenta

$success = $true

switch ($TestType.ToLower()) {
    "unit" {
        $success = Test-WorkflowLogic
    }
    "act" {
        $success = Test-WithAct
    }
    "all" {
        $success = Test-WorkflowLogic
        if ($success) {
            $success = Test-WithAct
        }
    }
    default {
        $success = Test-WorkflowLogic
    }
}

Write-Host "`n📝 Summary:" -ForegroundColor Cyan
if ($success) {
    Write-Host "✅ All selected tests passed!" -ForegroundColor Green
    Write-Host "`n🎯 Next steps:" -ForegroundColor Blue
    Write-Host "   - Merge the feature branch" -ForegroundColor White
    Write-Host "   - The automated workflows will start running on schedule" -ForegroundColor White
} else {
    Write-Host "❌ Some tests failed. Check the output above." -ForegroundColor Red
}

Write-Host "`n💡 Usage examples:" -ForegroundColor Cyan
Write-Host "   .\test-act.ps1 unit    # Test workflow logic only (fast)" -ForegroundColor White
Write-Host "   .\test-act.ps1 act     # Test with act (requires Docker)" -ForegroundColor White
Write-Host "   .\test-act.ps1 all     # Run both types of tests" -ForegroundColor White
