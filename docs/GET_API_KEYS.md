# Step-by-Step API Keys Setup - WAHA Edition

This guide walks you through getting all the API keys and tools you need - **100% FREE!**

## 1. Docker Desktop (5 minutes)

WAHA runs on Docker, so you need Docker Desktop installed first.

### Step 1: Download Docker Desktop
1. Go to https://www.docker.com/products/docker-desktop/
2. Download for your operating system:
   - **Windows 10/11**: Docker Desktop for Windows
   - **Mac**: Docker Desktop for Mac (Intel or Apple Silicon)
   - **Linux**: See https://docs.docker.com/engine/install/

### Step 2: Install Docker
1. Run the installer
2. **Windows**: Restart your computer when prompted
3. **Mac**: Drag Docker.app to Applications folder
4. Open Docker Desktop and wait for it to start (green icon in system tray)

### Step 3: Verify Installation
Open PowerShell (Windows) or Terminal (Mac/Linux):

```bash
docker --version
```

Should show: `Docker version 24.x.x` or similar

**✅ Docker is ready!**

---

## 2. WAHA (WhatsApp HTTP API) - 100% FREE! (3 minutes)

WAHA connects your actual WhatsApp account to the system. No signup, no credit card!

### Step 1: Download WAHA Image
Open PowerShell/Terminal in your project folder:

```bash
cd "c:\Users\mohamed wael\Documents\Whatsapp ai\whatsapp-ai-system"
docker pull devlikeapro/waha
```

**Output:**
```
latest: Pulling from devlikeapro/waha
...
Status: Downloaded newer image for devlikeapro/waha:latest
```

⏱️ Takes 2-3 minutes depending on internet speed.

### Step 2: Generate WAHA Credentials

**Windows PowerShell:**
```powershell
docker run --rm -v "${PWD}:/app/env" devlikeapro/waha init-waha /app/env
```

**Mac/Linux:**
```bash
docker run --rm -v "$(pwd)":/app/env devlikeapro/waha init-waha /app/env
```

**Output:**
```
Credentials generated.

Dashboard and Swagger:
  - Username: admin
  - Password: 11111111111111111111111111111111

API key: 
  - 00000000000000000000000000000000
```

### Step 3: Save These Credentials!

Copy the values from the output:
- **API Key**: `00000000000000000000000000000000` (long string)
- **Username**: `admin`
- **Password**: `11111111111111111111111111111111` (long string)

This creates a `.env` file in your folder with these credentials.

Your WAHA section in `.env` should look like:
```env
WAHA_API_KEY=00000000000000000000000000000000
WAHA_BASE_URL=http://localhost:3000
WAHA_SESSION_NAME=default
WAHA_WEBHOOK_SECRET=your_random_secret_here
WAHA_DASHBOARD_USERNAME=admin
WAHA_DASHBOARD_PASSWORD=11111111111111111111111111111111
```

**✅ WAHA credentials ready!**

**Cost:** $0 - Completely FREE forever!

---

## 3. Hugging Face API Key (3 minutes)

### Step 1: Sign Up
1. Go to https://huggingface.co/join
2. Create account (Free!)
3. Verify email

### Step 2: Generate API Key
1. Click your profile picture (top right)
2. Select **Settings**
3. Go to **Access Tokens** section
4. Click **New token**

### Step 3: Create Token
- Name: "WhatsApp AI System"
- Access: **Read** (you only need to read from models)
- Click **Create token**
- Copy the token (starts with `hf_`)

Your Hugging Face section in `.env`:
```env
HUGGINGFACE_API_KEY=hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### Step 4: Test It Works
```bash
# In Python shell:
import requests
import os

api_key = "hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxx"
model_id = "mistral-7b-instruct"
api_url = f"https://api-inference.huggingface.co/models/{model_id}"

headers = {"Authorization": f"Bearer {api_key}"}
payload = {"inputs": "Hello, how are you?"}

