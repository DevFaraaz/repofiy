# 🚀 Quick Start Guide - Get Reopfiy Running in 5 Minutes!

## What You're Building
An AI-powered Telegram bot that manages your GitHub repositories. Fix bugs, create features, refactor code, and create new files—all from your phone!

## Prerequisites Checklist
- [ ] Python 3.8+ installed
- [ ] Telegram account
- [ ] 5 minutes of time

**That's it! You'll add GitHub and AI keys directly in the Telegram bot.**

---

## Step 1: Create Telegram Bot (2 minutes)

1. Open Telegram
2. Search for `@BotFather`
3. Send: `/newbot`
4. Choose a name: `Reopfiy`
5. Choose username: `reopfiy_bot` (must end in 'bot')
6. **Copy the token** (looks like `123456789:ABCdefGHI...`)

---

## Step 2: Set Up Environment (1 minute)

Create `.env` file with ONLY the Telegram bot token:

```bash
# .env file - MINIMAL setup
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
```

That's it! **No GitHub or AI keys needed here.**

---

## Step 3: Install and Start Bot (2 minutes)

```bash
# Go to the bot directory
cd reopfiy

# Run the setup script
chmod +x setup.sh
./setup.sh

# Start the bot
python bugfixer_bot.py
```

You should see:
```
🚀 Reopfiy Bot started!
```

**Keep this terminal window open!**

---

## Step 4: Test in Telegram (1 minute)

1. **Open Telegram** on your phone or computer
2. **Search** for your bot (the username you chose)
3. **Click "Start"**
4. **Send**: `/start`

You should get a welcome message showing all commands!

---

## Step 5: Add GitHub Token in Telegram (1 minute)

### Get GitHub Token First
1. Go to GitHub → Settings → Developer Settings → Personal Access Tokens
2. Click "Generate new token (classic)"
3. Name it: `Reopfiy`
4. Check the `repo` scope (full control)
5. Click "Generate" and **copy the token**

### Add It to the Bot
In Telegram, send:
```
/settoken ghp_xxxxxxxxxxxxxxxxxxxx
```

Bot will confirm: ✅ GitHub token saved!

---

## Step 6: Choose Your AI Provider (1 minute)

Send this command in Telegram:
```
/setai
```

Choose one:
- 🌐 **OpenRouter** (400+ models: Claude, Llama, Mistral, etc.)
- 🧠 **Anthropic** (Claude 3.5 Sonnet - highest quality)
- ⚡ **Groq** (Mixtral 8x7b - fastest & free tier)

The bot will show a link to get the API key. Click it and copy the key.

Send your API key to the bot:
```
sk-or-xxxxxxxxxxxxx
```
(or `sk-ant-...` for Anthropic or `gsk-...` for Groq)

Bot will confirm: ✅ AI key saved!

---

## Step 7: Set Your Repository (30 seconds)

Send:
```
/setrepo your-username/your-repo-name
```

Example: `/setrepo johndoe/my-website`

Bot confirms: ✅ Repository set to: **your-username/your-repo-name**

---

## Step 8: Try All 4 Features! (2 minutes)

### 🐛 Fix a Bug
```
/fix Login button color is wrong - should be blue not red
```

### ✨ Create a Feature
```
/feature Add dark mode toggle to settings
```

### 🔧 Refactor Code
```
/change Optimize database queries in user service
```

### 📝 Create New Files
```
/create New API endpoint for user profile
```

Bot will show the proposed changes with buttons:
- ✅ **Apply** - Creates branch + PR
- 🔄 **Revise** - Ask for changes
- ❌ **Cancel** - Cancel operation

---

## 🎉 Success!

You now have a fully working AI assistant for your GitHub repositories!

---

## All Commands Quick Reference

### Setup Commands (Do These First)
```
/start              - Show welcome message
/setai              - Choose AI provider (Anthropic, OpenRouter, or Groq)
/settoken <token>   - Add GitHub token (use actual token, not <token>)
/setrepo owner/repo - Set which repository to work with
```

### Request Commands (The Main Stuff)
```
/fix <description>      - Fix a bug
/feature <description>  - Create new feature
/change <description>   - Refactor/optimize code
/create <description>   - Create new file/component
```

