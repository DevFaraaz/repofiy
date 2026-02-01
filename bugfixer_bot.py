"""
Reopfiy - Autonomous AI-Powered GitHub Assistant for Telegram
Fix bugs, create features, make code changes, refactor code, and manage your entire repository
"""

import os
import logging
import asyncio
from typing import Optional, Dict, List
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)
import requests
from github import Github, GithubException
import json
import subprocess
import tempfile
import shutil
import time

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


class BugFixerBot:
    """Reopfiy Bot - handles bug fixes, feature development, code changes, and repository management"""
    
    # Loader animations
    LOADERS = {
        "dots": ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"],
        "line": ["⠂", "-", "–", "—", "–", "-"],
        "circle": ["◡", "⊙", "◠"],
        "arrow": ["→", "↘", "↓", "↙", "←", "↖", "↑", "↗"]
    }
    
    def __init__(self, telegram_token: str, github_token: str = "", groq_key: str = ""):
        self.telegram_token = telegram_token
        self.github_token = github_token
        self.groq_key = groq_key
        
        # Only initialize GitHub client if token is provided
        self.github_client = Github(github_token) if github_token else None
        
        self.groq_url = "https://api.groq.com/openai/v1/chat/completions"
        self.groq_headers = {
            "Authorization": f"Bearer {groq_key}",
            "Content-Type": "application/json"
        }
        
        # Store active sessions
        self.active_fixes: Dict[int, dict] = {}
        
    def get_loader_text(self, stage: int, base_text: str, loader_type: str = "dots") -> str:
        """Get animated loader text"""
        frames = self.LOADERS.get(loader_type, self.LOADERS["dots"])
        frame = frames[stage % len(frames)]
        return f"{frame} {base_text}"
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        welcome_message = """
🚀 **Reopfiy** - Your AI Code Assistant on Telegram

I manage your GitHub repositories directly from Telegram!
Fix bugs, create features, refactor code, and more.

**Setup:**
/setai - Choose AI provider (Anthropic, OpenRouter, Groq)
/settoken <token> - Add GitHub token
/setrepo <owner/repo> - Set repository

**Main Commands:**
/fix <description> - Fix a bug
/feature <description> - Create new feature
/change <description> - Make code changes
/create <description> - Create new file/component
/view - Browse repository files
/analyze - Show repository structure

**Utility:**
/status - Check current operation status
/cancel - Cancel current operation

**Quick Examples:**
• /analyze - See what's in your repo
• /fix User login returns 401 error
• /feature Add dark mode toggle
• /change Refactor auth service
• /create New API endpoint for users

**Supported AI Providers:**
🌐 OpenRouter - 400+ models (Claude, Llama, etc.)
🧠 Anthropic - Claude 3.5 Sonnet
⚡ Groq - Mixtral 8x7b (fast & free)

Ready to manage code from your phone? Let's go!
        """
        await update.message.reply_text(welcome_message, parse_mode='Markdown')
    
    async def set_ai_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Set AI provider and API key"""
        keyboard = [
            [InlineKeyboardButton("🌐 OpenRouter", callback_data="ai_openrouter")],
            [InlineKeyboardButton("🧠 Anthropic", callback_data="ai_anthropic")],
            [InlineKeyboardButton("⚡ Groq", callback_data="ai_groq")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            "Choose your AI provider:\n\n"
            "**OpenRouter** - Access to 400+ models (Claude, Llama, etc.)\n"
            "**Anthropic** - Claude API directly\n"
            "**Groq** - Fast inference (llama, mixtral)\n\n"
            "Get free API keys:\n"
            "• OpenRouter: https://openrouter.ai/keys\n"
            "• Anthropic: https://console.anthropic.com/keys\n"
            "• Groq: https://console.groq.com/keys",
            parse_mode='Markdown',
            reply_markup=reply_markup
        )
    
    async def set_token_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Update GitHub token"""
        # Check if token provided directly
        if context.args:
            token = context.args[0].strip()
            
            if len(token) > 20:
                try:
                    # Verify token works
                    test_client = Github(token)
                    test_client.get_user().login
                    
                    context.user_data['github_token'] = token
                    await update.message.reply_text(
                        "✅ GitHub token saved!\n\n"
                        "Now set your repository:\n"
                        "/setrepo owner/repo\n\n"
                        "Example: /setrepo username/my-project"
                    )
                    return
                except Exception as e:
                    await update.message.reply_text(
                        f"❌ Invalid token: {str(e)}\n\n"
                        "Please check your token and try again."
                    )
                    return
            else:
                await update.message.reply_text(
                    "❌ Token too short.\n"
                    "Use: /settoken <your_token>"
                )
                return
        
        # No token provided, ask for it
        await update.message.reply_text(
            "Please send your GitHub personal access token:\n\n"
            "**Option 1 (Direct):**\n"
            "/settoken ghp_xxxxxxxxxxxxx\n\n"
            "**Option 2 (Interactive):**\n"
            "1. Go to https://github.com/settings/tokens\n"
            "2. Click 'Generate new token (classic)'\n"
            "3. Check the 'repo' scope\n"
            "4. Generate and copy the token\n"
            "5. Send it as a plain message (not a command)\n\n"
            "⚠️ Your token will be saved for this session.",
            parse_mode='Markdown'
        )
        context.user_data['waiting_for_github_token'] = True
    
    async def set_repo_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Set the GitHub repository to work with"""
        user_id = update.effective_user.id
        
        # Check if user has provided GitHub token
        if 'github_token' not in context.user_data:
            await update.message.reply_text(
                "Please set your GitHub token first:\n"
                "/settoken <your_token>"
            )
            return
        
        if not context.args:
            await update.message.reply_text(
                "Please provide a repository:\n\n"
                "/setrepo owner/repo\n\n"
                "Example: /setrepo username/my-project"
            )
            return
        
        repo_name = context.args[0]
        
        try:
            # Get user's GitHub client
            github_client = Github(context.user_data['github_token'])
            # Verify repository exists and user has access
            repo = github_client.get_repo(repo_name)
            
            # Store in user context
            context.user_data['repo'] = repo_name
            
            await update.message.reply_text(
                f"✅ Repository set to: **{repo_name}**\n"
                f"I can now help fix bugs, create features, make code changes, and manage your code in this repository!",
                parse_mode='Markdown'
            )
        except GithubException as e:
            await update.message.reply_text(
                f"❌ Error accessing repository: {str(e)}\n"
                "Make sure the repository exists and your GitHub token has access."
            )
    
    async def fix_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Start the bug fix process"""
        if not context.args:
            await update.message.reply_text(
                "Please describe the bug you want to fix:\n"
                "/fix <bug description>\n\n"
                "Example: /fix auth service returns 401 for valid tokens"
            )
            return
        
        bug_description = ' '.join(context.args)
        await self.process_code_task(update, context, bug_description, task_type="fix")
    
    async def feature_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Start feature development"""
        if not context.args:
            await update.message.reply_text(
                "Please describe the feature:\n"
                "/feature <feature description>\n\n"
                "Example: /feature Add dark mode toggle to settings"
            )
            return
        
        description = ' '.join(context.args)
        await self.process_code_task(update, context, description, task_type="feature")
    
    async def change_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Make code changes"""
        if not context.args:
            await update.message.reply_text(
                "Please describe the changes:\n"
                "/change <description>\n\n"
                "Example: /change Refactor auth service to use async/await"
            )
            return
        
        description = ' '.join(context.args)
        await self.process_code_task(update, context, description, task_type="change")
    
    async def create_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Create new file or component"""
        if not context.args:
            await update.message.reply_text(
                "Please describe what to create:\n"
                "/create <description>\n\n"
                "Example: /create New API endpoint for user notifications"
            )
            return
        
        description = ' '.join(context.args)
        await self.process_code_task(update, context, description, task_type="create")
    
    async def view_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """View files from repository"""
        repo_name = context.user_data.get('repo')
        
        if not repo_name:
            await update.message.reply_text(
                "Please set a repository first using:\n"
                "/setrepo owner/repo"
            )
            return
        
        if 'github_token' not in context.user_data:
            await update.message.reply_text(
                "Please set your GitHub token first:\n"
                "/settoken"
            )
            return
        
        # Check if user provided filename
        if context.args:
            filename = ' '.join(context.args)
            await self.view_file(update, context, filename, repo_name)
        else:
            # Show file browser
            await self.show_file_browser(update, context, repo_name)
    
    async def show_file_browser(self, update: Update, context: ContextTypes.DEFAULT_TYPE, repo_name: str):
        """Show interactive file browser"""
        status_message = await update.message.reply_text(
            "📂 **Loading files...**",
            parse_mode='Markdown'
        )
        
        try:
            github_client = Github(context.user_data['github_token'])
            repo = github_client.get_repo(repo_name)
            
            # Get important files
            important_files = await self.get_important_files(repo)
            
            if not important_files:
                await status_message.edit_text(
                    "❌ No files found in repository"
                )
                return
            
            # Build keyboard with file buttons
            keyboard = []
            for i, filename in enumerate(important_files[:10]):
                # Limit button text to 30 chars
                display_name = filename if len(filename) <= 30 else filename[-27:] + "..."
                keyboard.append([
                    InlineKeyboardButton(f"📄 {display_name}", callback_data=f"view_{i}_{repo_name}")
                ])
            
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            # Store file list in context
            context.user_data['file_list'] = important_files
            context.user_data['current_repo'] = repo_name
            
            await status_message.edit_text(
                f"📂 **Repository Files**\n\n"
                f"Showing {len(important_files[:10])} important files.\n"
                f"Click to view:\n",
                reply_markup=reply_markup
            )
            
        except Exception as e:
            logger.error(f"Error showing file browser: {str(e)}")
            await status_message.edit_text(
                f"❌ Error loading files: {str(e)}"
            )
    
    async def get_important_files(self, repo, path: str = "", max_files: int = 20) -> list:
        """Get list of important files from repo"""
        important_files = []
        priority_extensions = ['.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.go', '.rb', '.md', 'README', '.json', '.yml', '.yaml']
        
        try:
            contents = repo.get_contents(path) if path else repo.get_contents("")
            
            for item in contents:
                # Skip hidden and unimportant dirs
                if item.name.startswith('.') or item.name in ['node_modules', '__pycache__', '.git', 'venv', 'env', 'dist', 'build']:
                    continue
                
                if item.type == "file":
                    # Prioritize certain extensions
                    if any(item.name.endswith(ext) for ext in priority_extensions) or item.name in ['README', 'Dockerfile']:
                        important_files.append(item.path)
                
                elif item.type == "dir" and len(important_files) < max_files:
                    # Recursively check subdirectories
                    try:
                        sub_files = await self.get_important_files(repo, item.path, max_files - len(important_files))
                        important_files.extend(sub_files)
                    except:
                        pass
                
                if len(important_files) >= max_files:
                    break
            
            return important_files[:max_files]
            
        except Exception as e:
            logger.warning(f"Error getting important files: {str(e)}")
            return important_files
    
    async def view_file(self, update: Update, context: ContextTypes.DEFAULT_TYPE, filename: str, repo_name: str):
        """View specific file content"""
        # Determine if this is from a callback or regular message
        is_callback = update.callback_query is not None
        
        try:
            github_client = Github(context.user_data['github_token'])
            repo = github_client.get_repo(repo_name)
            file_obj = repo.get_contents(filename)
            
            # Check if it's a binary file
            if not isinstance(file_obj.content, str):
                msg = f"❌ Cannot display binary file: {filename}"
                if is_callback:
                    await update.callback_query.answer()
                    await update.callback_query.message.reply_text(msg)
                else:
                    await update.message.reply_text(msg)
                return
            
            content = file_obj.decoded_content.decode('utf-8')
            
            # Detect language for syntax highlighting
            ext = filename.split('.')[-1] if '.' in filename else ''
            lang_map = {
                'py': 'python',
                'js': 'javascript',
                'ts': 'typescript',
                'jsx': 'javascript',
                'tsx': 'typescript',
                'java': 'java',
                'go': 'go',
                'rb': 'ruby',
                'sh': 'bash',
                'json': 'json',
                'yaml': 'yaml',
                'yml': 'yaml',
                'html': 'html',
                'css': 'css',
                'md': 'markdown'
            }
            lang = lang_map.get(ext, '')
            
            # Get file size
            file_size = len(content)
            
            # Truncate if too large
            max_chars = 3000
            truncated = False
            if file_size > max_chars:
                content = content[:max_chars]
                truncated = True
            
            # Build message
            message = f"📄 **{filename}** ({file_size} bytes)\n\n"
            message += f"```{lang}\n{content}\n```\n"
            
            if truncated:
                message += "\n⚠️ **File truncated** (showing first 3000 chars)"
            
            if is_callback:
                await update.callback_query.answer()
                await update.callback_query.message.reply_text(message, parse_mode='Markdown')
            else:
                await update.message.reply_text(message, parse_mode='Markdown')
            
        except Exception as e:
            logger.error(f"Error viewing file: {str(e)}")
            error_msg = str(e).replace("_", "\\_").replace("*", "\\*")
            msg = f"❌ Error viewing file: `{error_msg}`"
            
            if is_callback:
                await update.callback_query.answer()
                await update.callback_query.message.reply_text(msg, parse_mode='Markdown')
            else:
                await update.message.reply_text(msg, parse_mode='Markdown')
    
    async def analyze_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Analyze and show repository structure"""
        repo_name = context.user_data.get('repo')
        
        if not repo_name:
            await update.message.reply_text(
                "Please set a repository first using:\n"
                "/setrepo owner/repo"
            )
            return
        
        if 'github_token' not in context.user_data:
            await update.message.reply_text(
                "Please set your GitHub token first:\n"
                "/settoken"
            )
            return
        
        status_message = await update.message.reply_text(
            f"📊 **Analyzing repository...**\n"
            f"Repository: {repo_name}\n\n"
            "Scanning directory structure...",
            parse_mode='Markdown'
        )
        
        try:
            # Get repository
            github_client = Github(context.user_data['github_token'])
            repo = github_client.get_repo(repo_name)
            
            # Get repository structure
            structure = await self.get_repo_structure(repo)
            
            # Build file tree message
            message = f"📁 **Repository: {repo_name}**\n\n"
            message += f"🔗 URL: {repo.html_url}\n"
            message += f"📝 Description: {repo.description or 'No description'}\n"
            message += f"⭐ Stars: {repo.stargazers_count}\n"
            message += f"🌿 Default Branch: {repo.default_branch}\n\n"
            message += "**📂 Structure:**\n```\n"
            message += structure[:3000]  # Limit message size
            message += "\n```"
            
            await status_message.edit_text(message, parse_mode='Markdown')
            
        except Exception as e:
            logger.error(f"Error analyzing repository: {str(e)}")
            error_msg = str(e).replace("_", "\\_").replace("*", "\\*")
            await status_message.edit_text(
                f"❌ **Error analyzing repository:**\n`{error_msg}`",
                parse_mode='Markdown'
            )
    
    async def get_repo_structure(self, repo, path: str = "", level: int = 0, max_level: int = 3) -> str:
        """Recursively get repository structure"""
        if level > max_level:
            return ""
        
        try:
            contents = repo.get_contents(path) if path else repo.get_contents("")
            
            structure = ""
            
            # Separate directories and files
            items = sorted(contents, key=lambda x: (x.type != "dir", x.name))
            
            for item in items:
                indent = "  " * level
                
                # Skip hidden files and common unimportant dirs
                if item.name.startswith('.') or item.name in ['node_modules', '__pycache__', '.git', 'venv', 'env']:
                    continue
                
                if item.type == "dir":
                    structure += f"{indent}📁 {item.name}/\n"
                    # Recursively get subdirectory contents
                    try:
                        sub_structure = await self.get_repo_structure(repo, item.path, level + 1, max_level)
                        structure += sub_structure
                    except:
                        pass
                else:
                    # Show file with extension icon
                    icon = "📄"
                    if item.name.endswith('.py'):
                        icon = "🐍"
                    elif item.name.endswith(('.js', '.ts', '.jsx', '.tsx')):
                        icon = "⚡"
                    elif item.name.endswith(('.html', '.css')):
                        icon = "🎨"
                    elif item.name.endswith(('.md', '.txt')):
                        icon = "📝"
                    elif item.name.endswith(('.json', '.yaml', '.yml')):
                        icon = "⚙️"
                    
                    structure += f"{indent}{icon} {item.name}\n"
            
            return structure
            
        except Exception as e:
            logger.warning(f"Error getting structure for {path}: {str(e)}")
            return ""
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle regular text messages as bug descriptions or API keys"""
        user_id = update.effective_user.id
        
        # If user is setting AI API key
        if context.user_data.get('waiting_for_ai_key'):
            api_key = update.message.text.strip()
            provider = context.user_data.get('ai_provider')
            
            if len(api_key) > 10:
                # Validate key format
                if provider == "openrouter" and not api_key.startswith("sk-or"):
                    await update.message.reply_text(
                        "❌ Invalid OpenRouter key (should start with sk-or-v1-)\n"
                        "Get one at https://openrouter.ai/keys"
                    )
                    return
                elif provider == "anthropic" and not api_key.startswith("sk-ant"):
                    await update.message.reply_text(
                        "❌ Invalid Anthropic key (should start with sk-ant-)\n"
                        "Get one at https://console.anthropic.com/keys"
                    )
                    return
                
                context.user_data['ai_key'] = api_key
                context.user_data['waiting_for_ai_key'] = False
                await update.message.reply_text(
                    f"✅ {provider.upper()} API key saved!\n\n"
                    "Now you need a GitHub personal access token.\n"
                    "Use: /settoken"
                )
                return
            else:
                await update.message.reply_text("❌ Key too short. Please provide valid API key.")
                return
        
        # If user is setting GitHub token
        if context.user_data.get('waiting_for_github_token'):
            token = update.message.text.strip()
            
            if len(token) > 20:
                try:
                    # Verify token works
                    test_client = Github(token)
                    test_client.get_user().login
                    
                    context.user_data['github_token'] = token
                    context.user_data['waiting_for_github_token'] = False
                    await update.message.reply_text(
                        "✅ GitHub token saved!\n\n"
                        "Now set your repository:\n"
                        "/setrepo owner/repo\n\n"
                        "Example: /setrepo username/my-project"
                    )
                    return
                except Exception as e:
                    await update.message.reply_text(
                        f"❌ Invalid token: {str(e)}\n\n"
                        "Please provide a valid GitHub token or type /settoken again"
                    )
                    return
            else:
                await update.message.reply_text(
                    "❌ Token too short.\n"
                    "Please provide a valid GitHub token or use /settoken again."
                )
                return
        
        # If user hasn't provided GitHub token, check if this is it
        if 'github_token' not in context.user_data:
            token = update.message.text.strip()
            
            # Basic validation (GitHub tokens usually start with ghp_ or similar)
            if len(token) > 20:
                try:
                    # Verify token works
                    test_client = Github(token)
                    test_client.get_user().login
                    
                    context.user_data['github_token'] = token
                    await update.message.reply_text(
                        "✅ GitHub token saved!\n\n"
                        "Now set your repository using:\n"
                        "/setrepo owner/repo\n\n"
                        "Example: /setrepo username/my-project"
                    )
                    return
                except Exception as e:
                    await update.message.reply_text(
                        f"❌ Invalid GitHub token: {str(e)}\n"
                        "Please provide a valid personal access token from:\n"
                        "https://github.com/settings/tokens"
                    )
                    return
            else:
                await update.message.reply_text(
                    "Please provide your GitHub personal access token:\n"
                    "1. Go to https://github.com/settings/tokens\n"
                    "2. Create a new token with 'repo' scope\n"
                    "3. Send the token here"
                )
                return
        
        repo = context.user_data.get('repo')
        
        if not repo:
            await update.message.reply_text(
                "Please set a repository first using:\n"
                "/setrepo owner/repo"
            )
            return
        
        description = update.message.text
        # Treat regular messages as feature/change requests by default
        await self.process_code_task(update, context, description, task_type="change")
    
    async def process_code_task(self, update: Update, context: ContextTypes.DEFAULT_TYPE, description: str, task_type: str = "fix"):
        """Main code processing workflow for all task types"""
        user_id = update.effective_user.id
        repo_name = context.user_data.get('repo')
        
        if not repo_name:
            await update.message.reply_text("Please set a repository first with /setrepo")
            return
        
        # Task type emojis and messages
        task_config = {
            "fix": {"emoji": "🔧", "action": "Fixing"},
            "feature": {"emoji": "✨", "action": "Implementing"},
            "change": {"emoji": "♻️", "action": "Making changes"},
            "create": {"emoji": "📝", "action": "Creating"}
        }
        config = task_config.get(task_type, task_config["fix"])
        
        # Send initial message
        status_message = await update.message.reply_text(
            f"{config['emoji']} **{config['action']}...**\n"
            f"Repository: {repo_name}\n"
            f"Request: {description}",
            parse_mode='Markdown'
        )
        
        try:
            # Step 1: Analyze the request with animated loader
            github_client = Github(context.user_data['github_token'])
            repo = github_client.get_repo(repo_name)
            
            # Animated fetching
            for i in range(5):
                await status_message.edit_text(
                    f"{config['emoji']} **{config['action']}...**\n"
                    f"Repository: {repo_name}\n"
                    f"Request: {description}\n\n"
                    f"{self.get_loader_text(i, 'Fetching repository code...')}",
                    parse_mode='Markdown'
                )
                await asyncio.sleep(0.3)
            
            # Get recent files and code context
            code_context = await self.get_code_context(repo, description)
            
            # Step 2: Ask AI to analyze and propose solution with animated loader
            for i in range(8):
                await status_message.edit_text(
                    f"{config['emoji']} **{config['action']}...**\n"
                    f"Repository: {repo_name}\n"
                    f"Request: {description}\n\n"
                    f"{self.get_loader_text(i, 'AI is analyzing your request...')}",
                    parse_mode='Markdown'
                )
                await asyncio.sleep(0.2)
            
            solution = await self.analyze_code_task(
                description, 
                code_context,
                repo_name,
                task_type,
                context.user_data
            )
            
            # Step 3: Present the fix to the user
            keyboard = [
                [
                    InlineKeyboardButton("✅ Apply Fix", callback_data=f"apply_{user_id}"),
                    InlineKeyboardButton("🔄 Revise", callback_data=f"revise_{user_id}")
                ],
                [
                    InlineKeyboardButton("❌ Cancel", callback_data=f"cancel_{user_id}")
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            # Store the solution
            self.active_fixes[user_id] = {
                'repo_name': repo_name,
                'description': description,
                'task_type': task_type,
                'solution': solution,
                'status_message_id': status_message.message_id
            }
            
            task_labels = {
                "fix": "Bug Fix",
                "feature": "New Feature",
                "change": "Code Modification",
                "create": "New Component"
            }
            label = task_labels.get(task_type, "Task")
            
            await status_message.edit_text(
                f"{config['emoji']} **{label} Complete**\n\n"
                f"**Request:** {description}\n\n"
                f"**Proposed Solution:**\n{solution['summary']}\n\n"
                f"**Files to modify:**\n{', '.join(solution['files'])}\n\n"
                f"**Changes:**\n```\n{solution['diff_preview'][:500]}...\n```\n\n"
                "What would you like to do?",
                parse_mode='Markdown',
                reply_markup=reply_markup
            )
            
        except Exception as e:
            logger.error(f"Error processing code task: {str(e)}")
            await status_message.edit_text(
                f"❌ **Error occurred:**\n{str(e)}\n\n"
                "Please try again or contact support.",
                parse_mode='Markdown'
            )
    
    async def get_code_context(self, repo, bug_description: str) -> str:
        """Fetch relevant code context from repository"""
        try:
            # Get repository structure
            contents = repo.get_contents("")
            
            # Build a context of relevant files
            code_files = []
            relevant_files = []
            
            def scan_directory(contents):
                for content in contents:
                    if content.type == "dir":
                        scan_directory(repo.get_contents(content.path))
                    elif content.name.endswith(('.py', '.js', '.ts', '.java', '.go', '.rb')):
                        code_files.append(content)
            
            scan_directory(contents)
            
            # Use simple heuristics to find relevant files
            # In production, you'd use more sophisticated methods
            keywords = bug_description.lower().split()
            
            for file in code_files[:20]:  # Limit to first 20 files
                file_path_lower = file.path.lower()
                if any(keyword in file_path_lower for keyword in keywords):
                    relevant_files.append(file)
            
            # If no matches, just take the first few files
            if not relevant_files:
                relevant_files = code_files[:5]
            
            # Build context
            context = f"Repository: {repo.full_name}\n"
            context += f"Default Branch: {repo.default_branch}\n\n"
            context += "Relevant Files:\n"
            
            for file in relevant_files[:5]:  # Limit context size
                try:
                    content = file.decoded_content.decode('utf-8')
                    context += f"\n--- {file.path} ---\n"
                    context += content[:2000]  # Limit file size
                    context += "\n...\n"
                except:
                    continue
            
            return context
            
        except Exception as e:
            logger.error(f"Error getting code context: {str(e)}")
            return f"Repository: {repo.full_name}\nError fetching code context: {str(e)}"
    
    async def call_ai(self, prompt: str, user_context: Dict) -> str:
        """Call the appropriate AI provider"""
        provider = user_context.get('ai_provider', 'groq')
        api_key = user_context.get('ai_key')
        
        if provider == "openrouter":
            return await self.call_openrouter(prompt, api_key)
        elif provider == "anthropic":
            return await self.call_anthropic(prompt, api_key)
        else:  # default to groq
            return await self.call_groq(prompt, api_key)
    
    async def call_groq(self, prompt: str, api_key: str = None) -> str:
        """Call Groq API"""
        if api_key is None:
            api_key = self.groq_key
        
        payload = {
            "model": "llama-3.3-70b-versatile",
            "max_tokens": 4000,
            "messages": [{"role": "user", "content": prompt}]
        }
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            json=payload,
            headers=headers,
            timeout=30
        )
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    
    async def call_anthropic(self, prompt: str, api_key: str) -> str:
        """Call Anthropic Claude API"""
        from anthropic import Anthropic
        
        client = Anthropic(api_key=api_key)
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=4000,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text
    
    async def call_openrouter(self, prompt: str, api_key: str) -> str:
        """Call OpenRouter API"""
        payload = {
            "model": "meta-llama/llama-3.1-70b-instruct",  # Default model
            "max_tokens": 4000,
            "messages": [{"role": "user", "content": prompt}]
        }
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "HTTP-Referer": "https://aicodassistant.local",
            "Content-Type": "application/json"
        }
        
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            json=payload,
            headers=headers,
            timeout=30
        )
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    
    async def analyze_code_task(self, description: str, code_context: str, repo_name: str, task_type: str, user_context: Dict = None) -> dict:
        """Use AI to analyze code task and propose solution"""
        
        task_prompts = {
            "fix": f"You are analyzing a BUG REPORT and need to propose a FIX.",
            "feature": f"You are analyzing a FEATURE REQUEST and need to implement it.",
            "change": f"You are analyzing a CODE CHANGE REQUEST and need to implement the changes.",
            "create": f"You are analyzing a REQUEST TO CREATE new code/file and need to implement it."
        }
        
        task_instruction = task_prompts.get(task_type, task_prompts["fix"])
        
        prompt = f"""You are an expert software engineer. {task_instruction}

