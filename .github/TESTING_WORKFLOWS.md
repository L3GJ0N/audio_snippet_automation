# Testing GitHub Actions Locally with `act`

## Installation

### Windows (via Windows Package Manager - Recommended)
```powershell
# Install act
winget install nektos.act

# After installation, restart your terminal or open a new PowerShell window
# to refresh the PATH environment variable
```

### Windows (via Chocolatey)
```powershell
choco install act-cli
```

### Windows (Manual Download)
1. Download from: https://github.com/nektos/act/releases
2. Extract the `act.exe` file
3. Add the directory to your PATH or place in a directory already in PATH

### Linux/macOS
```bash
# Using Homebrew
brew install act

# Using curl (Linux)
curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash
```

## Important Notes for Windows Users

- **Restart Terminal**: After installation, you must restart your terminal/PowerShell window for `act` to be available
- **Docker Required**: `act` requires Docker Desktop to be installed and running
- **Path Issues**: If `act` is not found after restart, check your PATH environment variable

## Alternative Testing Methods (if act isn't working)

### 1. Direct pytest execution
```powershell
# Run our unit tests that validate workflow logic
uv run python -m pytest tests/workflows/test_ytdlp_logic.py -v
```

### 2. Manual workflow validation
```powershell
# Test the Python logic that workflows use
cd tests/workflows
python test_ytdlp_logic.py
```

### 3. GitHub Actions debugging
```yaml
# Add this step to any workflow for debugging
- name: Debug environment
  run: |
    echo "Current directory: $(pwd)"
    echo "Python version: $(python --version)"
    echo "yt-dlp version: $(yt-dlp --version)"
```

## Usage

### Quick Start (Recommended for Windows)

**Test workflow logic without Docker:**
```powershell
# Test all workflow logic with unit tests - works immediately
uv run python -m pytest tests/workflows/test_ytdlp_logic.py -v

# Test specific functionality
uv run python -c "
from tests.workflows.test_ytdlp_logic import *
t = TestVersionParsing()
t.test_version_comparison()
print('✅ Version logic works!')
"
```

### Advanced Testing with act (Requires Docker)

**List available jobs:**
```bash
act --list
```

**Test specific workflows:**
```bash
# Test the workflow logic validation
act -j test-version-logic

# Test integration workflow
act -j integration-test

# Test the basic update workflow
act workflow_dispatch -W .github/workflows/update-ytdlp.yml

# Test the health check workflow
act workflow_dispatch -W .github/workflows/update-ytdlp-health.yml
```

### Test with secrets (create .secrets file)
```bash
# Create .secrets file
echo "GITHUB_TOKEN=your_token_here" > .secrets

# Run with secrets
act -s GITHUB_TOKEN workflow_dispatch -W .github/workflows/update-ytdlp.yml
```

## Prerequisites

### Docker Desktop (Required)
`act` requires Docker to run GitHub Actions locally. Install Docker Desktop:

**Windows:**
1. Download from: https://www.docker.com/products/docker-desktop/
2. Install and start Docker Desktop
3. Ensure it's running (check system tray)

**Verify Docker:**
```powershell
docker --version
docker run hello-world
```

## Configuration

Create `.actrc` file in project root:
```
--container-architecture linux/amd64
--action-offline-mode
--reuse
--rm
```

## Troubleshooting

### Common Issues

1. **`act` command not found after installation**
   ```powershell
   # Restart PowerShell or open new terminal window
   # Or manually add to PATH: C:\Users\<username>\AppData\Local\Microsoft\WinGet\Packages\nektos.act_Microsoft.Winget.Source_8wekyb3d8bbwe
   ```

2. **"Could not find any stages to run" / Wrong job name**
   ```powershell
   # List all available jobs first
   act --list

   # Use correct job names:
   act -j test-version-logic    # ✅ Correct
   act -j test-ytdlp-logic      # ❌ Wrong
   ```

3. **Docker not installed or running**
   ```
   Error: Could not find any stages to run
   time="..." level=warning msg="Couldn't get a valid docker connection..."
   ```

   **Solutions:**
   - **Without Docker (Recommended):** Use unit tests instead:
     ```powershell
     uv run python -m pytest tests/workflows/test_ytdlp_logic.py -v
     ```

   - **With Docker:** Install Docker Desktop:
     1. Download from https://www.docker.com/products/docker-desktop/
     2. Install and start Docker Desktop
     3. Wait for Docker to be ready (check system tray)
     4. Test: `docker run hello-world`

2. **Docker not running**
   ```
   Error: Cannot connect to the Docker daemon
   ```
   - Start Docker Desktop and wait for it to be ready

3. **Permission issues**
   - Run PowerShell as Administrator if needed

4. **Workflow fails in act but works on GitHub**
   - Some GitHub Actions don't work locally
   - Use unit tests for logic validation instead

## Limitations
- No access to GitHub API (use mocks)
- Limited secret support
- Some actions may not work identically
- Windows containers not fully supported
