# System Prompt Integration Guide

This guide shows how to integrate `SYSTEM_PROMPT.md` into the actual bot code.

## How It Works

The `SYSTEM_PROMPT.md` is used in **all AI provider requests** (Anthropic, OpenRouter, Groq). Here's the flow:

```
User Request
    ↓
Bot reads SYSTEM_PROMPT.md + Code Context
    ↓
Bot sends to AI Provider: System Prompt + User Request + Code
    ↓
AI Provider responds with structured fix
    (Works with: Anthropic Claude, OpenRouter any model, Groq)
    ↓
Bot applies fix to GitHub
```

**The system prompt is provider-agnostic** - it defines behavior for any AI model.

## User Configuration Flow

Instead of storing API keys in `.env`, they're managed in Telegram:

1. **Telegram Token** - Only thing in `.env`
   ```env
   TELEGRAM_BOT_TOKEN=...
   ```

2. **GitHub Token** - Added via `/settoken` command
   - Stored in: `context.user_data['github_token']`

3. **AI Provider** - Selected via `/setai` command
   - Stored in: `context.user_data['ai_provider']` (anthropic/openrouter/groq)
   - Stored in: `context.user_data['ai_key']` (the actual API key)

This approach:
- ✅ No sensitive keys in `.env` files
- ✅ Easy to change providers without restarting
- ✅ Users can have different providers per bot instance
- ✅ No risk of committing keys to git

## Integration Steps

### 1. Load System Prompt at Startup

Add to `bugfixer_bot.py` in the `__init__` method:

```python
def __init__(self, telegram_token: str, github_token: str = "", groq_key: str = ""):
    # ... existing code ...
    
    # Load system prompt
    self.system_prompt = self._load_system_prompt()
    
def _load_system_prompt(self) -> str:
    """Load system prompt from SYSTEM_PROMPT.md"""
    try:
        with open('SYSTEM_PROMPT.md', 'r') as f:
            return f.read()
    except FileNotFoundError:
        logger.warning("SYSTEM_PROMPT.md not found, using default")
        return "You are an AI code assistant that helps fix bugs and create features."
```

### 2. Use in AI Provider Requests

In the `analyze_code_with_ai()` method, build the prompt like this for **all providers**:

```python
async def analyze_code_with_ai(self, code_context: str, request: str, request_type: str, api_provider: str, api_key: str) -> dict:
    """Send code to AI for analysis using system prompt - works with all providers"""
    
    # Build the prompt using system prompt
    system_message = f"""{self.system_prompt}

---

## Current Task

**Request Type:** {request_type.upper()}
**User Request:** {request}

Please analyze the provided code and propose specific changes for this {request_type}.
"""
    
    user_message = f"""Repository Code Context:

{code_context}

{request_type.upper()} REQUEST: {request}

Respond with JSON:
{{
    "summary": "What you're doing and why",
    "files": ["list", "of", "files"],
    "changes": {{"filename.py": "new code here"}},
    "explanation": "Detailed explanation",
    "notes": "Edge cases, testing tips"
}}
"""
    
    # All providers use the same system prompt
    if api_provider == "anthropic":
        response = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json"
            },
            json={
                "model": "claude-3-5-sonnet-20241022",
                "max_tokens": 4096,
                "system": system_message,  # ← System prompt here
                "messages": [{"role": "user", "content": user_message}]
            }
        )
    
    elif api_provider == "openrouter":
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "auto",  # Auto-selects best available
                "max_tokens": 4096,
                "system": system_message,  # ← System prompt here
                "messages": [{"role": "user", "content": user_message}]
            }
        )
    
    elif api_provider == "groq":
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "mixtral-8x7b-32768",
                "max_tokens": 4096,
                "system": system_message,  # ← System prompt here
                "messages": [{"role": "user", "content": user_message}]
            }
        )
    
    return response.json()
```

**All providers support system prompts** - it's a standard feature in chat API requests.

### 3. Existing Code Pattern

