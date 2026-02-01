# Example: How to integrate SYSTEM_PROMPT.md into bugfixer_bot.py
# This shows the exact code changes needed

"""
STEP 1: Add to BugFixerBot.__init__() around line 46
"""

class BugFixerBot:
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
        
        # ===== ADD THIS NEW CODE =====
        self.system_prompt = self._load_system_prompt()
        # =============================
    
    # ===== ADD THIS NEW METHOD =====
    def _load_system_prompt(self) -> str:
        """Load system prompt from SYSTEM_PROMPT.md"""
        try:
            prompt_path = os.path.join(os.path.dirname(__file__), 'SYSTEM_PROMPT.md')
            with open(prompt_path, 'r') as f:
                content = f.read()
                logger.info("✅ System prompt loaded successfully")
                return content
        except FileNotFoundError:
            logger.warning("⚠️ SYSTEM_PROMPT.md not found, using default")
            return """
You are an AI code assistant that helps fix bugs, create features, and manage code.

Operating Principles:
1. Safety First - Never push directly to main branch
2. Clear Communication - Explain what you're doing
3. Autonomous but Controlled - Keep humans in control
4. Context Aware - Understand the repository structure

Always:
- Ask for clarification if request is vague
- Show proposed changes before applying
- Require user approval for all changes
- Create pull requests, not direct commits
"""
    # ================================


"""
STEP 2: Modify analyze_code_with_ai() method to use system prompt
Works with ALL providers: Anthropic, OpenRouter, and Groq
Find the method around line 400-600 and update it like this:
"""

async def analyze_code_with_ai(
    self, 
    code_context: str, 
    request: str, 
    request_type: str,  # "fix", "feature", "change", "create"
    api_provider: str,  # "anthropic", "openrouter", or "groq"
    api_key: str
) -> dict:
    """
    Send code to any AI provider for analysis using system prompt
    
    Works with:
    - Anthropic (Claude API)
    - OpenRouter (400+ models: Claude, Llama, etc.)
    - Groq (Fast open source models)
    
    Args:
        code_context: The relevant code from the repository
        request: The user's request (bug description, feature request, etc.)
        request_type: Type of request - "fix", "feature", "change", "create"
        api_provider: Which AI provider - "anthropic", "openrouter", "groq"
        api_key: API key for the provider
    """
    
    # ===== NEW: Build system message using system prompt =====
    system_message = f"""{self.system_prompt}

---

## Current Task Configuration

**Request Type:** {request_type.upper()}
**Task:** {request}

Please analyze the provided repository code and propose {request_type} changes.
Your response MUST be valid JSON with this structure:
{{
    "summary": "Brief explanation of what you're implementing",
    "files": ["list", "of", "affected", "filenames"],
    "changes": {{"path/to/file.py": "full new file content here"}},
    "explanation": "Detailed explanation of your approach and why it works",
    "notes": "Any edge cases, testing suggestions, security considerations"
}}
"""
    # ========================================================
    
    user_message = f"""
## Repository Code Context:

{code_context}

## {request_type.upper()} REQUEST:

{request}

Please provide your analysis as JSON (see format above).
"""
    
    try:
        # ===== ANTHROPIC (Claude) =====
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
                    "messages": [
                        {
                            "role": "user",
                            "content": user_message
                        }
                    ]
                }
            )
            
            result = response.json()
            content = result['content'][0]['text']
            
            # Parse JSON response
            try:
                solution = json.loads(content)
            except json.JSONDecodeError:
                # Extract JSON from text if wrapped
                import re
                json_match = re.search(r'\{.*\}', content, re.DOTALL)
                if json_match:
                    solution = json.loads(json_match.group())
                else:
                    raise ValueError("Invalid JSON response from Claude")
            
            return solution
        
        # ===== OPENROUTER (400+ models) =====
        elif api_provider == "openrouter":
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://github.com/bugfixer",
                },
                json={
                    "model": "auto",  # Auto-selects best model available
                    "max_tokens": 4096,
                    "system": system_message,  # ← System prompt here
                    "messages": [
                        {
                            "role": "user",
                            "content": user_message
                        }
                    ]
                }
            )
            
            result = response.json()
            content = result['choices'][0]['message']['content']
            
            # Parse JSON response
            try:
                solution = json.loads(content)
            except json.JSONDecodeError:
                import re
                json_match = re.search(r'\{.*\}', content, re.DOTALL)
                if json_match:
                    solution = json.loads(json_match.group())
                else:
                    raise ValueError("Invalid JSON response from OpenRouter")
            
            return solution
        
        # ===== GROQ (Fast inference) =====
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
                    "messages": [
                        {
                            "role": "user",
                            "content": user_message
                        }
                    ]
                }
            )
            
            result = response.json()
            content = result['choices'][0]['message']['content']
            
            # Parse JSON response
            try:
                solution = json.loads(content)
            except json.JSONDecodeError:
                import re
                json_match = re.search(r'\{.*\}', content, re.DOTALL)
                if json_match:
                    solution = json.loads(json_match.group())
                else:
                    raise ValueError("Invalid JSON response from Groq")
            
            return solution
        
        else:
            raise ValueError(f"Unknown AI provider: {api_provider}")
            
    except Exception as e:
        logger.error(f"Error analyzing code with {api_provider}: {str(e)}")
        raise


"""
STEP 3: Usage example in process_code_task()
The method already calls analyze_code_with_ai(), just needs the system 
prompt to be loaded (done in Step 1)

No changes needed here - it will automatically use the system prompt!
"""

async def process_code_task(
    self, 
    update: Update, 
    context: ContextTypes.DEFAULT_TYPE, 
    task_description: str,
    task_type: str = "fix"
) -> None:
    """
    Main workflow: task → analyze → propose → apply
    
    The system prompt is automatically used in analyze_code_with_ai()
    """
    user_id = update.effective_user.id
    
    # ... existing validation code ...
    
    # Fetch code context from GitHub
    code_context = await self.get_code_context(context.user_data['repo'])
    
    # Analyze using Claude (with system prompt automatically)
    solution = await self.analyze_code_with_ai(
        code_context=code_context,
        request=task_description,
        request_type=task_type,  # ← This determines system prompt behavior
        api_provider=context.user_data['ai_provider'],
        api_key=context.user_data['ai_key']
    )
    
    # ... rest of existing code ...


"""
BENEFITS OF THIS INTEGRATION:

1. CONSISTENCY
   - All requests follow the same guidelines
   - Claude knows the operating principles
   - Safety rules are enforced

2. TRANSPARENCY
   - System prompt is in SYSTEM_PROMPT.md
   - Users can see and modify bot behavior
   - Open source friendly

3. MAINTAINABILITY
   - Change prompt → change bot behavior
   - No code changes needed
   - Easier to test different approaches

4. QUALITY
   - Claude provides better analysis
   - Follows best practices
   - Includes edge case considerations

5. EXTENSIBILITY
   - Easy to add new request types
   - Customize for different use cases
   - Support domain-specific rules
"""
