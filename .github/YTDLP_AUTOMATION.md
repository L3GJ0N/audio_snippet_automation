# Automated yt-dlp Updates

This repository includes automated yt-dlp maintenance to ensure reliable YouTube downloading functionality.

## 🤖 How It Works

### Daily Health Checks
- **Schedule:** Daily at 8 AM UTC
- **Purpose:** Monitor yt-dlp functionality and detect breaking changes quickly
- **Actions:**
  - Tests current yt-dlp version
  - Checks for new releases
  - Performs real download test (optional)
  - Creates issues if problems are detected

### Automatic Updates
- **Schedule:** Mondays and Thursdays at 6 AM UTC (customizable)
- **Process:**
  1. Compares current version with latest release
  2. Updates `pyproject.toml` and `uv.lock`
  3. Runs all tests to ensure compatibility
  4. Performs real download verification
  5. Creates a Pull Request with detailed information

### Smart Failure Handling
- **Test Failures:** Automatically creates GitHub issues for manual intervention
- **API Limits:** Includes retry logic for GitHub API calls
- **Real-world Testing:** Verifies downloads work with actual YouTube videos

## 🔧 Configuration

Edit `.github/ytdlp-update-config.yml` to customize:
- Update frequency
- Test video URL
- PR creation settings
- Notification preferences

## 🚀 Manual Triggers

You can manually trigger updates:

```bash
# Via GitHub UI: Go to Actions → "yt-dlp Health Check & Update" → "Run workflow"
# Options available:
# - Force update even if versions match
# - Enable/disable real video testing
```

## 📊 What You'll See

### Successful Updates
- **Pull Requests:** Clearly labeled with version changes and test results
- **Commit Messages:** Structured format: `chore(deps): update yt-dlp to X.Y.Z`
- **Body Content:** Detailed change information and verification steps

### Failed Updates
- **GitHub Issues:** Automatically created with error details and recommended actions
- **Labels:** `🚨 urgent`, `🤖 automated`, `🔧 maintenance`
- **Assignee:** Repository owner (or configured user)

## 🛡️ Safety Features

1. **Test Suite:** All tests must pass before PR creation
2. **Real Download Test:** Verifies actual YouTube functionality
3. **Rollback Safe:** Updates only create PRs, no direct commits
4. **Issue Tracking:** Problems automatically reported
5. **Manual Override:** Force updates or disable via workflow inputs

## 🎯 Benefits

- ✅ **Always Compatible:** Stay current with YouTube API changes
- ✅ **Zero Maintenance:** Runs automatically without intervention
- ✅ **Safe Updates:** Thoroughly tested before deployment
- ✅ **Quick Recovery:** Issues detected and reported immediately
- ✅ **User Friendly:** Clear communication through PRs and issues

## 📱 Notifications

The system will:
- Create PRs for successful updates
- Generate issues for failures requiring attention
- Provide detailed logs in GitHub Actions
- Assign issues to repository maintainers

## 🔍 Monitoring

Check the status:
1. **Actions Tab:** View workflow run history
2. **Pull Requests:** Review pending updates
3. **Issues:** Check for any problems requiring attention
4. **Dependencies:** Monitor `pyproject.toml` for version changes