The bot already uses prompts in `analyze_code_with_ai()`. You just need to prepend the system prompt:

**Before (current code):**
```python
prompt = f"Fix this bug: {bug_description}\n\nCode:\n{code_context}"
```

**After (with system prompt):**
```python
system = self.system_prompt  # Loaded from SYSTEM_PROMPT.md
prompt = f"Request: {bug_description}\n\nCode:\n{code_context}"
```

## What Gets Sent to Claude

### Example 1: Bug Fix Request

```
[SYSTEM PROMPT from SYSTEM_PROMPT.md]

---

## Current Task
Request Type: FIX
User Request: Users can't login - 401 error

[CODE CONTEXT]

Response format: JSON with summary, files, changes, explanation, notes
```

### Example 2: Feature Request

```
[SYSTEM PROMPT from SYSTEM_PROMPT.md]

---

## Current Task
Request Type: FEATURE
User Request: Add dark mode toggle

[CODE CONTEXT]

Response format: JSON with summary, files, changes, explanation, notes
```

## Key Integration Points in bugfixer_bot.py

### Location 1: Initialization (Line ~46)
```python
class BugFixerBot:
    def __init__(self, ...):
        # ADD THIS:
        self.system_prompt = self._load_system_prompt()
```

### Location 2: AI Analysis Method (Line ~400-600, find `analyze_code_with_ai`)
```python
async def analyze_code_with_ai(self, ...):
    # USE THIS:
    system_message = f"{self.system_prompt}\n\n--- Current Task ---\n..."
    
    # Then pass to Claude API:
    response = requests.post(
        url,
        json={
            "system": system_message,  # ← ADD THIS
            "messages": [{"role": "user", "content": user_prompt}]
        }
    )
```

### Location 3: Process Code Task (Line ~450-600)
```python
async def process_code_task(self, ...):
    # ... existing code ...
    
    # When calling Claude:
    solution = await self.analyze_code_with_ai(
        code_context=context,
        request=task_description,
        request_type=task_type,  # "fix", "feature", "change", "create"
        api_provider=provider,
        api_key=api_key
    )
```

## Benefits

### 1. **Consistent Behavior**
- Claude follows the same guidelines for all requests
- Ensures safety (never merges own PRs, always asks approval)
- Maintains the bot's personality and constraints

### 2. **Better Quality Fixes**
- Claude understands the different request types
- Provides better explanations
- Considers edge cases and security

### 3. **Easy Customization**
- Change behavior by editing `SYSTEM_PROMPT.md`
- No code changes needed
- Users can fork and modify for their needs

### 4. **Open Source Transparency**
- Anyone can see exactly how the bot behaves
- System prompt is documented and versioned
- Easy to extend with new request types

## Testing the Integration

Once integrated, test with:

```bash
# Test bug fix
/fix Login returns 401 error

# Test feature creation
/feature Add email verification

# Test refactoring
/change Optimize database queries

# Test new file creation
/create New API endpoint for user profile
```

Claude should now:
- Follow all guidelines in SYSTEM_PROMPT.md
- Provide proper explanations
- Consider edge cases
- Include testing suggestions
- Never assume auto-merge is acceptable

## Future Enhancements

### Dynamic System Prompt
Load different prompts based on context:
```python
def get_system_prompt(self, request_type: str, user_preferences: dict) -> str:
    base = self.system_prompt
    if request_type == "security_fix":
        return f"{base}\n\nEXTRA: Focus on security best practices"
    elif request_type == "optimization":
        return f"{base}\n\nEXTRA: Prioritize performance and efficiency"
    return base
```

### User Customization
Allow users to override parts of system prompt:
```python
/customprompt Add "Always use TypeScript" to system instructions
```

### A/B Testing
Test different system prompts:
```python
# v1: Current system prompt
# v2: More aggressive fix suggestions
# v3: More conservative approach
```

---

This integration makes the system prompt the source of truth for bot behavior, ensuring consistency and quality across all code modifications.
