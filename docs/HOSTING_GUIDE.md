# 🌐 Hosting Guide for BugFixer Bot

## Understanding Telegram Bot Hosting

**Important:** Telegram bots are NOT hosted on Telegram itself. You need to run your Python bot somewhere that can:
- Run 24/7
- Connect to the internet
- Execute Python code

The bot connects to Telegram's API to receive and send messages.

---

## Option 1: Your Own Computer (Free, Testing Only)

### ✅ Best For
- Testing and development
- Personal use when your computer is on
- Learning how it works

### ❌ Limitations
- Stops when computer sleeps
- Stops when you close laptop
- Not accessible 24/7

### Setup
```bash
# Just run it!
python bugfixer_bot.py

# Keep terminal open
# Bot runs until you close terminal or shutdown computer
```

### Keep It Running (Mac/Linux)
```bash
# Run in background
nohup python bugfixer_bot.py &

# Or use screen
screen -S bugfixer
python bugfixer_bot.py
# Press Ctrl+A then D to detach
```

**Cost:** Free
**Difficulty:** ⭐ (1/5)

---

## Option 2: Replit (Free, Easy Cloud Hosting)

### ✅ Best For
- Beginners
- No credit card needed
- Quick deployment
- Learning

### Step-by-Step Setup

1. **Go to Replit**
   - Visit https://replit.com
   - Sign up for free account

2. **Create New Repl**
   - Click "Create Repl"
   - Choose "Python" template
   - Name it "bugfixer-bot"

3. **Upload Files**
   - Upload `bugfixer_bot.py`
   - Upload `requirements.txt`
   - Create `.env` file (using Secrets feature)

4. **Add Environment Variables**
   - Click "Tools" → "Secrets"
   - Add your three tokens:
     ```
     TELEGRAM_BOT_TOKEN = your_token
     GITHUB_TOKEN = your_token
     ANTHROPIC_API_KEY = your_token
     ```

5. **Install Dependencies**
   - Replit auto-installs from requirements.txt
   - Or click "Packages" and add them manually

6. **Run the Bot**
   - Click "Run" button
   - Bot starts and stays running!

7. **Keep It Always On (Optional)**
   - Replit free tier sleeps after inactivity
   - Upgrade to "Always On" for $7/month
   - Or use a free uptime service (see below)

### Keep Free Replit Awake

Create `keep_alive.py`:
```python
from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()
```

Modify `bugfixer_bot.py`:
```python
from keep_alive import keep_alive

def main():
    # ... existing code ...
    keep_alive()  # Add this line
    bot.run()
```

Then use UptimeRobot (free) to ping your Repl every 5 minutes.

**Cost:** Free (with limitations) or $7/month
**Difficulty:** ⭐⭐ (2/5)

---

## Option 3: PythonAnywhere (Free, Easy)

### ✅ Best For
- Python-specific hosting
- Free tier available
- Easy for beginners
- Good free limits

### Step-by-Step Setup

1. **Sign Up**
   - Go to https://www.pythonanywhere.com
   - Create free account

2. **Upload Code**
   - Go to "Files" tab
   - Create new directory: `bugfixer-bot`
   - Upload all your files

3. **Install Dependencies**
   - Go to "Consoles" tab
   - Open "Bash console"
   ```bash
   cd bugfixer-bot
   pip3.10 install --user -r requirements.txt
   ```

4. **Set Environment Variables**
   - Edit your .env file or use:
   ```bash
   echo 'TELEGRAM_BOT_TOKEN=your_token' >> .env
   echo 'GITHUB_TOKEN=your_token' >> .env
   echo 'ANTHROPIC_API_KEY=your_token' >> .env
   ```

5. **Create Always-On Task**
   - Go to "Tasks" tab
   - Create new task:
   ```
   python3.10 /home/yourusername/bugfixer-bot/bugfixer_bot.py
   ```
   - Set to run daily at specific time (free tier limitation)

### Free Tier Limitations
- Task runs at specific time only
- Need to restart daily
- Limited CPU time

### Upgrade for Always-On
- $5/month for "Hacker" plan
- Always-on processes
- More CPU time

**Cost:** Free (limited) or $5/month
**Difficulty:** ⭐⭐ (2/5)

---

## Option 4: DigitalOcean / AWS / VPS (Best for Production)

### ✅ Best For
- Production use
- 24/7 reliability
- Full control
- Team use

### Quick Setup (DigitalOcean Example)

1. **Create Droplet**
   - Sign up at https://digitalocean.com
   - Create new Droplet
   - Choose: Ubuntu 22.04
   - Select: Basic plan ($4-6/month)
   - Choose datacenter near you

