# ⚡ WAHA Quick Reference Card

```
┌─────────────────────────────────────────────────────────────────┐
│                    WAHA SETUP - 5 COMMANDS                       │
└─────────────────────────────────────────────────────────────────┘

1️⃣  INSTALL DOCKER
   → https://www.docker.com/products/docker-desktop/

2️⃣  DOWNLOAD WAHA
   docker pull devlikeapro/waha

3️⃣  GENERATE CREDENTIALS
   docker run --rm -v "${PWD}:/app/env" devlikeapro/waha init-waha /app/env
   📝 Save the API key!

4️⃣  START WAHA
   docker run -it --env-file ".env" -v "${PWD}/sessions:/app/.sessions" --rm -p 3000:3000 --name waha devlikeapro/waha

5️⃣  CONNECT WHATSAPP
   → http://localhost:3000/dashboard
   → Login → Start Session → Scan QR → WORKING ✅

┌─────────────────────────────────────────────────────────────────┐
│                    RUNNING THE SYSTEM                            │
└─────────────────────────────────────────────────────────────────┘

TERMINAL 1 - WAHA
docker run -it --env-file ".env" -v "${PWD}/sessions:/app/.sessions" --rm -p 3000:3000 --name waha devlikeapro/waha

TERMINAL 2 - FLASK BACKEND
cd backend
venv\Scripts\activate
python run.py

TERMINAL 3 - NGROK
ngrok http 5000

WEBHOOK CONFIG (use ngrok URL from terminal 3)
curl -X POST http://localhost:3000/api/sessions/default \
  -H "X-Api-Key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name":"default","config":{"webhooks":[{"url":"https://YOUR_NGROK_URL.ngrok.io/webhook/whatsapp","events":["message"]}]}}'

┌─────────────────────────────────────────────────────────────────┐
│                        TEST COMMANDS                             │
└─────────────────────────────────────────────────────────────────┘

SEND MESSAGE (replace YOUR_API_KEY and PHONE)
curl -X POST http://localhost:3000/api/sendText \
  -H "X-Api-Key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"chatId":"PHONE@c.us","text":"Hello!","session":"default"}'

CHECK SESSION STATUS
curl -X GET http://localhost:3000/api/sessions/default \
  -H "X-Api-Key: YOUR_API_KEY"

VIEW WAHA LOGS
docker logs -f waha

┌─────────────────────────────────────────────────────────────────┐
│                    TROUBLESHOOTING                               │
└─────────────────────────────────────────────────────────────────┘

❌ Port 3000 in use
   → docker stop waha

❌ QR not showing
   → Stop session → Wait 10s → Start again

❌ Session disconnected
   → Restart WAHA: docker restart waha
   → Or re-scan QR code

❌ Webhook not working
   → Check ngrok: curl YOUR_NGROK_URL/webhook/whatsapp
   → Verify webhook in WAHA dashboard

❌ Messages not sending
   → Check session status (should be WORKING)
   → Verify API key in .env
   → Test manually with curl

┌─────────────────────────────────────────────────────────────────┐
│                        .ENV FILE                                 │
└─────────────────────────────────────────────────────────────────┘

WAHA_API_KEY=00000000000000000000000000000000
WAHA_BASE_URL=http://localhost:3000
WAHA_SESSION_NAME=default
WAHA_WEBHOOK_SECRET=your_secret

HUGGINGFACE_API_KEY=hf_xxxxxxxxxxxxx
HUGGINGFACE_MODEL=mistral-7b-instruct

SECRET_KEY=your-secret-key
ADMIN_PASSWORD=admin123
DATABASE_URL=sqlite:///whatsapp_ai.db

┌─────────────────────────────────────────────────────────────────┐
│                      USEFUL URLS                                 │
└─────────────────────────────────────────────────────────────────┘

📊 WAHA Dashboard:     http://localhost:3000/dashboard
🔌 WAHA API Docs:      http://localhost:3000
🎛️  Admin Console:     http://localhost:5000/admin/login
📡 Flask API:          http://localhost:5000/api/health

┌─────────────────────────────────────────────────────────────────┐
│                    ADMIN CONSOLE                                 │
└─────────────────────────────────────────────────────────────────┘

DESKTOP GUI
cd admin
python admin_console.py

WEB ADMIN
http://localhost:5000/admin/login
Username: admin
Password: admin123

┌─────────────────────────────────────────────────────────────────┐
│                    WHATSAPP COMMANDS                             │
└─────────────────────────────────────────────────────────────────┘

Send these messages from any WhatsApp to your number:

"hi" or "hello"           → AI greeting
"catalog"                 → See product list
"order"                   → Check your orders
"what are hoodies?"       → AI product info
"how to order?"           → AI FAQ response

┌─────────────────────────────────────────────────────────────────┐
│                     DOCKER COMMANDS                              │
└─────────────────────────────────────────────────────────────────┘

START WAHA
docker run -it --env-file ".env" -v "${PWD}/sessions:/app/.sessions" --rm -p 3000:3000 --name waha devlikeapro/waha

STOP WAHA
docker stop waha

RESTART WAHA
docker restart waha

VIEW LOGS
docker logs -f waha

CHECK STATUS
docker ps

REMOVE CONTAINER
docker rm waha

┌─────────────────────────────────────────────────────────────────┐
│                   COST COMPARISON                                │
└─────────────────────────────────────────────────────────────────┘

                    TWILIO          WAHA
Monthly Cost        $15-100         $0
Messages/Month      2,000-10,000    Unlimited
Phone Number        Sandbox         Your real number
Setup Time          20 min          15 min
Annual Cost         $180-1,200      $0

💰 ANNUAL SAVINGS: $180-1,200

┌─────────────────────────────────────────────────────────────────┐
│                    DOCUMENTATION                                 │
└─────────────────────────────────────────────────────────────────┘

📖 START_WITH_WAHA.md           → Quick overview
📖 WAHA_MIGRATION_GUIDE.md      → Complete setup guide
📖 docs/WAHA_SETUP.md           → Detailed WAHA docs
📖 docs/QUICK_START.md          → 15-min quick start
📖 README.md                    → Project overview
📖 docs/API_REFERENCE.md        → API endpoints
📖 docs/DEPLOYMENT.md           → Production deployment

┌─────────────────────────────────────────────────────────────────┐
│                   PHONE NUMBER FORMATS                           │
└─────────────────────────────────────────────────────────────────┘

WAHA FORMAT:     1234567890@c.us
OLD FORMAT:      whatsapp:+1234567890

⚠️  Use WAHA format in all API calls!
⚠️  No "+" or "whatsapp:" prefix needed

┌─────────────────────────────────────────────────────────────────┐
│                      SESSION STATES                              │
└─────────────────────────────────────────────────────────────────┘

STOPPED      → Session not started
STARTING     → Initializing (wait 10-15s)
SCAN_QR      → Ready for QR scan 📷
WORKING      → Connected ✅ (ready to use!)
FAILED       → Error (restart session)

┌─────────────────────────────────────────────────────────────────┐
│                    PRODUCTION TIPS                               │
└─────────────────────────────────────────────────────────────────┘

✅ Use Docker Compose for easier management
✅ Set up HTTPS with reverse proxy (Nginx/Caddy)
✅ Backup sessions/ folder regularly
✅ Use environment variables for secrets
✅ Monitor WAHA logs
✅ Set restart policy: --restart unless-stopped

PRODUCTION COMMAND:
docker run -d --restart unless-stopped \
  --env-file ".env" \
  -v "${PWD}/sessions:/app/.sessions" \
  -p 3000:3000 \
  --name waha \
  devlikeapro/waha

┌─────────────────────────────────────────────────────────────────┐
│                        SUPPORT                                   │
└─────────────────────────────────────────────────────────────────┘

📖 Read: WAHA_MIGRATION_GUIDE.md
🔍 Search: https://waha.devlike.pro/
💬 Discuss: https://github.com/devlikeapro/waha/discussions
🐛 Report: https://github.com/devlikeapro/waha/issues

```

---

## ⚡ ONE-LINER SETUP

Copy and paste this entire block:

```powershell
# Windows PowerShell
docker pull devlikeapro/waha; `
docker run --rm -v "${PWD}:/app/env" devlikeapro/waha init-waha /app/env; `
Write-Host "`n✅ WAHA installed! Now update .env file and run: docker run -it --env-file '.env' -v '${PWD}/sessions:/app/.sessions' --rm -p 3000:3000 --name waha devlikeapro/waha"
```

```bash
# Mac/Linux
docker pull devlikeapro/waha && \
docker run --rm -v "$(pwd):/app/env" devlikeapro/waha init-waha /app/env && \
echo "\n✅ WAHA installed! Now update .env file and run: docker run -it --env-file '.env' -v '\$(pwd)/sessions:/app/.sessions' --rm -p 3000:3000 --name waha devlikeapro/waha"
```

---

**💡 TIP:** Bookmark this file for quick reference!

**🚀 Ready to start?** Open `START_WITH_WAHA.md` or `WAHA_MIGRATION_GUIDE.md`
