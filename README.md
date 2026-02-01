# 🚀 Reopfiy

An autonomous AI-powered Telegram bot that manages your GitHub repositories. Fix bugs, create features, make code changes, refactor code, and manage your entire codebase—all from your phone without needing a computer.

## ✨ Features

- 🐛 **Bug Fixes** - Analyze and fix production issues automatically
- ✨ **Feature Creation** - Build new functionality from natural language descriptions
- 🔧 **Code Changes** - Refactor, optimize, or update code on demand
- 🏗️ **Repository Management** - Handle configs, docs, tests, and scripts
- 🤖 **AI-Powered Analysis** - Works with Anthropic Claude, OpenRouter (400+ models), or Groq
- 🌿 **GitHub Integration** - Creates branches and pull requests automatically
- 💬 **Telegram Interface** - Manage your code from anywhere using just your phone
- ✅ **Review Before Apply** - You approve all changes before they're committed
- 📊 **Context-Aware** - Analyzes your repository structure and relevant files
- 📋 **System Prompts** - Configurable behavior guidelines (open source friendly)

## 📋 Documentation

- **[SYSTEM_PROMPT.md](SYSTEM_PROMPT.md)** - System behavior guidelines (easily customizable)
- **[INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md)** - How the system prompt integrates with code
- **[SYSTEM_PROMPT_IMPLEMENTATION.py](SYSTEM_PROMPT_IMPLEMENTATION.py)** - Code implementation examples
- **[PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md)** - Complete technical overview
- **[QUICKSTART.md](QUICKSTART.md)** - 5-minute setup guide
- **[USAGE_EXAMPLES.md](USAGE_EXAMPLES.md)** - Real-world usage examples
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Common issues & solutions
- **[DEPLOYMENT.md](docs/DEPLOYMENT.md)** - Railway and Vercel deployment guide

## 🚀 Quick Start

### Prerequisites

1. **Python 3.8+** installed
2. **Telegram Account** 
3. **That's it!** Everything else is added in Telegram

### Setup Instructions

#### 1. Create a Telegram Bot

