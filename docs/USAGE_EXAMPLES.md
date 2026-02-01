# 📖 BugFixer Bot - Usage Examples

This guide shows real-world examples of how to use BugFixer Bot to fix various types of bugs.

## Table of Contents
1. [Basic Bug Fixes](#basic-bug-fixes)
2. [Emergency Production Issues](#emergency-production-issues)
3. [Logic Errors](#logic-errors)
4. [API Issues](#api-issues)
5. [Frontend Bugs](#frontend-bugs)
6. [Best Practices](#best-practices)

---

## Basic Bug Fixes

### Example 1: Typo in Code

**Your message:**
```
There's a typo in the login function - "pasword" should be "password"
```

**Bot's response:**
```
🔍 Bug Analysis Complete

Issue: There's a typo in the login function - "pasword" should be "password"

Proposed Fix:
Fixed typo in authentication module where 'pasword' was misspelled as 'password'

Files to modify: auth.py

Changes:
- Line 45: user.pasword → user.password
- Line 67: check_pasword() → check_password()

[✅ Apply Fix] [🔄 Revise] [❌ Cancel]
```

---

### Example 2: Wrong Variable Name

**Your message:**
```
/fix The user profile page shows undefined for email address
```

**Bot's response:**
```
🔍 Bug Analysis Complete

Issue: The user profile page shows undefined for email address

Proposed Fix:
Fixed undefined email in profile component by correcting variable name from 'user.mail' to 'user.email'

Files to modify: components/Profile.jsx

Changes:
- Line 23: {user.mail} → {user.email}

[✅ Apply Fix] [🔄 Revise] [❌ Cancel]
```

---

## Emergency Production Issues

### Example 3: Server Crash

**Your message:**
```
URGENT! Production server crashing with "TypeError: Cannot read property 'id' of undefined" in payment processing
```

**Bot's response:**
```
🔍 Bug Analysis Complete

Issue: Production server crashing with TypeError in payment processing

Proposed Fix:
Added null check for user object before accessing id property in payment handler

Root Cause: Payment webhook receives events before user object is fully loaded

Files to modify: 
- api/payments.js
- middleware/auth.js

Changes:
api/payments.js:
+ if (!user || !user.id) {
+   return res.status(400).json({ error: 'Invalid user' });
+ }
  const payment = await processPayment(user.id, amount);

Confidence: high

[✅ Apply Fix] [🔄 Revise] [❌ Cancel]
```

---

### Example 4: Database Connection Error

**Your message:**
```
Users getting 500 errors - logs show "too many database connections"
```

**Bot's response:**
```
🔍 Bug Analysis Complete

Issue: Database connection pool exhausted

Proposed Fix:
Increased connection pool size and added proper connection cleanup

Files to modify: 
- config/database.js
- models/User.js

Changes:
config/database.js:
- pool: { max: 5 }
+ pool: { max: 20, min: 5, idle: 10000 }

models/User.js:
+ Added connection.release() in finally blocks

[✅ Apply Fix] [🔄 Revise] [❌ Cancel]
```

---

## Logic Errors

### Example 5: Math Calculation Bug

**Your message:**
```
Shopping cart total is wrong when applying discount codes - it's calculating (price * discount) instead of (price - discount)
```

**Bot's response:**
```
🔍 Bug Analysis Complete

Issue: Incorrect discount calculation in shopping cart

Proposed Fix:
Fixed discount calculation logic to subtract discount from price instead of multiplying

Files to modify: utils/cart.js

Changes:
- const total = price * (1 + discount);
+ const total = price * (1 - discount);

Or for fixed amount discounts:
- const total = price * discount;
+ const total = Math.max(0, price - discount);

[✅ Apply Fix] [🔄 Revise] [❌ Cancel]
```

---

### Example 6: Date Comparison Bug

**Your message:**
```
Event reminder system is sending notifications for past events
```

**Bot's response:**
```
🔍 Bug Analysis Complete

Issue: Past events receiving notifications

Proposed Fix:
Fixed date comparison to check if event is in the future before sending notification

Files to modify: services/notifications.js

Changes:
- if (event.date < Date.now()) {
+ if (event.date > Date.now()) {
    sendNotification(user, event);
  }

[✅ Apply Fix] [🔄 Revise] [❌ Cancel]
```

---

## API Issues

### Example 7: Missing API Key

**Your message:**
```
API calls to weather service failing with 401 - I think we forgot to include the API key header
```

**Bot's response:**
```
🔍 Bug Analysis Complete

Issue: Missing API key in weather service requests

Proposed Fix:
Added API key to request headers

Files to modify: services/weather.js

Changes:
const response = await fetch(url, {
  method: 'GET',
+ headers: {
+   'X-API-Key': process.env.WEATHER_API_KEY
+ }
});

Also added:
- Check for missing API key in .env
- Better error handling for 401 responses

[✅ Apply Fix] [🔄 Revise] [❌ Cancel]
```

---

### Example 8: Wrong HTTP Method

**Your message:**
```
/fix Delete user endpoint not working - getting 405 Method Not Allowed
```

**Bot's response:**
```
🔍 Bug Analysis Complete

Issue: Wrong HTTP method for delete user endpoint

Proposed Fix:
Changed route from GET to DELETE for user deletion endpoint

Files to modify: routes/users.js

Changes:
- router.get('/users/:id', deleteUser);
+ router.delete('/users/:id', deleteUser);

[✅ Apply Fix] [🔄 Revise] [❌ Cancel]
```

---

## Frontend Bugs

### Example 9: CSS Styling Issue

**Your message:**
```
Button on mobile is cut off - text overflows the button container
```

**Bot's response:**
```
🔍 Bug Analysis Complete

Issue: Button text overflow on mobile devices

Proposed Fix:
Added proper text wrapping and padding to button styles

Files to modify: styles/Button.css

Changes:
.button {
+ white-space: normal;
+ word-wrap: break-word;
+ padding: 12px 16px;
+ min-height: 44px;
}

[✅ Apply Fix] [🔄 Revise] [❌ Cancel]
```

---

### Example 10: React State Update Issue

**Your message:**
```
Form doesn't update when user types - value stays empty
```

**Bot's response:**
```
🔍 Bug Analysis Complete

Issue: Controlled input not updating state

Proposed Fix:
Added onChange handler to update state when input value changes

Files to modify: components/Form.jsx

Changes:
<input
  value={email}
+ onChange={(e) => setEmail(e.target.value)}
  placeholder="Email"
/>

[✅ Apply Fix] [🔄 Revise] [❌ Cancel]
```

---

## Best Practices

### ✅ DO: Be Specific

**Good:**
```
Login button on /auth page returns 500 error when email contains special characters
```

**Bad:**
```
Login broken
```

---

### ✅ DO: Include Error Messages

**Good:**
```
Getting "ReferenceError: userData is not defined" on line 45 of profile.js
```

**Bad:**
```
Profile page has an error
```

---

### ✅ DO: Mention the File/Component

**Good:**
```
In UserSettings.jsx, the save button doesn't trigger the API call
```

**Bad:**
```
Save button doesn't work
```

---

### ✅ DO: Describe Expected Behavior

**Good:**
```
Search should return results sorted by date, but it's sorting by name instead
```

**Bad:**
```
Search results are wrong
```

---

### ❌ DON'T: Send Multiple Issues at Once

**Instead of:**
```
Fix the login bug and also the search is slow and the navbar is misaligned
```

**Do this:**
```
Message 1: Login button doesn't work on mobile Safari
Message 2: Search takes 5+ seconds to return results
Message 3: Navbar menu items are misaligned on tablets
```

---

### ❌ DON'T: Be Too Vague

**Instead of:**
```
Something is wrong with the database
```

**Be specific:**
```
User queries are failing with "connection timeout" after 30 seconds
```

---

## Advanced Usage Tips

### Using Context from Previous Messages

The bot remembers your repository, so you can have a conversation:

```
You: Fix the authentication bug in login.js
Bot: [Shows fix for login.js]
You: Also check the session handler - it might have the same issue
Bot: [Analyzes session.js and proposes related fix]
```

---

### Revising Fixes

If the proposed fix isn't quite right:

```
Bot: [Proposes a fix]
You: [Click "🔄 Revise"]
You: The fix should use bcrypt for password hashing, not plain text comparison
Bot: [Proposes updated fix with bcrypt]
```

---

### Multiple Related Fixes

For complex issues requiring multiple files:

```
You: The shopping cart has several issues:
1. Total calculation is wrong
2. Discount codes don't apply
3. Tax isn't calculated for international orders

Can you analyze the cart.js file and propose fixes for all three?
```

Bot will propose a comprehensive fix addressing all issues.

---

## Example Workflow: From Bug to Deployed Fix

### Real-world scenario: You're at a coffee shop and production breaks

**9:00 AM** - You get an alert
```
📱 Alert: High error rate on /api/checkout
```

**9:01 AM** - You check logs on your phone and message the bot
```
You: URGENT - checkout API returning 500 errors. 
Logs show "Cannot read property 'items' of null" in cart.calculateTotal()
```

**9:02 AM** - Bot analyzes
```
Bot: 🔍 Analyzing bug...
Bot: 📊 Fetching repository code...
Bot: 🤖 AI is analyzing the issue...
```

**9:03 AM** - Bot proposes fix
```
Bot: ✅ Bug Analysis Complete

Issue: Null pointer exception in cart total calculation

Proposed Fix:
Added null check for cart.items before calculating total

Files to modify: api/cart.js

Changes:
+ if (!cart || !cart.items) {
+   throw new Error('Invalid cart');
+ }
  const total = cart.items.reduce(...);

[✅ Apply Fix] [🔄 Revise] [❌ Cancel]
```

**9:04 AM** - You approve
```
You: [Click "✅ Apply Fix"]
```

**9:05 AM** - Bot creates PR
```
Bot: ✅ Fix Applied Successfully!

Branch: bugfix/auto-fix-12345-1234567890
Pull Request: #156
Files Modified: 1

[🔗 View PR]
```

**9:06 AM** - You review and merge on your phone
```
[On GitHub mobile app]
✓ Tests passing
✓ Code looks good
✓ Merge PR
```

**9:07 AM** - Deploy
```
[Your CI/CD automatically deploys]
✅ Deployed to production
```

**9:08 AM** - Crisis averted! ☕

You fixed a production bug, reviewed the code, and deployed—all from your phone at a coffee shop.

---

## Need Help?

If you're stuck or the bot isn't understanding your bug description:

1. Try being more specific about:
   - Which file/function has the issue
   - What the error message says
   - What you expected vs what happened

2. Use the `/help` command for tips

3. Check the bot logs for any errors

4. Review the README.md for setup issues

---

**Happy Bug Fixing! 🐛→✨**