### Utility Commands
```
/view       - Browse repository files
/analyze    - Show repository structure
/status     - Check current operation status
/cancel     - Cancel current operation
```

---

## .env File - That's All You Need

```env
# This is your complete .env file
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
```

**Everything else is added in Telegram via commands:**
- GitHub token → `/settoken`
- AI provider → `/setai` (then paste key when prompted)
- Repository → `/setrepo`

---

## Workflow: Step by Step

```
1. Run bot (python bugfixer_bot.py)
   ↓
2. Open Telegram and find your bot
   ↓
3. /start (see welcome message)
   ↓
4. /setai (choose provider, get link, paste key)
   ↓
5. /settoken (paste GitHub token)
   ↓
6. /setrepo (set repository)
   ↓
7. /fix, /feature, /change, or /create (make requests!)
   ↓
8. Approve changes in Telegram
   ↓
9. Review PR in GitHub
```

---

## Common First-Time Issues

**Bot doesn't respond:**
- Make sure the bot is running (check terminal)
- Verify you clicked "Start" in Telegram
- Check `TELEGRAM_BOT_TOKEN` in `.env` is correct

**"Invalid token" when setting GitHub:**
- Make sure you have `repo` scope selected
- Copy the full token (no spaces)
- Try generating a new one

**"Invalid API key" when setting AI provider:**
- Make sure you chose the right provider with `/setai` first
- Copy the full key from the provider's website
- Check for extra spaces

**"Repository not found":**
- Format must be: `owner/repo` (not a URL)
- Make sure you have access to the repository
- Verify GitHub token has `repo` permissions

**Want to change providers?**
- Just run `/setai` again and choose a different one
- Paste the new API key when prompted

**Want to change repository?**
- Run `/setrepo owner/new-repo`

---

## Pro Tips

💡 **Be specific** - "Login button returns 401 on /auth" works better than "login broken"

💡 **Include error messages** - Copy/paste actual errors when possible

💡 **One request at a time** - Don't send multiple requests in one message

💡 **Review before merging** - Always check the PR before merging to production

💡 **Try different providers** - Use `/setai` to test which AI provider works best for you

💡 **Customize behavior** - Edit `SYSTEM_PROMPT.md` to change how bot analyzes code

---

## Testing Locally First

Don't have a repo handy? Create a test one:

```bash
mkdir test-repo
cd test-repo
git init
echo "# Test Project" > README.md
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR-USERNAME/test-repo.git
git branch -M main
git push -u origin main
```

Then use `/setrepo YOUR-USERNAME/test-repo` in the bot.

---

## AI Provider Comparison

| Provider | Quality | Speed | Cost | Setup |
|----------|---------|-------|------|-------|
| **Anthropic** | ⭐⭐⭐⭐⭐ | Medium | ~$0.03/fix | `/setai` → Choose Anthropic → Get key → Paste |
| **OpenRouter** | ⭐⭐⭐⭐ | Variable | Varies | `/setai` → Choose OpenRouter → Get key → Paste |
| **Groq** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Free tier | `/setai` → Choose Groq → Get key → Paste |

**All setup is done in Telegram - no .env editing needed!**

---

## Emergency Stop

If something goes wrong:
```bash
# Stop the bot
Press Ctrl+C in the terminal

# Or force kill it
pkill -f bugfixer_bot.py
```

---

## Next Steps

1. ✅ Set everything up with the commands above
2. ✅ Try each request type (`/fix`, `/feature`, `/change`, `/create`)
3. ✅ Test with a real repository
4. ✅ Read `USAGE_EXAMPLES.md` for real-world examples
5. ✅ Bookmark `TROUBLESHOOTING.md` if you hit issues
6. ✅ Edit `SYSTEM_PROMPT.md` to customize behavior (optional)
7. ✅ Share with your team!

---

## Documentation

- **README.md** - Complete documentation
- **SYSTEM_PROMPT.md** - Customize bot behavior (advanced)
- **USAGE_EXAMPLES.md** - Real-world examples
- **TROUBLESHOOTING.md** - Problem solving
- **DOCS_INDEX.md** - Find anything quickly
- **INTEGRATION_GUIDE.md** - How system prompt works (for developers)

---

**You're all set! Happy coding! 🚀**

Everything is set up in Telegram - no config files needed!
