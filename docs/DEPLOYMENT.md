# Deployment Guide

## Production Checklist

Before deploying to production, ensure:

- [ ] All credentials in `.env` (never commit `.env` file)
- [ ] Database backed up
- [ ] SSL/HTTPS configured
- [ ] Error logging set up
- [ ] Monitor set up for failures
- [ ] Backup strategy in place
- [ ] Security headers configured
- [ ] Rate limiting enabled
- [ ] CORS properly configured
- [ ] Admin password is strong

## Option 1: Deploy to Railway (Recommended - Easiest)

Railway.app is perfect for beginners. Free tier includes $5/month credit.

### Step 1: Create Railway Account
1. Go to https://railway.app
2. Sign up with GitHub/email
3. Create new project

### Step 2: Connect Repository
1. Fork or upload to GitHub
2. In Railway: Connect GitHub repo
3. Select `whatsapp-ai-system` folder

### Step 3: Add Environment Variables
1. In Railway dashboard: Variables
2. Add all from `.env`:
   ```
   TWILIO_ACCOUNT_SID
   TWILIO_AUTH_TOKEN
   TWILIO_WHATSAPP_NUMBER
   HUGGINGFACE_API_KEY
   SECRET_KEY
   ADMIN_USERNAME
   ADMIN_PASSWORD
   DATABASE_URL=sqlite:///whatsapp_ai.db
   ```

### Step 4: Configure Start Command
1. Create `Procfile` in project root:
   ```
   web: cd backend && gunicorn -w 4 -b 0.0.0.0:$PORT run:app
   ```

### Step 5: Deploy
1. Push to GitHub
2. Railway auto-deploys
3. Get URL: `https://yourproject.up.railway.app`

### Step 6: Update Twilio Webhook
1. In Twilio Console
2. Set webhook to: `https://yourproject.up.railway.app/webhook/whatsapp`

---

## Option 2: Deploy to Heroku

Heroku is free tier is discontinued, but you can use paid tier ($7+/month).

### Step 1: Install Heroku CLI
```bash
# Download from heroku.com/products/heroku-cli
# Or with Chocolatey:
choco install heroku-cli
```

### Step 2: Login
```bash
heroku login
```

### Step 3: Create App
```bash
heroku create your-app-name
```

### Step 4: Set Environment Variables
```bash
heroku config:set TWILIO_ACCOUNT_SID=xxxxx
heroku config:set TWILIO_AUTH_TOKEN=xxxxx
heroku config:set TWILIO_WHATSAPP_NUMBER=xxxxx
heroku config:set HUGGINGFACE_API_KEY=xxxxx
heroku config:set SECRET_KEY=xxxxx
heroku config:set ADMIN_PASSWORD=xxxxx
```

### Step 5: Create Procfile
```
web: cd backend && gunicorn -w 4 -b 0.0.0.0:$PORT run:app
```

### Step 6: Deploy
```bash
git push heroku main
```

### Step 7: View Logs
```bash
heroku logs --tail
```

---

## Option 3: Deploy to Your Own Server

### VPS Options (Cheapest)
- DigitalOcean: $5-40/month
- Linode: $5-30/month
- Vultr: $2.50-12/month
- AWS EC2: Variable

### Step 1: Set Up Server

**Ubuntu/Debian:**
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python
sudo apt install python3 python3-pip python3-venv git -y

# Install Nginx (reverse proxy)
sudo apt install nginx -y

# Install Supervisor (process manager)
sudo apt install supervisor -y
```

### Step 2: Clone Project
```bash
cd /opt
sudo git clone <your-repo> whatsapp-ai
cd whatsapp-ai/backend
```

### Step 3: Set Up Python Environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r ../requirements.txt
```

### Step 4: Create Systemd Service
Create `/etc/systemd/system/whatsapp-ai.service`:
```ini
[Unit]
Description=WhatsApp AI System
After=network.target

[Service]
Type=notify
User=www-data
WorkingDirectory=/opt/whatsapp-ai/backend
Environment="PATH=/opt/whatsapp-ai/backend/venv/bin"
ExecStart=/opt/whatsapp-ai/backend/venv/bin/gunicorn \
    --workers 4 \
    --bind 127.0.0.1:5000 \
    --timeout 120 \
    run:app

Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### Step 5: Enable Service
```bash
sudo systemctl daemon-reload
sudo systemctl start whatsapp-ai
sudo systemctl enable whatsapp-ai
sudo systemctl status whatsapp-ai
```

### Step 6: Configure Nginx
Create `/etc/nginx/sites-available/whatsapp-ai`:
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 120;
    }

    # WebSocket support (if added later)
    location /socket.io {
        proxy_pass http://127.0.0.1:5000/socket.io;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "Upgrade";
    }
}
```

