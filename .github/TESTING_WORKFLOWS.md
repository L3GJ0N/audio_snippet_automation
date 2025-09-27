# Testing GitHub Actions Locally with `act`

## Installation

### Windows (via Chocolatey)
```powershell
choco install act-cli
```

### Windows (via Winget)
```powershell
winget install nektos.act
```

### Alternative: Download from releases
https://github.com/nektos/act/releases

## Usage

### Test the basic update workflow
```bash
# Test the update-ytdlp workflow
act workflow_dispatch -W .github/workflows/update-ytdlp.yml

# Test with specific event
act schedule -W .github/workflows/update-ytdlp.yml

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

### Test specific job
```bash
# Test only the update job
act -j update workflow_dispatch -W .github/workflows/update-ytdlp-health.yml
```

## Configuration

Create `.actrc` file in project root:
```
--container-architecture linux/amd64
--action-offline-mode
--reuse
--rm
```

## Limitations
- No access to GitHub API (use mocks)
- Limited secret support
- Some actions may not work identically
