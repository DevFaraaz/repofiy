# 🔧 Troubleshooting Guide

This guide helps you resolve common issues with BugFixer Bot.

## Quick Diagnostics

Run this checklist first:

```bash
# 1. Check if bot is running
ps aux | grep bugfixer_bot.py

# 2. Check Python version (need 3.8+)
python3 --version

# 3. Verify environment variables are set
cat .env | grep -v '^#'

# 4. Test network connectivity
ping api.telegram.org
ping api.github.com
ping api.anthropic.com
```

---

## Common Issues & Solutions

### 1. Bot Doesn't Start

#### Symptom
```bash
python bugfixer_bot.py
# Nothing happens or immediate crash
```

#### Possible Causes & Solutions

**Missing Dependencies**
```bash
# Solution:
pip install -r requirements.txt --upgrade
```

**Invalid Environment Variables**
```bash
# Check .env file exists
ls -la .env

# Check contents (without revealing secrets)
cat .env

# Should show all three tokens:
# TELEGRAM_BOT_TOKEN=...
# GITHUB_TOKEN=...
# ANTHROPIC_API_KEY=...
```

**Python Version Too Old**
```bash
# Check version
python3 --version

# Should be 3.8 or higher
# If not, install newer Python or use pyenv
```

**Port Already in Use** (If running webhook mode)
```bash
# Check if port is in use
lsof -i :8443

# Kill the process
kill -9 <PID>
```

---

### 2. Bot Starts But Doesn't Respond

#### Symptom
Bot shows "🤖 BugFixer Bot started!" but doesn't respond to messages in Telegram

#### Possible Causes & Solutions

**Wrong Bot Token**
```bash
# Verify token format (should look like):
# 123456789:ABCdefGHIjklMNOpqrsTUVwxyz

# Get new token from @BotFather:
# 1. Message @BotFather
# 2. Send /mybots
# 3. Select your bot
# 4. Click "API Token"
```

**Bot Not Started in Telegram**
```
1. Open Telegram
2. Search for your bot username
3. Click "Start" button
4. Try sending a message
```

**Network/Firewall Issues**
```bash
# Test Telegram API connection
curl https://api.telegram.org/bot<YOUR_TOKEN>/getMe

# Should return JSON with bot info
# If timeout or error, check firewall/network
```

**Bot Polling Issue**
```python
# Check logs for:
# "Error while getting Updates"
# "Conflict: terminated by other getUpdates request"

# Solution: Make sure you don't have another instance running
ps aux | grep bugfixer_bot.py
# Kill other instances
pkill -f bugfixer_bot.py
# Restart
python bugfixer_bot.py
```

---

### 3. "Repository Not Found" or "Permission Denied"

#### Symptom
```
❌ Error accessing repository: 404 Not Found
```
or
```
❌ Error accessing repository: 403 Permission Denied
```

#### Solutions

**Verify Repository Name**
```
# Correct format:
/setrepo username/repo-name

# NOT:
/setrepo https://github.com/username/repo-name
/setrepo github.com/username/repo-name
```

**Check GitHub Token Permissions**
```
1. Go to: https://github.com/settings/tokens
2. Find your token
3. Click on it
4. Verify it has 'repo' scope checked
5. If not, regenerate token with correct permissions
```

**Token Expired or Revoked**
```
1. Generate new token at GitHub
2. Update .env file
3. Restart bot
```

**Repository is Private**
```
# Make sure your GitHub token has access to private repos
# The 'repo' scope should include private repository access
```

---

### 4. Claude API Errors

#### Symptom
```
❌ Error calling Claude API: ...
```

#### Common API Errors

**401 Unauthorized**
```
Error: 401 authentication_error

Solution:
1. Verify API key starts with 'sk-ant-'
2. Check for extra spaces in .env file
3. Generate new key at console.anthropic.com
```

**429 Too Many Requests**
```
Error: 429 rate_limit_error

Solution:
1. You're sending requests too quickly
2. Wait a few minutes
3. Consider upgrading your Anthropic plan
```

**400 Bad Request**
```
Error: 400 invalid_request_error

Solution:
1. Check code context isn't too large
2. Verify bug description is clear
3. Repository might have binary files causing issues
```

**402 Payment Required**
```
Error: 402 credit_limit_reached

Solution:
1. Add credits to your Anthropic account
2. Visit console.anthropic.com
3. Add payment method
```

---

### 5. "Error Applying Fix"