2. **SSH into Server**
   ```bash
   ssh root@your_droplet_ip
   ```

3. **Install Python & Dependencies**
   ```bash
   apt update
   apt install python3 python3-pip git -y
   ```

4. **Upload Your Code**
   ```bash
   # Option A: Use git
   git clone your-repo-url
   cd bugfixer-bot
   
   # Option B: Use SCP from your computer
   scp -r /path/to/bugfixer-bot root@your_ip:/root/
   ```

5. **Install Dependencies**
   ```bash
   pip3 install -r requirements.txt
   ```

6. **Setup Environment Variables**
   ```bash
   nano .env
   # Paste your tokens
   # Save: Ctrl+X, Y, Enter
   ```

7. **Create Systemd Service** (Makes it auto-start)
   ```bash
   nano /etc/systemd/system/bugfixer-bot.service
   ```
   
   Paste this:
   ```ini
   [Unit]
   Description=BugFixer Telegram Bot
   After=network.target

   [Service]
   Type=simple
   User=root
   WorkingDirectory=/root/bugfixer-bot
   ExecStart=/usr/bin/python3 bugfixer_bot.py
   Restart=always
   RestartSec=10

   [Install]
   WantedBy=multi-user.target
   ```

8. **Start the Service**
   ```bash
   systemctl daemon-reload
   systemctl enable bugfixer-bot
   systemctl start bugfixer-bot
   ```

9. **Check Status**
   ```bash
   systemctl status bugfixer-bot
   
   # View logs
   journalctl -u bugfixer-bot -f
   ```

### Management Commands
```bash
# Start bot
systemctl start bugfixer-bot

# Stop bot
systemctl stop bugfixer-bot

# Restart bot
systemctl restart bugfixer-bot

# View logs
journalctl -u bugfixer-bot -f

# Check status
systemctl status bugfixer-bot
```

**Cost:** $4-6/month
**Difficulty:** ⭐⭐⭐ (3/5)

---

## Option 5: Docker Deployment (Advanced)

### ✅ Best For
- DevOps enthusiasts
- Easy deployment/updates
- Portable setup

### On Any Server with Docker

1. **Install Docker**
   ```bash
   curl -fsSL https://get.docker.com -o get-docker.sh
   sh get-docker.sh
   ```

2. **Upload Your Files**
   ```bash
   scp -r /path/to/bugfixer-bot user@server:/home/user/
   ```

3. **Create .env File**
   ```bash
   cd bugfixer-bot
   nano .env
   # Add your tokens
   ```

4. **Build and Run**
   ```bash
   # Build the image
   docker build -t bugfixer-bot .
   
   # Run the container
   docker run -d \
     --name bugfixer-bot \
     --restart unless-stopped \
     --env-file .env \
     bugfixer-bot
   ```

   Or use docker-compose:
   ```bash
   docker-compose up -d
   ```

5. **Manage the Bot**
   ```bash
   # View logs
   docker logs -f bugfixer-bot
   
   # Stop
   docker stop bugfixer-bot
   
   # Start
   docker start bugfixer-bot
   
   # Restart
   docker restart bugfixer-bot
   
   # Remove
   docker rm -f bugfixer-bot
   ```

**Cost:** Same as VPS ($4-6/month)
**Difficulty:** ⭐⭐⭐⭐ (4/5)

---

## Option 6: Railway.app (Modern, Easy)

### ✅ Best For
- Modern deployment
- Easy GitHub integration
- Auto-deployments
- Free trial

### Setup

1. **Sign Up**
   - Go to https://railway.app
   - Sign up with GitHub

2. **Create New Project**
   - Click "New Project"
   - Choose "Deploy from GitHub repo"
   - Connect your repo (or create new one)

3. **Add Environment Variables**
   - Click on your service
   - Go to "Variables" tab
   - Add:
     ```
     TELEGRAM_BOT_TOKEN
     GITHUB_TOKEN
     ANTHROPIC_API_KEY
     ```

4. **Deploy**
   - Railway auto-deploys from your repo
   - Any push to GitHub = auto-deploy!

**Cost:** $5 free credit, then ~$5/month
**Difficulty:** ⭐⭐ (2/5)

---

## Comparison Table

| Option | Cost | Difficulty | Always On | Best For |
|--------|------|------------|-----------|----------|
| Your Computer | Free | ⭐ | ❌ | Testing |
| Replit | Free-$7 | ⭐⭐ | ⚠️ | Learning |
| PythonAnywhere | Free-$5 | ⭐⭐ | ⚠️ | Simple hosting |
| VPS (DigitalOcean) | $4-6 | ⭐⭐⭐ | ✅ | Production |
| Docker | $4-6 | ⭐⭐⭐⭐ | ✅ | DevOps |
| Railway | Free-$5 | ⭐⭐ | ✅ | Modern deploy |

