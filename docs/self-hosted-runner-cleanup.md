# Self-Hosted GitHub Actions Runner Cleanup Guide

## Overview
This guide helps you completely remove GitHub Actions self-hosted runner software and related components from your workstation after switching back to GitHub-hosted runners.

## Pre-Cleanup Checklist

### 1. Verify Repository Settings
- ✅ All workflows now use `ubuntu-latest` instead of conditional `self-hosted` runners
- ✅ No active jobs are currently running on your self-hosted runner
- ✅ Repository settings show no registered self-hosted runners

### 2. Check Runner Status
Before removing, verify the runner is offline in your GitHub repository:
1. Go to **Settings** → **Actions** → **Runners**
2. Look for any self-hosted runners listed
3. If any are "Online", stop the runner service first

---

## Windows Cleanup Steps

### Step 1: Stop the Runner Service
```powershell
# If you installed as a service
Stop-Service "actions.runner.*"
sc.exe delete "actions.runner.*"

# If you ran it manually, just stop the process
Get-Process | Where-Object {$_.Name -like "*Runner*"} | Stop-Process -Force
```

### Step 2: Remove Runner from GitHub
```powershell
# Navigate to your runner directory (typically where you extracted it)
cd C:\actions-runner  # or wherever you installed it

# Remove the runner (this requires the removal token from GitHub)
.\config.cmd remove --token YOUR_REMOVAL_TOKEN
```

**Getting the removal token:**
1. Go to **Settings** → **Actions** → **Runners** in your GitHub repo
2. Click on your self-hosted runner
3. Click **Remove** and copy the token provided
4. Use this token in the command above

### Step 3: Delete Runner Files
```powershell
# Remove the entire runner directory
Remove-Item -Recurse -Force C:\actions-runner
# Or whatever path you used during installation

# Remove any environment variables you may have set
[Environment]::SetEnvironmentVariable("ACTIONS_RUNNER_*", $null, "Machine")
```

### Step 4: Clean Up Windows Services (if applicable)
```powershell
# List any remaining Actions runner services
Get-Service | Where-Object {$_.Name -like "*actions*"}

# Remove any found services
sc.exe delete "service-name-here"
```

---

## macOS/Linux Cleanup Steps

### Step 1: Stop the Runner Service
```bash
# If running as a service
sudo systemctl stop actions.runner.*
sudo systemctl disable actions.runner.*

# If running manually, stop the process
pkill -f "Runner.Listener"
```

### Step 2: Remove Runner from GitHub
```bash
# Navigate to your runner directory
cd ~/actions-runner  # or wherever you installed it

# Remove the runner
./config.sh remove --token YOUR_REMOVAL_TOKEN
```

### Step 3: Delete Runner Files
```bash
# Remove the runner directory
rm -rf ~/actions-runner
# Or whatever path you used

# Clean up any systemd service files (Linux)
sudo rm -f /etc/systemd/system/actions.runner.*
sudo systemctl daemon-reload

# Clean up launchd files (macOS)
rm -f ~/Library/LaunchAgents/actions.runner.*
```

---

## Additional Cleanup Tasks

### 1. Remove Related Software (Optional)
If you installed software specifically for the self-hosted runner:

**Windows:**
```powershell
# Remove Git (if installed only for runner)
winget uninstall Git.Git

# Remove Visual Studio Build Tools (if installed only for runner)
winget uninstall Microsoft.VisualStudio.2022.BuildTools
```

**macOS/Linux:**
```bash
# Remove any packages installed specifically for the runner
# This depends on what you installed - be careful not to remove needed software
```

### 2. Clean Up Environment Variables
Check for and remove any environment variables you set up for the runner:
- `ACTIONS_RUNNER_*`
- `GITHUB_*`
- Custom PATH additions for runner tools

### 3. Remove SSH Keys (if created for runner)
If you created SSH keys specifically for the self-hosted runner:
```bash
# Remove runner-specific SSH keys
rm ~/.ssh/id_rsa_actions_runner*
```

### 4. Clean Up Firewall Rules
Remove any firewall rules you may have added for the runner:

**Windows:**
```powershell
# Remove firewall rules (adjust rule names as needed)
Remove-NetFirewallRule -DisplayName "*Actions Runner*"
```

**Linux:**
```bash
# Remove iptables rules (if any were added)
sudo iptables -L --line-numbers
# sudo iptables -D INPUT <line-number>
```

---

## Verification Steps

### 1. Confirm GitHub Repository
- Go to **Settings** → **Actions** → **Runners**
- Verify no self-hosted runners are listed
- Check that recent workflow runs use "ubuntu-latest" runners

### 2. Verify Local Cleanup
```powershell
# Windows - check for remaining processes
Get-Process | Where-Object {$_.Name -like "*Runner*" -or $_.Name -like "*actions*"}

# Check for remaining services
Get-Service | Where-Object {$_.Name -like "*actions*"}

# Verify directories are removed
Test-Path C:\actions-runner  # Should return False
```

```bash
# macOS/Linux - check for remaining processes
ps aux | grep -i runner
ps aux | grep -i actions

# Verify directories are removed
ls ~/actions-runner  # Should show "No such file or directory"
```

### 3. Test Workflows
After cleanup, trigger a workflow run to ensure:
- ✅ Jobs run on GitHub-hosted runners
- ✅ No errors related to runner availability
- ✅ All steps complete successfully

---

## Troubleshooting

### Runner Won't Remove from GitHub
- Ensure the runner is stopped first
- Try using a new removal token
- Contact GitHub support if the runner appears "stuck"

### Permission Errors During Cleanup
```powershell
# Windows - run as Administrator
# Take ownership of stubborn files
takeown /f C:\actions-runner /r /d y
icacls C:\actions-runner /grant Administrators:F /t
Remove-Item -Recurse -Force C:\actions-runner
```

```bash
# macOS/Linux - use sudo for protected files
sudo rm -rf /path/to/runner
```

### Remaining Background Processes
```powershell
# Windows - force kill any remaining processes
Get-Process | Where-Object {$_.Path -like "*actions-runner*"} | Stop-Process -Force
```

```bash
# macOS/Linux
sudo pkill -f actions-runner
sudo pkill -f Runner.Listener
```

---

## Cost Impact

**Before (Self-Hosted):**
- Hardware/electricity costs for your workstation
- Maintenance overhead
- Limited to your machine's availability

**After (GitHub-Hosted):**
- ✅ No hardware costs
- ✅ No maintenance overhead
- ✅ Reliable GitHub infrastructure
- ✅ Multiple OS support available
- ✅ Automatic updates and security patches

**Monthly GitHub Actions minutes:**
- Free tier: 2,000 minutes/month for private repos
- Your typical workflow: ~5-10 minutes per run
- Estimated runs per month: 200-400 (well within limits)

---

## Summary

✅ **What was accomplished:**
1. Updated all workflow files to use `ubuntu-latest`
2. Removed conditional self-hosted runner logic
3. Updated documentation and comments
4. Provided comprehensive cleanup guide

✅ **Next steps:**
1. Follow this cleanup guide to remove runner software
2. Remove runner from GitHub repository settings
3. Test a workflow run to verify GitHub-hosted runners work
4. Monitor GitHub Actions usage in repository insights

Your repository now uses GitHub-hosted runners exclusively, providing better reliability and removing the maintenance burden from your workstation.