response = requests.post(api_url, headers=headers, json=payload)
print(response.json())
```

If you get a response (not an error), you're good!

---

## 4. ngrok for Local Development (2 minutes)

ngrok creates a public URL for your local computer. WAHA needs this to send webhooks to your Flask backend.

### Step 1: Download & Install
1. Go to https://ngrok.com/download
2. Download for your OS (Windows/Mac/Linux)
3. **Windows**: Extract to a folder (e.g., `C:\ngrok`)
4. **Mac**: Unzip and move to `/usr/local/bin/` (or any folder in PATH)
5. **Optional**: Add to PATH so you can run `ngrok` from anywhere

### Step 2: Sign Up (Free Account)
1. Go to https://ngrok.com/signup
2. Sign up (free, no credit card)
3. Get your authtoken from https://dashboard.ngrok.com/get-started/your-authtoken
4. Connect your account:
   ```bash
   ngrok config add-authtoken YOUR_AUTHTOKEN
   ```

### Step 3: Run ngrok
Open a new PowerShell/Terminal window:

```bash
ngrok http 5000
```

You'll see:
```
Forwarding    https://abc123-def456.ngrok.io -> http://localhost:5000
```

**Copy the `https://` URL!** (Changes every time you restart ngrok)

### Step 4: Update WAHA Webhook (After Flask is Running)

You'll configure this later using WAHA's dashboard or API:
5
```env
WEBHOOK_URL=https://abc123-def456.ngrok.io/webhook/whatsapp
```

**Note:** Every time you restart ngrok, you get a new URL. You'll need to update WAHA webhook settings each time.

---

## 4. Optional: Other Free Models

By default, we use `mistral-7b-instruct`. You can change to:

| Model | Speed | Quality | Use Case |
|-------|-------|---------|----------|
| `gpt2` | ⚡ Fast | Basic | Quick responses |
| `mistral-7b-instruct` | ⚡⚡ Medium | ⭐⭐⭐ Good | **Recommended** |
| `meta-llama/Llama-2-7b-chat-hf` | ⚡⚡ Medium | ⭐⭐⭐ Good | Alternative |
| `bigcode/starcoder` | ⚡⚡⚡ Slow | ⭐⭐⭐⭐ Great | Technical questions |

Change in `.env`:
```env
HUGGINGFACE_MODEL=gpt2
```

---

## 6. Complete .env Example

Here's a complete `.env` file with all keys filled in:

```env
# WAHA WhatsApp Configuration (100% FREE!)
WAHA_API_KEY=00000000000000000000000000000000
WAHA_BASE_URL=http://localhost:3000
WAHA_SESSION_NAME=default
WAHA_WEBHOOK_SECRET=your_random_secret_here_change_this
WAHA_DASHBOARD_USERNAME=admin
WAHA_DASHBOARD_PASSWORD=11111111111111111111111111111111

# Hugging Face API Key (FREE!)
HUGGINGFACE_API_KEY=hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxx
HUGGINGFACE_MODEL=mistral-7b-instruct

# Flask Configuration
FLASK_ENV=development
SECRET_KEY=my-super-secret-key-change-in-production
FLASK_DEBUG=True

# Database
DATABASE_URL=sqlite:///whatsapp_ai.db

# Admin Credentials
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123

# Webhook Configuration (will be your ngrok URL)
WEBHOOK_URL=https://abc123-def456.ngrok.io/webhook/whatsapp
```
7. Troubleshooting

### "Docker not working"
- [ ] Check Docker Desktop is running (green icon in system tray)
- [ ] Windows: Make sure WSL2 is installed
- [ ] Mac: Allow Docker in System Preferences → Security
- [ ] Run `docker --version` to verify

### "WAHA not starting"
- [ ] Check Docker is running
- [ ] Check port 3000 is not in use: `netstat -ano | findstr :3000`
- [ ] Check `.env` file exists and has WAHA_API_KEY
- [ ] Try stopping and restarting: `docker stop waha` then start again