---

## Recommended Path

### For Beginners
1. **Start:** Test on your computer
2. **Next:** Deploy to Replit (free)
3. **Production:** Upgrade to Railway or DigitalOcean

### For Experienced Developers
1. Go straight to DigitalOcean/AWS with systemd service
2. Or use Docker for easier management

### For Teams
1. VPS with proper monitoring
2. Set up CI/CD pipeline
3. Use Docker for consistency

---

## Quick Start Recommendation: Replit

**I recommend starting with Replit because:**
- ✅ Completely free to start
- ✅ No credit card needed
- ✅ Web-based (no server management)
- ✅ Works in minutes
- ✅ Can upgrade later if needed

### Replit Setup in 5 Minutes

```bash
1. Go to replit.com → Sign up
2. Create new Python Repl
3. Upload bugfixer_bot.py and requirements.txt
4. Click "Secrets" → Add your 3 tokens
5. Click "Run"
6. Done! Bot is live!
```

---

## Testing Before Full Deployment

Before deploying permanently, test locally:

```bash
# Terminal 1: Run the bot
python bugfixer_bot.py

# Terminal 2: Test it
# Open Telegram and message your bot
# Try: /start
# Try: /setrepo username/repo
# Try: "Fix the bug in file.py"

# If it works locally, it will work on any server!
```

---

## Monitoring Your Bot

Once hosted, monitor it:

### Check if Running
```bash
# On VPS
systemctl status bugfixer-bot

# On Replit
# Just check the web interface

# With Docker
docker ps | grep bugfixer
```

### View Logs
```bash
# On VPS
journalctl -u bugfixer-bot -f

# On Replit
# Check the console output

# With Docker
docker logs -f bugfixer-bot
```

### Restart if Needed
```bash
# On VPS
systemctl restart bugfixer-bot

# On Replit
# Click "Stop" then "Run"

# With Docker
docker restart bugfixer-bot
```

---

## Troubleshooting Hosting Issues

### Bot Keeps Stopping
- **On your computer:** Normal - it stops when you turn off PC
- **On Replit free:** Sleeps after inactivity - upgrade or use keep-alive
- **On VPS:** Check systemd service - `systemctl status bugfixer-bot`

### Can't Connect to Telegram
- Check internet connection
- Verify bot token is correct
- Check firewall isn't blocking port 443
- Try: `curl https://api.telegram.org`

### High CPU/Memory Usage
- Claude API calls are intensive
- Consider rate limiting
- Use a VPS with more RAM
- Monitor with: `htop` or `docker stats`

---

## Security Best Practices

1. **Never commit .env to GitHub**
   ```bash
   # .gitignore should include:
   .env
   ```

2. **Use SSH keys for VPS**
   ```bash
   ssh-keygen -t rsa -b 4096
   # Add to DigitalOcean/AWS during setup
   ```

3. **Keep tokens secure**
   - Use environment variables
   - Rotate tokens every 90 days
   - Don't share in chat/email

4. **Update regularly**
   ```bash
   pip install --upgrade -r requirements.txt
   ```

---

## Cost Breakdown

### Free Options
- ✅ Your computer - $0
- ✅ Replit (with sleep) - $0
- ✅ PythonAnywhere (limited) - $0

### Paid Options (Monthly)
- $5 - PythonAnywhere Hacker plan
- $5 - Railway.app
- $6 - DigitalOcean Basic Droplet
- $7 - Replit Always-On
- $0.01-0.05 per fix - Claude API usage

**Total:** $5-7/month for reliable hosting + API costs

---

## My Recommendation

**Start here:**
1. Test locally first (your computer)
2. Deploy to **Replit** for free 24/7 access
3. If you need true production reliability, upgrade to **DigitalOcean** ($6/month)

**This gives you:**
- Free testing period
- Learn how it works
- Easy upgrade path
- Low cost for production

---

## Next Steps

1. **Choose your hosting option** (I recommend Replit to start)
2. **Follow the setup guide** for that option above
3. **Test it thoroughly** before relying on it
4. **Monitor it** to ensure it stays running
5. **Upgrade when needed** as your usage grows

---

## Need Help?

- **Can't decide which option?** → Start with Replit
- **Setup issues?** → Check TROUBLESHOOTING.md
- **Server problems?** → Check your host's documentation
- **Bot not working?** → Test locally first

---

**You're ready to host! Pick an option above and let's get your bot online! 🚀**