### Step 7: Enable Site
```bash
sudo ln -s /etc/nginx/sites-available/whatsapp-ai \
    /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Step 8: Get SSL Certificate (Free)
```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d yourdomain.com
```

### Step 9: Configure Firewall
```bash
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

### Step 10: Set Up Backups
```bash
# Create daily backup script
cat > /opt/whatsapp-ai/backup.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/backups/whatsapp-ai"
mkdir -p $BACKUP_DIR
DATE=$(date +%Y%m%d_%H%M%S)
cp /opt/whatsapp-ai/backend/whatsapp_ai.db \
    $BACKUP_DIR/whatsapp_ai_$DATE.db
find $BACKUP_DIR -mtime +7 -delete  # Keep 7 days
EOF

chmod +x /opt/whatsapp-ai/backup.sh

# Add to crontab
sudo crontab -e
# Add: 0 2 * * * /opt/whatsapp-ai/backup.sh
```

---

## Option 4: Docker Deployment

### Create Dockerfile
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "backend/run.py"]
```

### Create docker-compose.yml
```yaml
version: '3'
services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - TWILIO_ACCOUNT_SID=${TWILIO_ACCOUNT_SID}
      - TWILIO_AUTH_TOKEN=${TWILIO_AUTH_TOKEN}
      - HUGGINGFACE_API_KEY=${HUGGINGFACE_API_KEY}
      - SECRET_KEY=${SECRET_KEY}
    volumes:
      - ./backend/whatsapp_ai.db:/app/backend/whatsapp_ai.db
    restart: always
```

### Deploy
```bash
docker-compose up -d
```

---

## Monitoring & Maintenance

### View Logs
```bash
# Railway
railway logs

# Heroku
heroku logs -t

# Own server
sudo journalctl -u whatsapp-ai -f
```

### Monitor Database
```bash
# Check database size
ls -lh whatsapp_ai.db

# Cleanup old logs (keep last 100,000)
sqlite3 whatsapp_ai.db "DELETE FROM chat_logs WHERE id NOT IN (SELECT id FROM chat_logs ORDER BY id DESC LIMIT 100000);"
```

### Set Up Alerts
```bash
# Email alerts on crash (add to crontab)
*/5 * * * * systemctl is-active --quiet whatsapp-ai || \
  echo "WhatsApp AI crashed!" | mail -s "Alert!" admin@email.com
```

### Monitor Disk Usage
```bash
# Check disk space
df -h

# Find large files
du -sh /opt/whatsapp-ai/backend/*
```

---

## Performance Optimization for Production

### 1. Database Optimization
```python
# In run.py, before app.run()
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_size': 20,
    'pool_recycle': 3600,
    'pool_pre_ping': True,
}
```

### 2. Add Redis Caching
```bash
pip install redis Flask-Caching
```

```python
# In app/__init__.py
from flask_caching import Cache
cache = Cache(app, config={'CACHE_TYPE': 'redis'})

# In routes
@bp.route('/api/products')
@cache.cached(timeout=300)  # Cache for 5 minutes
def get_products():
    ...
```

### 3. Use Gunicorn with Multiple Workers
```bash
gunicorn -w 8 -b 0.0.0.0:5000 --worker-class sync --worker-connections 1000 run:app
```

### 4. Enable GZIP Compression
```python
from flask_compress import Compress
Compress(app)
```

### 5. Add Security Headers
```python
@app.after_request
def set_security_headers(response):
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    return response
```

---

## Troubleshooting Deployment

### App won't start
```bash
# Check logs for errors
heroku logs --tail  # Heroku
journalctl -u whatsapp-ai  # Own server

# Common issues:
# - Missing environment variables
# - Port already in use
# - Database connection error
```

### Webhook not working
```bash
# Test webhook URL
curl -X POST https://yourapp.com/webhook/whatsapp \
  -d "From=whatsapp:+1234567890&Body=test"

# Check Twilio webhook settings
# Make sure URL matches exactly
```

### Database errors
```bash
# Backup database before changes
cp whatsapp_ai.db whatsapp_ai.db.backup

# Check database integrity
sqlite3 whatsapp_ai.db "PRAGMA integrity_check;"

# Rebuild database if corrupted
# Delete old db and restart (will recreate)
```

---

**Deployment complete! Your WhatsApp AI system is now live!**