### "QR code not showing"
- [ ] Make sure WAHA is running (check http://localhost:3000/dashboard)
- [ ] Make sure session status is `SCAN_QR` (not `STARTING` or `STOPPED`)
- [ ] Click "Stop Session" wait 10 seconds, then "Start Session" again
- [ ] Check WAHA logs: `docker logs waha`

### "Hugging Face API error"
- [ ] Check API key starts with `hf_`
- [ ] Check model name is spelled correctly
- [ ] Check you have internet connection
- [ ] Wait a moment and try again (API might be slow with free tier)

### "Connection refused" or "404 Not Found"
- [ ] Make sure Flask app is running (`python run.py`)
- [ ] Make sure ngrok is running (`ngrok http 5000`)
- [ ] Check ngrok URL is configured in WAHA webhook settings

### "Webhook URL not working"
- [ ] ngrok must be running
- [ ] URL must start with `https://`
- [ ] URL must end with `/webhook/whatsapp`
- [ ] WAHA webhook must be configured with your ngrok URL
- [8. Testing Before Going Live

### Test 1: Is Docker Working?
```bash
docker --version
docker ps
# Should show Docker version and running containers
```

### Test 2: Is WAHA Running?
Open browser: http://localhost:3000/dashboard
- Should show WAHA dashboard login page
- Login with username/password from `.env`

### Test 3: Is Flask Working?
```bash
cd backend
python run.py
# Should show: "WhatsApp AI System Starting..."
# Should show: "Running on http://127.0.0.1:5000"
```

### Test 4: Is ngrok Working?
```bash
ngrok http 5000
# Should show forwarding URL like: https://abc123-def456.ngrok.io
```

### Test 5: Is Webhook Reachable?
```bash
# In new terminal (use YOUR ngrok URL):
curl https://abc123-def456.ngrok.io/webhook/whatsapp
# Should return: {"status":"ok","service":"WAHA WhatsApp Webhook"}
```
9. Cost Summary

| Service | Cost | Why Free? |
|---------|------|-----------|
| **WAHA** | **$0** | **Open source - FREE FOREVER!** |
| **Hugging Face** | **$0** | Generous free tier |
| **ngrok** | **$0** | Free plan sufficient for development |
| **Docker** | **$0** | Free for personal use |
| **Database** | **$0** | SQLite is embedded |
| **Messages** | **$0** | **UNLIMITED - No fees!** |
| **Total Setup** | **$0** | **Completely FREE!** |

### Cost Comparison

| Feature | Twilio (Old) | WAHA (New) |
|---------|--------------|------------|
| Monthly Cost | $15-100 | **$0** |
| Message Limit | 2,000-10,000 | **Unlimited** |
| Phone Number | Sandbox/Business | **Your real WhatsApp** |
| Annual Cost | $180-1,200 | **$0** |

**💰 You save $180-1,200 per year with WAHA!**

Check your WhatsApp - you should receive the message!

###10. Quick Reference - All API Keys & URLs

```env
# WAHA (Get from: docker run init-waha)
WAHA_API_KEY=00000000000000000000000000000000
WAHA_BASE_URL=http://localhost:3000
WAHA_SESSION_NAME=default

# Hugging Face (Get from: https://huggingface.co/settings/tokens)
HUGGINGFACE_API_KEY=hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxx

# ngrok (Get from: ngrok http 5000 output)
WEBHOOK_URL=https://YOUR_NGROK_URL.ngrok.io/webhook/whatsapp

# System (Change these!)
SECRET_KEY=your-secret-key-change-this
ADMIN_PASSWORD=admin123
```

### Important URLs

| Service | URL | Purpose |
|---------|-----|---------|
| WAHA Dashboard | http://localhost:3000/dashboard | Manage WhatsApp connection |
| WAHA API Docs | http://localhost:3000 | API documentation |
| Flask Admin | http://localhost:5000/admin/login | Admin panel |
| Flask API | http://localhost:5000/api/health | Health check |
| Hugging Face | https://huggingface.co/settings/tokens | Get API key |
| ngrok Dashboard | https://dashboard.ngrok.com | Manage tunnels |
| Docker Hub | https://hub.docker.com/r/devlikeapro/waha | WAHA image |

---

## Next Steps After Setup

### Immediate (15 minutes)
1. ✅ Install Docker Desktop
2. ✅ Download WAHA image
3. ✅ Generate WAHA credentials
4. ✅ Get Hugging Face API key
5. ✅ Update `.env` file with all keys
6. ✅ Download ngrok

### Short Term (30 minutes)
1. ✅ Start WAHA: `docker run -it --env-file ".env" -v "${PWD}/sessions:/app/.sessions" --rm -p 3000:3000 --name waha devlikeapro/waha`
2. ✅ Open http://localhost:3000/dashboard and scan QR code
3. ✅ Start Flask backend: `python backend/run.py`
4. ✅ Start ngrok: `ngrok http 5000`
5. ✅ Configure WAHA webhook with ngrok URL
6. ✅ Send test WhatsApp message
7. ✅ Verify AI responds

### Medium Term (1 day)
1. → Read [WAHA_MIGRATION_GUIDE.md](../WAHA_MIGRATION_GUIDE.md) for detailed setup
2. → Add products to database using admin console
3. → Customize FAQ responses in `backend/app/services/huggingface_service.py`
4. → Test all features thoroughly

### Long Term (1 week)
1. → Deploy to production (see [DEPLOYMENT.md](DEPLOYMENT.md))
2. → Set up monitoring and backups
3. → Configure custom domain and HTTPS
4. → Add advanced features (see [ADVANCED_FEATURES.md](ADVANCED_FEATURES.md))

---

## Complete Setup Checklist

- [ ] Docker Desktop installed and running
- [ ] WAHA image downloaded (`docker pull devlikeapro/waha`)
- [ ] WAHA credentials generated (`docker run init-waha`)
- [ ] Hugging Face API key obtained
- [ ] ngrok downloaded and authtoken configured
- [ ] `.env` file created and filled with all keys
- [ ] Python virtual environment created
- [ ] Python dependencies installed (`pip install -r requirements.txt`)
- [ ] WAHA running on port 3000
- [ ] WhatsApp QR code scanned (session status: WORKING)
- [ ] Flask backend running on port 5000
- [ ] ngrok running and URL copied
- [ ] WAHA webhook configured with ngrok URL
- [ ] Test message sent via API successfully
- [ ] Test message received from WhatsApp successfully
- [ ] AI response working

---

Need help? Check these guides:

- **[START_WITH_WAHA.md](../START_WITH_WAHA.md)** - Quick overview
- **[WAHA_MIGRATION_GUIDE.md](../WAHA_MIGRATION_GUIDE.md)** - Complete setup guide
- **[WAHA_QUICK_REFERENCE.md](../WAHA_QUICK_REFERENCE.md)** - Command cheat sheet
- **[QUICK_START.md](QUICK_START.md)** - 15-minute quick start
- **[WAHA_SETUP.md](WAHA_SETUP.md)** - Detailed WAHA guide

**🎉 You're all set! Enjoy unlimited FREE WhatsApp messaging with AI!**
3. Should see: "Received message from..."

### Test 5: Is AI Working?
1. Send question to WhatsApp
2. Wait 5 seconds
3. Should get AI response

---

## Cost Summary

| Service | Cost | Why Free? |
|---------|------|-----------|
| Twilio WhatsApp | $0.0075/msg | Free $15 credit covers ~2,000 messages |
| Hugging Face | Free | Generous free tier |
| ngrok | Free | Free plan sufficient for development |
| Database | Free | SQLite is embedded |
| **Total** | **$0** | Completely free to try! |

---

## Next Steps After Setup

1. ✅ Get all API keys
2. ✅ Update `.env` file
3. ✅ Start Flask backend
4. ✅ Run ngrok
5. ✅ Send WhatsApp message
6. ✅ Get AI response
7. → Read [SETUP_GUIDE.md](SETUP_GUIDE.md) for full system setup
8. → Add products to database
9. → Customize FAQ responses
10. → Deploy to production

---

Need help? Check the [main setup guide](SETUP_GUIDE.md) or see [QUICK_START.md](QUICK_START.md) for 10-minute setup.
