# Quick Start - 15 Minutes with WAHA (FREE!)

## TL;DR Setup

### 1. Install Python & Dependencies (3 min)

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r ..\requirements.txt
```

### 2. Install Docker & WAHA (5 min)

**Install Docker:**
- Windows/Mac: Download [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- Linux: `sudo apt-get install docker.io`

**Setup WAHA:**
```bash
# Download WAHA image
docker pull devlikeapro/waha

# Initialize credentials
docker run --rm -v "${PWD}:/app/env" devlikeapro/waha init-waha /app/env

# Run WAHA (keep this terminal open)
docker run -it --env-file "${PWD}/.env" -v "${PWD}/sessions:/app/.sessions" --rm -p 3000:3000 --name waha devlikeapro/waha
```

Save the credentials shown (username, password, API key)!

### 3. Connect WhatsApp via QR Code (2 min)

1. Open http://localhost:3000/dashboard
2. Login with credentials from Step 2
3. Enter API key to connect
4. Click **Start Session** on "default" session
5. When status shows `SCAN_QR`, click the camera icon 📷
6. **Scan QR code with your WhatsApp** (like WhatsApp Web)
7. Status changes to `WORKING` ✅

### 4. Get Hugging Face API Key (2 min)

- Go to https://huggingface.co/settings/tokens
- Create new token (Read access)
- Copy the token

### 5. Configure Environment (1 min)

**Create `.env` file in project root:**
```env
# WAHA Configuration
WAHA_API_KEY=00000000000000000000000000000000
WAHA_BASE_URL=http://localhost:3000
WAHA_SESSION_NAME=default
WAHA_WEBHOOK_SECRET=your_webhook_secret

# Hugging Face
HUGGINGFACE_API_KEY=hf_xxxxxxxxxxxxx
HUGGINGFACE_MODEL=mistral-7b-instruct

# Flask
SECRET_KEY=my-secret-key
ADMIN_PASSWORD=admin123
DATABASE_URL=sqlite:///whatsapp_ai.db
```

Replace `WAHA_API_KEY` with the one from Step 2!

### 6. Run System (2 min)

**Terminal 1 - WAHA (already running from Step 2):**
```bash
# Should already be running on port 3000
```

**Terminal 2 - Backend:**
```bash
cd backend
python run.py
```

**Terminal 3 - ngrok (for webhook):**
```bash
ngrok http 5000
```

**Copy ngrok URL** (e.g., `https://abc123.ngrok.io`)

### 7. Configure WAHA Webhook (1 min)

Tell WAHA where to send incoming messages:

```bash
curl -X POST http://localhost:3000/api/sessions/default \
  -H "X-Api-Key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "default",
    "config": {
      "webhooks": [{
        "url": "https://YOUR_NGROK_URL.ngrok.io/webhook/whatsapp",
        "events": ["message"]
      }]
    }
  }'
```

Replace `YOUR_API_KEY` and `YOUR_NGROK_URL`!

### 8. Test It! 🎉

**From another WhatsApp account:**
- Send message to your number: "Hi"
- AI should respond automatically!
- Send "catalog" to see products
- Send "order" to check orders

**Admin Console (Optional):**
```bash
cd admin
python admin_console.py
```

Or visit: `http://localhost:5000/admin/login`
Login: admin / admin123

## File Structure

```
whatsapp-ai-system/
├── backend/
│   ├── app/
│   │   ├── models/          # Database models
│   │   ├── services/        # Business logic
│   │   ├── routes/          # Flask endpoints
│   │   └── __init__.py
│   ├── run.py              # Main entry point
│   └── venv/               # Virtual environment
├── admin/
│   └── admin_console.py    # Desktop GUI
├── database/
│   └── whatsapp_ai.db      # SQLite (created automatically)
├── requirements.txt        # Python dependencies
├── .env                    # Configuration (KEEP SECRET!)
└── docs/
    ├── SETUP_GUIDE.md
    └── API_REFERENCE.md
```

## Key Features Enabled

✅ WhatsApp messaging via WAHA (FREE!)  
✅ Your actual WhatsApp number (no business API needed)  
✅ AI responses using Hugging Face  
✅ Order management with SQLite  
✅ Product catalog  
✅ Admin console to manage everything  
✅ Chat logs for analytics  

## Why WAHA vs Twilio?

| Feature |Python environment
venv\Scripts\activate

# Run Flask backend
cd backend
python run.py

# Start WAHA
docker run -it --env-file ".env" -v "${PWD}/sessions:/app/.sessions" --rm -p 3000:3000 --name waha devlikeapro/waha

# Stop WAHA
docker stop waha

# Check WAHA logs
docker logs waha

# Install new Python package
pip install package_name
💰 **WAHA saves you $180-1,200/year!**  

## Common Commands

```bash
# Activate environment
venv\Scripts\activate

# Install new package
pip install package_name

# Run backend
python run.py

# Check database
sqlite3 whatsapp_ai.db ".tables"

# Port 3000 in use | `docker stop waha` then restart |
| WAHA not working | Check Docker is running, check `.env` file |
| QR code not showing | Stop and start session again in dashboard |
| Webhook not working | Verify ngrok URL in WAHA webhook config |
| Admin won't connect | Make sure backend is running on port 5000 |
| No AI responses | Check `HUGGINGFACE_API_KEY` in `.env` |
| Session disconnected | Re-scan QR code in WAHA dashboard |

## Next: Customize It

1. Edit product list in database
2. Modify FAQ responses in `huggingface_service.py`
3. Customize welcome message in `whatsapp.py`
4. Add your business logic to services
5. Read **docs/WAHA_SETUP.md** for detailed WAHA configuration

---

**Need help?**  
- **WAHA Setup**: See `docs/WAHA_SETUP.md`  
- **Complete Guide**: See `docs/SETUP_GUIDE.md`  
- **API Reference**: See `docs/API_REFERENCE.md`
## Next: Customize It

1. Edit product list in database
2. Modify FAQ responses in `huggingface_service.py`
3. Customize welcome message in `whatsapp.py`
4. Add your business logic to services

---

**Need help? Check SETUP_GUIDE.md for detailed instructions**