#### Symptom
Bot creates analysis but fails when applying fix

#### Solutions

**Branch Already Exists**
```
Error: Reference already exists

Solution:
1. Delete the branch in GitHub
2. Or wait for unique timestamp in branch name
3. Try fix again
```

**Protected Branch**
```
Error: Cannot push to protected branch

Solution:
1. Go to repository Settings → Branches
2. Check branch protection rules
3. Either:
   - Add bot as exception
   - Or have bot create PR instead of direct push
```

**No Write Access**
```
Error: Must have push access

Solution:
1. Verify GitHub token has 'repo' scope
2. Check you're a collaborator on the repository
3. For organization repos, check org permissions
```

**Merge Conflict**
```
Error: Merge conflict

Solution:
1. Bot tries to apply fix to outdated code
2. Pull latest changes
3. Try fix again
```

---

### 6. Bot Analyzes Wrong Files

#### Symptom
Bot looks at irrelevant files or misses the bug

#### Solutions

**Be More Specific**
```
❌ Bad:
"Login is broken"

✅ Good:
"In auth/login.js, the validatePassword function always returns false"
```

**Mention File Names**
```
"The bug is in components/UserProfile.jsx line 45"
```

**Provide Error Context**
```
"Getting error: 'Cannot read property id of undefined' in api/users.js:67"
```

**Repository Too Large**
```
If repo has 1000+ files:
1. Specify which directory/module
2. Example: "Bug in /backend/auth/ module"
```

---

### 7. Fix Doesn't Solve the Bug

#### Symptom
Bot creates PR but the bug persists

#### Why This Happens

1. **Incomplete Analysis** - Bot didn't see full context
2. **Complex Bug** - Requires multiple files/changes
3. **Wrong Root Cause** - Surface issue vs actual problem

#### Solutions

**Provide More Context**
```
You: The fix didn't work. The error still happens when...
Bot: [Analyzes with new info]
```

**Review and Modify PR**
```
1. Open the PR in GitHub
2. Add additional changes manually
3. Or close PR and request new fix with more details
```

**Break Down the Problem**
```
Instead of:
"Users can't complete checkout"

Try:
"Step 1: Fix cart total calculation in cart.js"
[Bot fixes]
"Step 2: Fix payment processing in payment.js"
[Bot fixes]
```

---

## Performance Issues

### Bot is Slow to Respond

**Large Repository**
```
Issue: Bot takes minutes to analyze

Solution:
- Bot fetches all files to find relevant ones
- For repos with 1000+ files, specify location:
  "Bug in /src/components/Auth.jsx"
```

**Rate Limiting**
```
Issue: Claude API calls are rate limited

Solution:
- Wait between requests
- Upgrade Anthropic plan for higher limits
```

**Network Latency**
```
Issue: Slow internet connection

Solution:
- Deploy bot on cloud server (AWS, DigitalOcean)
- Bot will have faster connection to APIs
```

---

## Logging & Debugging

### Enable Verbose Logging

Edit `bugfixer_bot.py`:

```python
# Change from INFO to DEBUG
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG  # Changed from INFO
)
```

### View Logs in Real-Time

```bash
# If running directly
python bugfixer_bot.py 2>&1 | tee bot.log

# If running as systemd service
journalctl -u bugfixer-bot -f

# If running in Docker
docker-compose logs -f
```

### Common Log Messages

**Normal Operation**
```
INFO - 🤖 BugFixer Bot started!
INFO - Update received from user: <user_id>
INFO - Analyzing bug: <description>
INFO - Fix proposal generated
INFO - PR created: #<number>
```

**Warning Signs**
```
WARNING - Rate limit approaching
WARNING - Large code context (>10000 chars)
WARNING - Unusual repository structure
```

**Errors to Investigate**
```
ERROR - Error calling Claude API: ...
ERROR - GitHub API error: ...
ERROR - Failed to parse fix proposal: ...
```

---

## Security Concerns

### Leaked Credentials

**If .env is committed to git:**
```bash
# 1. Remove from git history
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch .env" \
  --prune-empty --tag-name-filter cat -- --all

# 2. Force push (if safe to do so)
git push origin --force --all

# 3. IMMEDIATELY rotate all tokens:
# - Get new Telegram token from @BotFather
# - Generate new GitHub token
# - Generate new Anthropic API key
```

### Suspicious Activity

**Bot makes unauthorized changes:**
```
1. Immediately revoke GitHub token
2. Check bot logs for unusual activity
3. Review all recent PRs
4. Regenerate all API keys
5. Update .env with new keys
```

