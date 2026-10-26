---
name: create-account-in-chrome
description: Use whenever a task requires CREATING an online account / signing up / registering credentials, OR a first-time login whose credentials must land in the user's password manager. Triggers — "crée un compte", "inscris-moi", "il faut créer un compte", "sign up", "register an account", OR any automated (Playwright/MCP) flow that hits a registration or login wall. NEVER fill signup/login forms in the automation browser — it is an isolated browser WITHOUT the user's profile or password manager, so any account made there is lost to their vault. Instead, open the EXACT target URL in the user's real browser so THEY type and save the credentials.
---

# Create account in the user's browser (not in the automation browser)

## Why this exists
The Playwright/MCP browser is an **isolated Chromium** with no access to the user's browser profile or **password manager**. If an account is created (or a password typed) inside it, the credentials are **never saved to their vault** — they lose them. So account creation and first logins must happen in **their real browser**, where the password manager offers to save the password.

## When to trigger
- The flow needs a **new account** (signup/registration) on any site.
- A first **login** where the credentials should be captured by the password manager.
- An automated flow reaches an **auth wall** (login / "create an account").
- The user says: « crée un compte », « inscris-moi », « il faut créer un compte », « sign up », « register »…

## Hard rules
- **NEVER** type a password into the automation browser.
- **NEVER** click the final "Create account" / "Sign up" / "Submit" there for credential creation — hand it over.
- Non-secret fields (first name, last name, e-mail) MAY be prepared as copy-paste text, but the **actual submission happens in the user's browser, by the user**.

## Procedure
1. **Stop** automating the signup/login in the automation browser. Say so explicitly.
2. **Open the exact URL in the user's real browser** (default profile + password manager):
   - Linux: `xdg-open "<URL>"` · macOS: `open "<URL>"` · Windows: `Start-Process "<URL>"` (opens the default browser).
   - Use the **precise** signup/registration URL, not a generic homepage, so they land directly on the form.
3. **Brief the user**: which page just opened, exactly what to create/fill (give the non-secret values to paste), and remind them that **the browser will offer to save the password** → accept it.
4. **Wait** for their confirmation that the account is created and the credentials are saved.
5. **Resume** only after that. If the remaining flow is behind the login:
   - Prefer continuing **in their browser** (already authenticated there), or
   - If automation must continue in Playwright, the user **dictates the credentials live** when needed — never fetch them from disk or memory.

## Notes
- This applies to ALL account-creation contexts (administrative portals, SaaS, developer tools…).
- A captcha, 2FA or e-mail-confirmation step is one more reason to do it in the user's browser, where they control their inbox and devices.