Repository: {repo_name}
Request: {description}

Code Context:
{code_context}

Please analyze this request and provide:
1. A summary of what's likely causing the bug
2. The specific files that need to be modified
3. The exact code changes needed (in unified diff format)
4. Any tests that should be run

Respond in JSON format:
{{
    "summary": "Brief explanation of the fix",
    "cause": "Root cause analysis",
    "files": ["list", "of", "files"],
    "changes": {{
        "filename": "code changes for this file"
    }},
    "diff_preview": "Brief preview of the main changes",
    "tests_to_run": ["list of test commands"],
    "confidence": "high/medium/low"
}}
"""
        
        try:
            response_text = await self.call_ai(prompt, user_context or {})
            
            # Extract JSON from response (Claude might wrap it in markdown)
            if "```json" in response_text:
                json_start = response_text.find("```json") + 7
                json_end = response_text.find("```", json_start)
                response_text = response_text[json_start:json_end].strip()
            elif "```" in response_text:
                json_start = response_text.find("```") + 3
                json_end = response_text.find("```", json_start)
                response_text = response_text[json_start:json_end].strip()
            
            fix_data = json.loads(response_text)
            return fix_data
            
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing Groq response: {str(e)}")
            # Return a fallback response
            return {
                "summary": response_text[:200],
                "cause": "Unable to parse detailed analysis",
                "files": [],
                "changes": {},
                "diff_preview": response_text[:500],
                "tests_to_run": [],
                "confidence": "low"
            }
        except requests.exceptions.HTTPError as e:
            logger.error(f"Groq API error: {e.response.text}")
            raise
        except Exception as e:
            logger.error(f"Error calling Groq API: {str(e)}")
            raise
    
    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle button callbacks"""
        query = update.callback_query
        await query.answer()
        
        callback_data = query.data
        
        # Handle file view button
        if callback_data.startswith("view_"):
            parts = callback_data.split("_", 2)
            if len(parts) >= 3:
                file_idx = int(parts[1])
                repo_name = parts[2]
                
                file_list = context.user_data.get('file_list', [])
                if file_idx < len(file_list):
                    filename = file_list[file_idx]
                    await self.view_file(update, context, filename, repo_name)
            return
        
        # Handle AI provider selection
        if callback_data.startswith("ai_"):
            provider = callback_data.replace("ai_", "")
            context.user_data['ai_provider'] = provider
            
            await query.edit_message_text(
                f"AI provider set to **{provider.upper()}**\n\n"
                f"Now send your {provider.upper()} API key:",
                parse_mode='Markdown'
            )
            context.user_data['waiting_for_ai_key'] = True
            return
        
        # Handle fix/feature/change/create actions
        if "_" not in callback_data:
            return
            
        action, user_id = callback_data.split('_')
        user_id = int(user_id)
        
        if user_id not in self.active_fixes:
            await query.edit_message_text("This task session has expired. Please start a new one.")
            return
        
        if action == "apply":
            await self.apply_fix(query, context, user_id)
        elif action == "revise":
            await query.edit_message_text(
                "Please describe what you'd like to change about the fix:",
                parse_mode='Markdown'
            )
        elif action == "cancel":
            del self.active_fixes[user_id]
            await query.edit_message_text("❌ Fix cancelled.")
    
    async def apply_fix(self, query, context, user_id: int):
        """Apply the proposed solution to the repository"""
        fix_data = self.active_fixes[user_id]
        repo_name = fix_data['repo_name']
        solution = fix_data['solution']
        task_type = fix_data.get('task_type', 'fix')
        
        # Animated applying status
        for i in range(3):
            await query.edit_message_text(
                f"{self.get_loader_text(i, '🔧 Applying fix...')}\n"
                "Creating branch and committing changes...",
                parse_mode='Markdown'
            )
            await asyncio.sleep(0.3)
        
        try:
            # Get user's GitHub client
            github_client = Github(context.user_data['github_token'])
            repo = github_client.get_repo(repo_name)
            
            # Create a new branch
            base_branch = repo.get_branch(repo.default_branch)
            task_prefix = {"fix": "bugfix", "feature": "feature", "change": "refactor", "create": "feat"}
            prefix = task_prefix.get(task_type, "update")
            branch_name = f"{prefix}/ai-{user_id}-{int(asyncio.get_event_loop().time())}"
            
            repo.create_git_ref(
                ref=f"refs/heads/{branch_name}",
                sha=base_branch.commit.sha
            )
            
            # Apply changes to files
            files_updated = 0
            total_files = len(solution.get('changes', {}))
            
            for idx, (filename, changes) in enumerate(solution.get('changes', {}).items()):
                # Show progress with loader
                for i in range(2):
                    await query.edit_message_text(
                        f"{self.get_loader_text(i, '🔧 Applying fix...')}\n"
                        f"Writing files: {idx + 1}/{total_files} - {filename}",
                        parse_mode='Markdown'
                    )
                    await asyncio.sleep(0.2)
                
                try:
                    try:
                        # Try to get existing file
                        file = repo.get_contents(filename, ref=branch_name)
                        # Update existing file
                        repo.update_file(
                            path=filename,
                            message=f"chore: {fix_data['description'][:50]}",
                            content=changes,
                            sha=file.sha,
                            branch=branch_name
                        )
                    except Exception:
                        # File doesn't exist, create it
                        repo.create_file(
                            path=filename,
                            message=f"feat: {fix_data['description'][:50]}",
                            content=changes,
                            branch=branch_name
                        )
                    files_updated += 1
                    logger.info(f"Successfully processed {filename}")
                except Exception as e:
                    logger.warning(f"Could not process {filename}: {str(e)}")
            
            # Show PR creation loader
            for i in range(3):
                await query.edit_message_text(
                    f"{self.get_loader_text(i, '🔧 Applying fix...')}\n"
                    "Creating pull request...",
                    parse_mode='Markdown'
                )
                await asyncio.sleep(0.3)
            
            # Create pull request
            task_labels = {
                "fix": "🤖 Auto-fix",
                "feature": "✨ Feature",
                "change": "♻️ Code Change",
                "create": "📝 New Addition"
            }
            pr_title = f"{task_labels.get(task_type, '🤖 Auto-fix')}: {fix_data['description'][:50]}"
            
            pr = repo.create_pull(
                title=pr_title,
                body=f"""## Automated {task_labels.get(task_type, 'Fix')}

**Description:** {fix_data['description']}

**Analysis:** {solution['summary']}

**Root Cause:** {solution.get('cause', 'See changes')}

**Confidence Level:** {solution.get('confidence', 'medium')}

---
*This PR was automatically generated by AI Code Assistant*
""",
                head=branch_name,
                base=repo.default_branch
            )
            
            # Success message
            keyboard = [[InlineKeyboardButton("🔗 View PR", url=pr.html_url)]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            task_success = {
                "fix": "✅ Fix Applied",
                "feature": "✨ Feature Created",
                "change": "♻️ Changes Applied",
                "create": "📝 Component Created"
            }
            success_msg = task_success.get(task_type, "✅ Applied")
            
            await query.edit_message_text(
                f"{success_msg} Successfully!\n\n"
                f"**Branch:** {branch_name}\n"
                f"**Pull Request:** #{pr.number}\n"
                f"**Files Modified:** {len(solution.get('changes', {}))}\n\n"
                f"Review the changes and merge when ready!",
                parse_mode='Markdown',
                reply_markup=reply_markup
            )
            
            # Clean up
            del self.active_fixes[user_id]
            
        except Exception as e:
            logger.error(f"Error applying fix: {str(e)}")
            error_msg = str(e).replace("_", "\\_").replace("*", "\\*").replace("[", "\\[").replace("]", "\\]")
            await query.edit_message_text(
                f"❌ **Error applying fix:**\n`{error_msg}`\n\n"
                "Please check your repository permissions and try again.",
                parse_mode='Markdown'
            )
    
    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Check status of active tasks"""
        user_id = update.effective_user.id
        
        if user_id not in self.active_fixes:
            await update.message.reply_text("No active task sessions.")
            return
        
        fix_data = self.active_fixes[user_id]
        task_type = fix_data.get('task_type', 'fix')
        task_labels = {
            "fix": "Bug Fix",
            "feature": "New Feature",
            "change": "Code Modification",
            "create": "New Component"
        }
        await update.message.reply_text(
            f"**Active Task Session**\n"
            f"Type: {task_labels.get(task_type, 'Task')}\n"
            f"Repository: {fix_data['repo_name']}\n"
            f"Description: {fix_data['description']}",
            parse_mode='Markdown'
        )
    
    async def cancel_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Cancel current operation"""
        user_id = update.effective_user.id
        
        if user_id in self.active_fixes:
            del self.active_fixes[user_id]
            await update.message.reply_text("✅ Current operation cancelled.")
        else:
            await update.message.reply_text("No active operations to cancel.")
    
    def run(self):
        """Start the bot"""
        application = Application.builder().token(self.telegram_token).build()
        
        # Add handlers
        application.add_handler(CommandHandler("start", self.start_command))
        application.add_handler(CommandHandler("setai", self.set_ai_command))
        application.add_handler(CommandHandler("settoken", self.set_token_command))
        application.add_handler(CommandHandler("setrepo", self.set_repo_command))
        application.add_handler(CommandHandler("view", self.view_command))
        application.add_handler(CommandHandler("analyze", self.analyze_command))
        application.add_handler(CommandHandler("fix", self.fix_command))
        application.add_handler(CommandHandler("feature", self.feature_command))
        application.add_handler(CommandHandler("change", self.change_command))
        application.add_handler(CommandHandler("create", self.create_command))
        application.add_handler(CommandHandler("status", self.status_command))
        application.add_handler(CommandHandler("cancel", self.cancel_command))
        application.add_handler(CallbackQueryHandler(self.handle_callback))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        
        logger.info("🚀 Reopfiy Bot started!")
        application.run_polling()


def main():
    """Main entry point"""
    from dotenv import load_dotenv
    load_dotenv()
    
    # Load environment variables
    TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    
    # Optional: Load default AI provider key (users can set their own via /setai)
    GROQ_KEY = os.getenv('GROQ_API_KEY', '')
    GITHUB_TOKEN = os.getenv('GITHUB_TOKEN', '')
    
    if not TELEGRAM_TOKEN:
        print("❌ Error: Missing TELEGRAM_BOT_TOKEN!")
        print("Please set TELEGRAM_BOT_TOKEN in your .env file")
        return
    
    bot = BugFixerBot(TELEGRAM_TOKEN, GITHUB_TOKEN, GROQ_KEY)
    bot.run()


if __name__ == '__main__':
    main()