---

## Emergency Recovery

### Bot Goes Haywire

**Steps to take:**

```bash
# 1. STOP THE BOT IMMEDIATELY
pkill -9 -f bugfixer_bot.py

# 2. Check what it did
# - Review recent PRs in GitHub
# - Check recent commits
# - Look at bot logs

# 3. Rollback if needed
git revert <commit-hash>

# 4. Investigate logs
tail -100 bot.log

# 5. Only restart after fixing issue
```

---

## Getting Help

### Before Asking for Help

Gather this information:

```bash
# 1. Bot version
git log -1 --oneline

# 2. Python version
python3 --version

# 3. Installed packages
pip list

# 4. Recent logs
tail -50 bot.log

# 5. Error messages
grep ERROR bot.log
```

### Where to Get Help

1. **Check this guide first**
2. **Review README.md**
3. **Check USAGE_EXAMPLES.md**
4. **Search existing GitHub issues**
5. **Create new GitHub issue with:**
   - Problem description
   - Steps to reproduce
   - Logs (redact secrets!)
   - System info

---

## Prevention Tips

### Best Practices to Avoid Issues

✅ **Use Virtual Environment**
```bash
python3 -m venv venv
source venv/bin/activate
```

✅ **Keep Dependencies Updated**
```bash
pip install --upgrade -r requirements.txt
```

✅ **Rotate Tokens Regularly**
```
Every 90 days:
- Generate new GitHub token
- Generate new API keys
- Update .env
```

✅ **Monitor Bot Activity**
```
- Check PRs it creates
- Review code changes
- Watch for unusual patterns
```

✅ **Test in Development First**
```
- Use a test repository
- Verify fixes before production use
- Keep production and test tokens separate
```

✅ **Backup Configuration**
```bash
# (Without committing to git!)
cp .env .env.backup
```

---

## System Status Check Script

Save this as `check_health.sh`:

```bash
#!/bin/bash

echo "🏥 BugFixer Bot Health Check"
echo "=============================="
echo ""

# Check if bot is running
if pgrep -f bugfixer_bot.py > /dev/null; then
    echo "✅ Bot is running"
else
    echo "❌ Bot is NOT running"
fi

# Check environment file
if [ -f .env ]; then
    echo "✅ .env file exists"
    if grep -q "TELEGRAM_BOT_TOKEN=" .env && \
       grep -q "GITHUB_TOKEN=" .env && \
       grep -q "ANTHROPIC_API_KEY=" .env; then
        echo "✅ All tokens configured"
    else
        echo "❌ Missing tokens in .env"
    fi
else
    echo "❌ .env file missing"
fi

# Check network connectivity
if ping -c 1 api.telegram.org > /dev/null 2>&1; then
    echo "✅ Telegram API reachable"
else
    echo "❌ Cannot reach Telegram API"
fi

if ping -c 1 api.github.com > /dev/null 2>&1; then
    echo "✅ GitHub API reachable"
else
    echo "❌ Cannot reach GitHub API"
fi

if ping -c 1 api.anthropic.com > /dev/null 2>&1; then
    echo "✅ Anthropic API reachable"
else
    echo "❌ Cannot reach Anthropic API"
fi

# Check logs
if [ -f bot.log ]; then
    error_count=$(grep -c ERROR bot.log)
    echo "📊 Errors in log: $error_count"
    if [ $error_count -gt 10 ]; then
        echo "⚠️  High error count - check logs!"
    fi
else
    echo "ℹ️  No log file found"
fi

echo ""
echo "=============================="
echo "Health check complete!"
```

Make it executable:
```bash
chmod +x check_health.sh
./check_health.sh
```

---

## Still Having Issues?

If you've tried everything in this guide:

1. **Double-check the basics:**
   - All tokens are correct and valid
   - Bot has necessary permissions
   - Network connectivity is good

2. **Review the logs carefully:**
   - Enable DEBUG logging
   - Look for specific error messages
   - Google the exact error

3. **Start fresh:**
   - Backup your .env
   - Delete and reinstall bot
   - Use fresh virtual environment
   - Regenerate all tokens

4. **Ask for help:**
   - Provide detailed error info
   - Include relevant logs (redact secrets!)
   - Describe what you've already tried

---

**Remember: Most issues are simple configuration problems. Stay calm, check the basics, and you'll get it working! 💪**