1. Open Telegram and search for [@BotFather](https://t.me/botfather)
2. Send `/newbot` command
3. Follow the prompts to name your bot
4. Save the bot token (looks like `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

#### 2. Install the Bot

```bash
# Clone or download the files
cd reopfiy

# Install dependencies
pip install -r requirements.txt

# Create environment file with ONLY the Telegram token
echo "TELEGRAM_BOT_TOKEN=YOUR_BOT_TOKEN_HERE" > .env
```

Replace `YOUR_BOT_TOKEN_HERE` with your actual bot token from BotFather.

#### 3. Run the Bot

```bash
python repofiy_bot.py
```

You should see: `🚀 Reopfiy Bot started!`

---

#### 4. Add GitHub Token in Telegram (1 minute)

1. Open Telegram and find your bot
2. Send `/start` to see the welcome message
3. Get your GitHub personal access token:
   - Go to GitHub Settings → Developer Settings → Personal Access Tokens → [Tokens (classic)](https://github.com/settings/tokens)
   - Click "Generate new token (classic)"
   - Name it "Reopfiy"
   - Select `repo` scope (full control)
   - Generate and copy the token
4. Send in Telegram:
```
/settoken ghp_xxxxxxxxxxxxxxxxxxxx
```
Bot confirms: ✅ GitHub token saved!

---

#### 5. Choose Your AI Provider (1 minute)

Send in Telegram:
```
/setai
```

Choose one:
- **🌐 OpenRouter** - 400+ models (Claude, Llama, Mistral, etc.)
- **🧠 Anthropic** - Claude 3.5 Sonnet (highest quality)
- **⚡ Groq** - Mixtral 8x7b (fastest & free tier)

Bot shows a link to get an API key. Click it and copy the key from:
- **Anthropic**: https://console.anthropic.com/
- **OpenRouter**: https://openrouter.ai/keys
- **Groq**: https://console.groq.com/keys

Send your API key to the bot:
```
sk-ant-xxxxxxxxxxxxx
```
(or `sk-or-...` for OpenRouter or `gsk-...` for Groq)

Bot confirms: ✅ AI key saved!

---

#### 6. Set Your Repository

Send in Telegram:
```
/setrepo owner/repo
```

Example: `/setrepo johndoe/my-website`

You're ready to go! 🎉

## 📱 How to Use

### 1. Start a Conversation

Open Telegram and search for your bot (the username you chose with BotFather). Send `/start`

#### 2. Set Your AI Provider

```
/setai
```

Choose from the bot's menu:
- 🌐 **OpenRouter** (400+ models: Claude, Llama, Mistral)
- 🧠 **Anthropic** (Claude 3.5 Sonnet)
- ⚡ **Groq** (Mixtral 8x7b - fast & free)

When prompted, send your API key from the chosen provider.

### 3. Add Your GitHub Token

```
/settoken ghp_xxxxxxxxxxxxxxxxxxxxx
```

Get your token from: GitHub Settings → Developer Settings → Personal Access Tokens → Generate new token (classic)

### 4. Set Your Repository

```
/setrepo username/repository-name
```

Example: `/setrepo johndoe/my-web-app`

### 5. Request Changes (Multiple Options)

**Fix a Bug:**
```
/fix Users can't login - getting 401 error on auth endpoint
```

**Create a Feature:**
```
/feature Add dark mode toggle to settings
```

**Make Code Changes:**
```
/change Refactor auth service to use async/await
```

**Create New Files:**
```
/create New API endpoint for user profile
```

**Or just describe naturally:**
```
Users are complaining about slow login - let's optimize the auth
```

### 6. Review and Apply

The bot will:
1. 🔍 Analyze your repository code
2. 🤖 Use AI to understand your request
3. 💡 Propose specific changes
4. 📝 Show you the changes with a diff

You'll get buttons to:
- ✅ **Apply** - Creates a branch and pull request
- 🔄 **Revise** - Ask for changes to the proposal
- ❌ **Cancel** - Cancel the operation

### 7. Review the Pull Request

The bot creates a PR in your GitHub repository. Review it like any other PR:
- Check the code changes
- Run tests
- Merge when satisfied

## 🎯 Use Cases

### Emergency Production Fixes
You're away from your computer and production is down:
```
/fix Payment processing failing with 500 error
```

### Feature Development
You want to add functionality without opening an IDE:
```
/feature Add email verification to signup flow
```

### Code Optimization
Improve existing code on the fly:
```
/change Optimize database queries in user service
```

### Quick Patches
You're in a meeting and need a quick fix:
```
/fix Button on homepage has wrong color - should be #FF5733 not #FF0000
```

### Learning/Student Scenarios
You're in class and found a bug in your assignment:
```
/fix My sorting algorithm fails on arrays with duplicates
```

## 🔧 Commands

- `/start` - Show welcome message and help
- `/setai` - Choose AI provider (Anthropic, OpenRouter, Groq)
- `/settoken <token>` - Add or update GitHub token
- `/setrepo <owner/repo>` - Set the repository to work with
- `/view` - Browse repository files
- `/analyze` - Show repository structure
- `/fix <description>` - Fix a bug
- `/feature <description>` - Create new feature
- `/change <description>` - Make code changes
- `/create <description>` - Create new file/component
- `/status` - Check current operation status
- `/cancel` - Cancel current operation

## 🏗️ Architecture

```
┌─────────────┐
│  Telegram   │
│    User     │
└──────┬──────┘
       │ Describes request
       ▼
┌─────────────────────┐
│    Reopfiy Bot      │
│  (Python, Async)    │
└──────┬──────────────┘
       │
       ├─────────────────────┐────────────────┐
       │                     │                │
       ▼                     ▼                ▼
┌─────────────┐   ┌──────────────┐   ┌──────────────┐
│  GitHub     │   │ AI Provider  │   │ System       │
│  API        │   │ (Anthropic,  │   │ Prompt       │
└─────────────┘   │  OpenRouter, │   │ (SYSTEM_     │
       │          │  Groq)       │   │  PROMPT.md)  │
       │          └──────────────┘   └──────────────┘
       │                 │                   │
       ▼                 ▼                   ▼
   Create PR      Analyze & Propose   Guide Behavior
```

### Flow:

1. **User** sends request via Telegram
2. **Bot** reads SYSTEM_PROMPT.md for behavior guidelines
3. **Bot** fetches relevant code from GitHub
4. **AI Provider** (Claude/Llama/Mixtral) analyzes code + system prompt
5. **User** reviews proposed changes
6. **Bot** creates branch, commits, and opens PR on GitHub

## 💡 System Prompt (Open Source Feature)

Unlike closed-source solutions, Reopfiy's behavior is defined in **SYSTEM_PROMPT.md** - a human-readable file you can see, edit, and customize:

**Benefits:**
- ✅ Transparency - See exactly how the bot behaves
- ✅ Customizable - Modify for your team's needs
- ✅ Extensible - Add new request types easily
- ✅ Open Source Friendly - Fork and modify as needed

**To customize:**
1. Edit [SYSTEM_PROMPT.md](SYSTEM_PROMPT.md)
2. Bot automatically uses updated behavior
3. No code changes needed

**To integrate in your code:**
- See [INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md)
- See [SYSTEM_PROMPT_IMPLEMENTATION.py](SYSTEM_PROMPT_IMPLEMENTATION.py)

## ⚙️ Configuration

### Environment Variables (.env)

Your `.env` file only needs:

```env
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
```

**That's it!** GitHub and AI provider keys are added in Telegram via commands.

### Supported AI Providers

All providers are set up in Telegram with `/setai`. When you choose a provider, send your API key:

**Anthropic Claude (Best Quality)**
- Model: Claude 3.5 Sonnet
- Best for high-quality, accurate fixes
- ~$0.03 per fix
- [Get API Key](https://console.anthropic.com/)
- Command: `/setai` → Choose Anthropic → Paste key

**OpenRouter (Most Flexible)**
- 400+ models available (Claude, Llama, Mistral, etc.)
- Choose different models per request
- Auto-selects best model
- [Get API Key](https://openrouter.ai/keys)
- Command: `/setai` → Choose OpenRouter → Paste key

**Groq (Fastest & Free)**
- Model: Mixtral 8x7b
- Fastest inference
- Free tier available
- [Get API Key](https://console.groq.com/keys)
- Command: `/setai` → Choose Groq → Paste key

### Running in Production

For production deployment, see **[DEPLOYMENT.md](docs/DEPLOYMENT.md)** for detailed guides on:

1. **Railway** - Recommended for continuous bots (auto-deploys from GitHub)
2. **Vercel** - For serverless/API endpoints
3. **Docker** - Self-hosted deployment
4. **Systemd** - Process management on Linux

Quick systemd example:
```bash
sudo nano /etc/systemd/system/reopfiy.service
```

```ini
[Unit]
Description=Reopfiy Telegram Bot
After=network.target

[Service]
Type=simple
User=youruser
WorkingDirectory=/path/to/reopfiy
ExecStart=/usr/bin/python3 repofiy_bot.py
Restart=always
EnvironmentFile=/path/to/.env

[Install]
WantedBy=multi-user.target
```

Then start:
```bash
sudo systemctl enable reopfiy
sudo systemctl start reopfiy
```

**Logging:**
```bash
journalctl -u reopfiy -f  # systemd logs
tail -f bot.log            # or check bot.log
```

### Customization

You can customize the bot:

1. **Change AI Model** - Edit ANTHROPIC_API_KEY, GROQ_API_KEY, or OPENROUTER_API_KEY
2. **Modify System Prompt** - Edit [SYSTEM_PROMPT.md](SYSTEM_PROMPT.md) to change bot behavior
3. **Adjust Code Context** - Change how many files are analyzed in `get_code_context()`
4. **Modify PR Format** - Edit the PR template in `apply_fix()`
5. **Add Testing** - Integrate with CI/CD to run tests before creating PR

## 🔒 Security Best Practices

1. **Never commit `.env` file** - It contains secrets
2. **Use minimal GitHub permissions** - Only grant `repo` scope
3. **Rotate tokens regularly** - Change your API keys every 90 days
4. **Review all PRs** - Always review before merging bot-generated PRs
5. **Limit bot access** - Only use with repositories you control
6. **Monitor bot activity** - Check created PRs regularly

## 🐛 Troubleshooting

### Bot doesn't respond
- Check if the bot is running: `ps aux | grep repofiy_bot.py`
- Check logs for errors: `tail -f bot.log`
- Verify your Telegram token is correct

### Can't access GitHub repository
- Verify your GitHub token has `repo` permissions
- Check the repository name format: `owner/repo`
- Ensure the repository exists and you have access

### AI Provider API errors
- **Anthropic**: Check your API key is valid, verify you have credits
- **OpenRouter**: Check rate limiting, verify API key
- **Groq**: Check free tier limits, verify key validity
- Run `/setai` to reconfigure

### "Permission denied" errors
- Ensure your GitHub token has write access to the repository
- Check that the repository isn't archived
- Verify branch protection rules aren't blocking the bot

### Changes aren't working correctly
- Provide more specific request description
- Mention relevant file names or components
- Describe what you expect vs what's happening
- Use `/change` to refine instead of `/cancel`

## 📈 Limitations & Future Enhancements

### Current Limitations
- Analyzes limited number of files (performance)
- No automatic testing before PR creation
- Single repository per user session
- No support for monorepos or complex project structures

### Planned Features
- 🔄 Multi-repository support per user
- 🧪 Automatic test execution before PR
- 🔍 Advanced code search and analysis
- 📊 Fix success rate tracking
- 🎨 Web dashboard for monitoring
- 🔔 Proactive bug detection from logs
- 💬 Discord support

## 🤝 Contributing

Want to improve Reopfiy? Here's how:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

**Contribution areas:**
- Better file relevance detection
- Multi-repository support
- Automatic testing integration
- Discord/Slack support
- Web dashboard
- Documentation improvements

## 📄 License

MIT License - feel free to use, modify, and distribute for any purpose!

## 🆘 Support

Having issues?

1. Check the troubleshooting section above
2. Review the logs for error messages: `tail -f bot.log`
3. Open an issue on GitHub (if this becomes a public repo)
4. Read [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for detailed guides

## 🎓 Learning Resources

Want to understand how this works?

- [Telegram Bot API](https://core.telegram.org/bots/api)
- [GitHub REST API](https://docs.github.com/en/rest)
- [Anthropic Claude API](https://docs.anthropic.com/claude/reference/getting-started-with-the-api)
- [OpenRouter API Docs](https://openrouter.ai/docs)
- [Groq API Docs](https://console.groq.com/docs)
- [Python async/await](https://docs.python.org/3/library/asyncio.html)

## ⭐ Credits

Built with:
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) - Telegram integration
- [PyGithub](https://github.com/PyGithub/PyGithub) - GitHub API
- [Anthropic Python SDK](https://github.com/anthropics/anthropic-sdk-python) - Claude AI
- [OpenRouter API](https://openrouter.ai) - Multi-model AI
- [Groq API](https://groq.com) - Fast AI inference

---

**Made with ❤️ for developers who need to fix code from anywhere**

**Transform your GitHub workflow - manage your entire codebase from your phone**
