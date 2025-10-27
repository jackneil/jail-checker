# Deploying the Serverless Proxy to Vercel

The browser version requires a serverless proxy to handle session cookies. This is a **one-time setup** that takes 5 minutes.

## Why We Need This

The jail API requires session cookies which browsers can't handle due to CORS restrictions. Our serverless proxy:
- Runs on Vercel's free tier (no cost, no limits for this use case)
- Handles session cookies properly
- Allows the browser version to work from any computer

## One-Time Deployment Steps

### 1. Install Vercel CLI

Open PowerShell or Command Prompt:

```powershell
npm install -g vercel
```

(If you don't have npm/Node.js, download from: https://nodejs.org/)

### 2. Login to Vercel

```powershell
vercel login
```

This opens your browser - create a free account or login with GitHub.

### 3. Deploy

```powershell
cd C:\Github\jail-checker
vercel
```

Answer the prompts:
- **Set up and deploy?** `Y`
- **Which scope?** (select your account)
- **Link to existing project?** `N`
- **Project name?** `jail-checker` (or any name)
- **Directory?** `.` (current directory)
- **Override settings?** `N`

Vercel will deploy and give you a URL like: `https://jail-checker-abc123.vercel.app`

### 4. Update the HTML File

Open `web/custody-checker.html` and find this line (around line 684):

```javascript
const PROXY_URL = 'http://localhost:3000/api/jail-proxy';  // CHANGE THIS
```

Change it to your Vercel URL:

```javascript
const PROXY_URL = 'https://jail-checker-abc123.vercel.app/api/jail-proxy';
```

### 5. Done!

Now the HTML file will call YOUR proxy (which handles sessions) instead of trying to call the jail API directly.

## Updating Later

When you make changes to the proxy code:

```powershell
cd C:\Github\jail-checker
vercel --prod
```

## Testing Locally (Optional)

To test the proxy on your local machine before deploying:

```powershell
cd C:\Github\jail-checker
vercel dev
```

This starts a local server at `http://localhost:3000`

## Free Tier Limits

Vercel's free tier includes:
- 100 GB bandwidth/month
- Unlimited requests
- Perfect for this use case

For our jail checker with ~300 inmates and ~200 defendants:
- Each check uses ~5 MB bandwidth
- Free tier allows ~20,000 checks/month
- More than enough for daily use

## Troubleshooting

**"npm: command not found"**
- Install Node.js from https://nodejs.org/

**"vercel: command not found"**
- Restart PowerShell after installing Vercel CLI
- Or use: `npx vercel` instead of `vercel`

**Deployment fails**
- Make sure you're in the `C:\Github\jail-checker` directory
- Check that `api/jail-proxy.js` exists
- Try: `vercel --debug` for more info

**Getting 401 Unauthorized errors**
- Go to https://vercel.com/dashboard
- Find your "jail-checker" project
- Go to Settings → Deployment Protection
- Set to "Disabled" (this is a public API that needs browser access)

**Getting 404 errors after deployment**
- Make sure `vercel.json` is using simplified config (empty `{}` or removed)
- Vercel auto-detects the `api/` folder
- Redeploy with `vercel --prod`
