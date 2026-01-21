# WAHA Setup Guide - WhatsApp HTTP API

WAHA (WhatsApp HTTP API) is a free, open-source solution that allows you to connect your actual WhatsApp account to the system via QR code. Unlike Twilio, WAHA requires **no monthly fees** or message credits!

## 📋 Table of Contents

- [What is WAHA?](#what-is-waha)
- [Requirements](#requirements)
- [Step 1: Install Docker](#step-1-install-docker)
- [Step 2: Download WAHA Image](#step-2-download-waha-image)
- [Step 3: Initialize WAHA](#step-3-initialize-waha)
- [Step 4: Run WAHA](#step-4-run-waha)
- [Step 5: Access the Dashboard](#step-5-access-the-dashboard)
- [Step 6: Start a Session](#step-6-start-a-session)
- [Step 7: Scan QR Code](#step-7-scan-qr-code)
- [Step 8: Configure Webhooks](#step-8-configure-webhooks)
- [Step 9: Test the Connection](#step-9-test-the-connection)
- [Troubleshooting](#troubleshooting)
- [Production Deployment](#production-deployment)

---

## What is WAHA?

WAHA is a Docker-based WhatsApp HTTP API that:
- ✅ **Free forever** - no subscription or message fees
- ✅ Uses your **real WhatsApp account** (not a business API)
- ✅ Simple **QR code authentication** like WhatsApp Web
- ✅ Full **REST API** for sending/receiving messages
- ✅ Built-in **Dashboard** for management
- ✅ Supports **media messages** (images, documents, etc.)
- ✅ Works on **Linux, Windows, and macOS**

---

## Requirements

You need only one thing:
- **Docker Desktop** (Windows/Mac) or **Docker Engine** (Linux)

### System Requirements
- **RAM**: Minimum 2GB, Recommended 4GB
- **Disk**: At least 2GB free space
- **OS**: Windows 10/11, macOS 10.14+, or any modern Linux

---

## Step 1: Install Docker

### Windows
1. Download [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop/)
2. Run the installer
3. Restart your computer
4. Open Docker Desktop and wait for it to start
5. Verify installation:
   ```powershell
   docker --version
   ```

### macOS
1. Download [Docker Desktop for Mac](https://www.docker.com/products/docker-desktop/)
2. Drag Docker.app to Applications
3. Open Docker from Applications
4. Verify installation:
   ```bash
   docker --version
   ```

### Linux (Ubuntu/Debian)
```bash
# Update package index
sudo apt-get update

# Install dependencies
sudo apt-get install ca-certificates curl gnupg

# Add Docker's official GPG key
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Set up repository
echo \
  "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io

# Verify installation
sudo docker --version
```

---

## Step 2: Download WAHA Image

Open your terminal (PowerShell on Windows, Terminal on Mac/Linux) and run:

```bash
docker pull devlikeapro/waha
```

**Output:**
```
latest: Pulling from devlikeapro/waha
...
Status: Downloaded newer image for devlikeapro/waha:latest
```

⏱️ **Time**: 2-5 minutes depending on internet speed

---

## Step 3: Initialize WAHA

Generate credentials and `.env` file:

### Windows (PowerShell)
```powershell
docker run --rm -v "${PWD}:/app/env" devlikeapro/waha init-waha /app/env
```

### macOS/Linux
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

Use it in the Dashboard connection flow: https://waha.devlike.pro/docs/how-to/dashboard/#api-key
```

📝 **Save these credentials!** You'll need them to access the dashboard.

This command creates a `.env` file in your current directory with:
- `WAHA_DASHBOARD_USERNAME` and `WAHA_DASHBOARD_PASSWORD`
- `WAHA_API_KEY`

---

## Step 4: Run WAHA

Start the WAHA server:

### Windows (PowerShell)
```powershell
docker run -it --env-file "${PWD}/.env" -v "${PWD}/sessions:/app/.sessions" --rm -p 3000:3000 --name waha devlikeapro/waha
```

### macOS/Linux
```bash
docker run -it --env-file "$(pwd)/.env" -v "$(pwd)/sessions:/app/.sessions" --rm -p 3000:3000 --name waha devlikeapro/waha
```

**What this does:**
- `--env-file`: Loads configuration from `.env`
- `-v sessions:/app/.sessions`: Saves WhatsApp session data
- `-p 3000:3000`: Exposes API on port 3000
- `--name waha`: Names the container "waha"

**Output:**
```
WAHA is running on http://localhost:3000
Dashboard: http://localhost:3000/dashboard
Swagger: http://localhost:3000
```

✅ Keep this terminal open! WAHA is now running.

---

## Step 5: Access the Dashboard

1. Open your browser
2. Go to: http://localhost:3000/dashboard
3. Login with credentials from Step 3:
   - **Username**: `admin`
   - **Password**: (the long string from `.env`)

![Dashboard Login](https://waha.devlike.pro/images/dashboard-login.png)

4. Enter your **API Key** (also from `.env`)
5. Click **Connect**

![Dashboard Connected](https://waha.devlike.pro/images/dashboard-connected.png)

---

## Step 6: Start a Session

1. In the dashboard, you'll see the **default** session with status `STOPPED`
2. Click **Start Session**
3. Leave all settings as default (or customize if needed)
4. Click **Start**

![Start Session](https://waha.devlike.pro/images/start-session.png)

⏳ Wait for status to change to `SCAN_QR` (10-15 seconds)

---

## Step 7: Scan QR Code

1. When status shows `SCAN_QR`, click the **camera icon** 📷
2. If you see "Click to reload QR", click it to refresh
3. You'll see a QR code (similar to WhatsApp Web)

![QR Code](https://waha.devlike.pro/images/qr-code.png)

4. **On your phone**:
   - Open WhatsApp
   - Tap **⋮** (Android) or **Settings** (iOS)
   - Tap **Linked Devices**
   - Tap **Link a Device**
   - Scan the QR code on your screen

5. ✅ Status will change to `WORKING`

![Session Working](https://waha.devlike.pro/images/session-working.png)

🎉 **Your WhatsApp is now connected!**

---

## Step 8: Configure Webhooks

WAHA needs to send incoming messages to your Flask backend.

### For Local Development (using ngrok)

1. **Install ngrok**:
   - Download from https://ngrok.com/download
   - Extract and place in your PATH

2. **Start ngrok** (in a new terminal):
   ```bash
   ngrok http 5000
   ```
   
   **Output:**
   ```
   Forwarding  https://abc123.ngrok.io -> http://localhost:5000
   ```

3. **Copy the ngrok URL** (e.g., `https://abc123.ngrok.io`)

4. **Configure WAHA webhook**:
   - In WAHA Dashboard, go to **Sessions** → **default** → **Settings**
   - Or use the API:
   
   ```bash
   curl -X POST http://localhost:3000/api/sessions/default \
     -H "X-Api-Key: YOUR_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "default",
       "config": {
         "webhooks": [{
           "url": "https://abc123.ngrok.io/webhook/whatsapp",
           "events": ["message"]
         }]
       }
     }'
   ```

5. **Update your `.env` file**:
   ```bash
   WAHA_BASE_URL=http://localhost:3000
   WEBHOOK_URL=https://abc123.ngrok.io/webhook/whatsapp
   ```

### For Production

Replace ngrok URL with your production domain:
```
https://yourdomain.com/webhook/whatsapp
```

---

## Step 9: Test the Connection

### Test 1: Send a Message via API

```bash
curl -X POST http://localhost:3000/api/sendText \
  -H "X-Api-Key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "chatId": "YOUR_PHONE_NUMBER@c.us",
    "text": "Hello from WAHA!",
    "session": "default"
  }'
```

Replace:
- `YOUR_API_KEY`: Your API key from `.env`
- `YOUR_PHONE_NUMBER`: Your phone number (no `+`, e.g., `1234567890`)

✅ You should receive the message on your WhatsApp!

### Test 2: Send a Message TO the Bot

1. From another WhatsApp account, send a message to your number
2. Check your Flask backend logs - you should see:
   ```
   Received message from 1234567890: Hello!
   ```

3. The AI should respond automatically!

---

## Troubleshooting

### QR Code Not Appearing
**Problem**: Session stuck at `STARTING` or shows error

**Solution**:
1. Stop the session
2. Wait 10 seconds
3. Start it again
4. Check Docker logs:
   ```bash
   docker logs waha
   ```

### Session Disconnected
**Problem**: Status changes to `FAILED` or `STOPPED`

**Solution**:
1. Check your phone's WhatsApp - you may need to re-scan
2. Restart WAHA:
   ```bash
   docker restart waha
   ```

### Webhook Not Working
**Problem**: Messages sent to WhatsApp but no response

**Solution**:
1. Verify ngrok is running:
   ```bash
   curl https://YOUR_NGROK_URL.ngrok.io/webhook/whatsapp
   ```
   Should return: `{"status": "ok"}`

2. Check WAHA webhook configuration:
   ```bash
   curl -X GET http://localhost:3000/api/sessions/default \
     -H "X-Api-Key: YOUR_API_KEY"
   ```

3. Verify Flask backend is running on port 5000

### Port Already in Use
**Problem**: `Error: Port 3000 is already allocated`

**Solution**:
1. Stop existing WAHA:
   ```bash
   docker stop waha
   ```

2. Or use a different port:
   ```bash
   docker run -it --env-file ".env" -p 3001:3000 --name waha devlikeapro/waha
   ```
   Then update `WAHA_BASE_URL=http://localhost:3001`

### Docker Not Running
**Problem**: `Cannot connect to Docker daemon`

**Solution**:
- **Windows/Mac**: Open Docker Desktop
- **Linux**: Start Docker service:
  ```bash
  sudo systemctl start docker
  ```

---

## Production Deployment

### Using Docker Compose

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  waha:
    image: devlikeapro/waha
    restart: unless-stopped
    ports:
      - "3000:3000"
    environment:
      - WAHA_DASHBOARD_USERNAME=${WAHA_DASHBOARD_USERNAME}
      - WAHA_DASHBOARD_PASSWORD=${WAHA_DASHBOARD_PASSWORD}
      - WAHA_API_KEY=${WAHA_API_KEY}
    volumes:
      - ./sessions:/app/.sessions
```

Start with:
```bash
docker-compose up -d
```

### Security Recommendations

1. **Change default credentials** in `.env`:
   - Use long, random strings (UUIDv4)
   - Never commit `.env` to version control

2. **Use HTTPS** in production:
   - Configure reverse proxy (Nginx/Caddy)
   - Get free SSL certificate (Let's Encrypt)

3. **Firewall rules**:
   - Only expose port 3000 to your backend
   - Don't expose publicly unless needed

4. **Backup sessions**:
   ```bash
   # Regular backups of sessions folder
   tar -czf sessions-backup-$(date +%Y%m%d).tar.gz sessions/
   ```

### Recommended Server Specs

For production:
- **CPU**: 2 cores
- **RAM**: 4GB
- **Disk**: 10GB SSD
- **Network**: Good connectivity

Handles ~10,000 messages/day comfortably.

---

## Next Steps

1. ✅ **Test the system**: Send WhatsApp messages and verify AI responses
2. 📝 **Customize FAQs**: Edit `backend/app/services/huggingface_service.py`
3. 🛍️ **Add products**: Use the admin console or API
4. 🚀 **Deploy to production**: Follow deployment guide
5. 📊 **Monitor**: Check logs and dashboard regularly

---

## Additional Resources

- [WAHA Official Documentation](https://waha.devlike.pro/)
- [WAHA GitHub Repository](https://github.com/devlikeapro/waha)
- [Docker Documentation](https://docs.docker.com/)
- [WAHA API Reference](https://waha.devlike.pro/docs/api/)

---

## Cost Comparison

| Service | Monthly Cost | Message Limit |
|---------|--------------|---------------|
| **WAHA** | **$0** | ♾️ Unlimited |
| Twilio WhatsApp | $15-100+ | ~2,000-10,000 |
| WhatsApp Business API | $25-500+ | Varies |

💰 **WAHA saves you $180-1,200 per year!**

---

## FAQ

**Q: Is WAHA legal?**  
A: Yes, WAHA uses the official WhatsApp Web protocol, just like WhatsApp Web.

**Q: Can I use multiple WhatsApp numbers?**  
A: Yes! Create multiple sessions (one per number).

**Q: Does my phone need to stay online?**  
A: No! Once connected, WAHA works independently (like WhatsApp Web).

**Q: What if my session expires?**  
A: Just scan the QR code again. Sessions last 30+ days usually.

**Q: Can I send images/files?**  
A: Yes! WAHA supports all WhatsApp media types. See API docs.

---

🎉 **Congratulations!** You've successfully set up WAHA for free WhatsApp integration!
