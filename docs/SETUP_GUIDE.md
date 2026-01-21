# WhatsApp AI Customer Support & Order System - Complete Setup Guide

## Table of Contents
1. [System Overview](#system-overview)
2. [Prerequisites](#prerequisites)
3. [Step-by-Step Setup](#step-by-step-setup)
4. [WhatsApp Integration](#whatsapp-integration)
5. [Hugging Face Setup](#hugging-face-setup)
6. [Database Setup](#database-setup)
7. [Running the System](#running-the-system)
8. [Admin Console](#admin-console)
9. [Deployment](#deployment)
10. [API Endpoints](#api-endpoints)
11. [Troubleshooting](#troubleshooting)
12. [Best Practices](#best-practices)

## System Overview

This system provides:
- **WhatsApp AI Assistant**: Answers customer questions using Hugging Face AI
- **Automated Order Management**: Customers can order products via WhatsApp
- **Admin Console**: Desktop GUI to manage orders, products, and chat logs
- **Multi-Customer Support**: Handles multiple concurrent conversations
- **SQLite Database**: Stores orders, customers, products, and chat logs
- **REST API**: For integration with other systems

### Architecture Diagram
```
WhatsApp → Twilio → Flask Backend → SQLite DB
                  ↓
          Hugging Face AI (for responses)
                  ↑
          Admin Console (PyQt5 GUI)
```

## Prerequisites

### Required Software
- **Python 3.8+** (Download from python.org)
- **Visual Studio Code** (or Visual Studio)
- **Git** (Optional, for version control)
- **ngrok** (For tunneling - free version at ngrok.com)

### Required Accounts (All Free)
1. **Twilio Account** (Free tier: $15 credit)
   - Sign up at twilio.com
   - Enable WhatsApp sandbox
   
2. **Hugging Face Account**
   - Sign up at huggingface.co
   - Generate API key
   
3. **Free Hosting (Optional)**
   - Heroku, Railway, or similar for production

## Step-by-Step Setup

### Step 1: Create Project Directory

```bash
# Navigate to your workspace
cd "c:\Users\<your-username>\Documents\Whatsapp ai\whatsapp-ai-system"

# You already have the structure, verify it exists:
dir
# Should show: backend, admin, database, docs folders
```

### Step 2: Set Up Python Virtual Environment

```bash
# Navigate to backend folder
cd backend

# Create virtual environment
python -m venv venv

# Activate it (Windows)
venv\Scripts\activate

# On Mac/Linux:
# source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
# Make sure you're in the backend directory with venv activated
pip install --upgrade pip setuptools wheel

# Install all requirements
pip install -r ..\requirements.txt

# Verify installation
pip list
```

### Step 4: Configure Environment Variables

```bash
# Go to project root
cd ..

# Copy the example file
copy .env.example .env

# Edit .env with your credentials (use Notepad or VS Code)
```

**Edit `.env` file with your credentials:**

```env
# Twilio WhatsApp Configuration
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_WHATSAPP_NUMBER=whatsapp:+1234567890

# Hugging Face API Key
HUGGINGFACE_API_KEY=hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Flask Configuration
FLASK_ENV=development
SECRET_KEY=change-this-to-a-random-string-in-production
FLASK_DEBUG=True

# Database
DATABASE_URL=sqlite:///whatsapp_ai.db

# Admin Credentials
ADMIN_USERNAME=admin
ADMIN_PASSWORD=secure_password_here

# Webhook (will set after ngrok setup)
WEBHOOK_URL=https://your_public_url.com/webhook/whatsapp
```

## WhatsApp Integration

### Getting Twilio Credentials

1. **Sign up for Twilio** (https://www.twilio.com/try-twilio)
   - Free account includes $15 credit
   - Verify your phone number

2. **Find Your Credentials**
   - Go to Twilio Console: https://console.twilio.com
   - Copy `Account SID` and `Auth Token`
   - Paste into `.env` file

3. **Enable WhatsApp Sandbox**
   - In Twilio Console, go to Messaging → WhatsApp → Sandbox
   - You'll see a phone number like `+1 415-523-8886`
   - Copy this and add `whatsapp:` prefix in `.env`
   - The message will show how to opt-in from your phone

4. **Opt-In to Sandbox**
   - Send from your phone: `join [two-word-code]` to the Twilio number
   - Example: `join purple-tiger`
   - You'll receive a confirmation

### Set Up Webhook

1. **Install ngrok** (https://ngrok.com/download)
   - Extract to a folder
   - Add to PATH or use full path

2. **Start ngrok** (in new terminal):
   ```bash
   ngrok http 5000
   ```
   - ngrok will show: `https://abc123.ngrok.io`
   - Copy this URL

3. **Configure Twilio Webhook**
   - In Twilio Console → Messaging → Settings
   - Webhook URL: `https://abc123.ngrok.io/webhook/whatsapp`
   - Update `.env` `WEBHOOK_URL` with this

4. **Update `.env` with ngrok URL**
   ```env
   WEBHOOK_URL=https://abc123.ngrok.io/webhook/whatsapp
   ```

## Hugging Face Setup

### Get Free API Key

1. **Sign up** at https://huggingface.co/join
2. **Go to Settings** → API tokens
3. **Create new token**
   - Select "Read" access
   - Copy token
4. **Paste in `.env`**
   ```env
   HUGGINGFACE_API_KEY=hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```

### Available Free Models

The system uses `mistral-7b-instruct` by default. Other free options:

- `gpt2` - Lightweight (Fast but less capable)
- `mistral-7b-instruct` - **Recommended** (Best balance)
- `meta-llama/Llama-2-7b-chat-hf` - Good quality (May have wait times)
- `bigcode/starcoder` - Good for technical questions

Change model in `.env`:
```env
HUGGINGFACE_MODEL=mistral-7b-instruct
```

## Database Setup

### Initialize Database

```bash
# Navigate to backend folder with venv activated
cd backend

# Start Python shell
python

# Then run:
from app import create_app, db
app = create_app()
with app.app_context():
    db.create_all()
    print("Database initialized!")

# Exit (Ctrl+D or type: exit())
```

### Add Sample Products

```bash
# While in Python shell (continuing from above):
from app.services import ProductService

# Add hoodies
products = [
    {
        'name': 'Classic Black Hoodie',
        'price': 49.99,
        'description': '100% cotton, comfortable fit',
        'category': 'hoodies',
        'sizes': 'XS,S,M,L,XL,XXL',
        'colors': 'Black',
        'stock': 50
    },
    {
        'name': 'Premium Gray Hoodie',
        'price': 59.99,
        'description': 'Premium cotton blend, soft interior',
        'category': 'hoodies',
        'sizes': 'XS,S,M,L,XL,XXL',
        'colors': 'Gray,Charcoal',
        'stock': 35
    },
    {
        'name': 'Sport Performance Hoodie',
        'price': 65.99,
        'description': 'Moisture-wicking, athletic fit',
        'category': 'performance',
        'sizes': 'S,M,L,XL,XXL',
        'colors': 'Blue,Black,Red',
        'stock': 25
    }
]

for p in products:
    ProductService.add_product(**p)
    print(f"Added: {p['name']}")

exit()
```

## Running the System

### Start the Backend Server

```bash
# Make sure you're in backend folder
cd backend

# Activate virtual environment (if not already active)
venv\Scripts\activate

# Run Flask server
python run.py

# You should see:
# 🚀 WhatsApp AI System Starting...
# 📱 Webhook URL: http://localhost:5000/webhook/whatsapp
# 🔐 Admin Panel: http://localhost:5000/admin/login
# 📊 API Base: http://localhost:5000/api
```

### In Another Terminal - Start ngrok

```bash
ngrok http 5000
```

### Start Admin Console (Optional)

```bash
# In a new terminal, navigate to admin folder
cd admin

# Activate virtual environment from backend
..\backend\venv\Scripts\activate

# Run admin console
python admin_console.py
```

## Admin Console

### Login
- **Username**: admin
- **Password**: (from `.env` ADMIN_PASSWORD)

### Features

1. **Orders Tab**
   - View all orders
   - Filter by status (pending, confirmed, shipped, delivered)
   - Update order status
   - Auto-refreshes every 30 seconds
   - Customer automatically notified when status changes

2. **Products Tab**
   - Add new products
   - Edit existing products
   - Manage inventory
   - Set categories and pricing

3. **Chat Logs Tab**
   - View all customer conversations
   - Filter by customer
   - See AI-generated responses
   - Monitor model performance

## Deployment

### Option 1: Deploy to Railway (Recommended for Beginners)

1. **Sign up** at railway.app
2. **Create new project**
3. **Connect GitHub repo** or upload files
4. **Add environment variables** from `.env`
5. **Deploy**

### Option 2: Deploy to Heroku

```bash
# Create Heroku account at heroku.com
# Install Heroku CLI

# Login
heroku login

# Create app
heroku create your-app-name

# Set environment variables
heroku config:set TWILIO_ACCOUNT_SID=xxxxx
heroku config:set TWILIO_AUTH_TOKEN=xxxxx
# ... set all from .env

# Deploy
git push heroku main
```

### Option 3: Deploy to Your Own Server

1. **Rent a VPS** (DigitalOcean, Linode, etc.) - $5/month
2. **Install Python and dependencies**
3. **Use Gunicorn** as production server:
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 run:app
   ```
4. **Use Nginx** as reverse proxy
5. **Get free SSL** with Let's Encrypt

## API Endpoints

### Public Endpoints (No auth required)

```
GET /api/products
GET /api/products?category=hoodies
GET /api/products/<id>
GET /api/orders/<order_number>/track
GET /api/health
```

### WhatsApp Webhook

```
POST /webhook/whatsapp
- Receives messages from Twilio
- Processes with AI
- Returns response
```

### Admin Endpoints (Requires login)

```
GET /admin/dashboard
GET /admin/orders?status=pending&limit=50
PUT /admin/orders/<id>/status (body: {"status": "confirmed"})
GET /admin/products
POST /admin/products (body: {product data})
PUT /admin/products/<id> (body: {updates})
DELETE /admin/products/<id>
GET /admin/chat-logs?customer_id=123
GET /admin/customers
```

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'twilio'"

**Solution:**
```bash
pip install -r requirements.txt
```

### Issue: "WhatsApp messages not received"

**Checklist:**
- [ ] Twilio credentials correct in `.env`
- [ ] ngrok running and URL in Twilio webhook settings
- [ ] You've opted into WhatsApp sandbox (sent "join" code)
- [ ] `.env` file has WEBHOOK_URL set correctly

### Issue: "Hugging Face API timeout"

**Solution:**
- API is overloaded (many free users)
- Add retry logic (already included in code)
- Or use different model with faster inference

### Issue: "Database locked"

**Solution:**
```bash
# Delete and recreate database
del whatsapp_ai.db

# Reinitialize
python
from app import create_app, db
app = create_app()
with app.app_context():
    db.create_all()
exit()
```

### Issue: Port 5000 already in use

```bash
# Find and kill process using port 5000
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Or use different port:
$env:PORT=5001  # PowerShell
flask run --port 5001
```

## Best Practices

### 1. Performance Optimization

**Reduce AI API calls:**
- FAQ database is used first (no API calls)
- Intent classification is local
- Implement caching for common questions

```python
# Example: Cache responses for 1 hour
from functools import lru_cache
from datetime import datetime

@lru_cache(maxsize=100)
def get_cached_response(question):
    return ai_service.generate_response(question)
```

### 2. Reliability

**Always use try-catch blocks:**
```python
try:
    response = whatsapp_service.send_message(phone, text)
except Exception as e:
    logger.error(f"Failed to send: {e}")
    # Implement retry logic
```

**Implement message queues** for high volume:
```bash
pip install redis
pip install celery
```

### 3. Security

**Never hardcode credentials:**
- Always use `.env` file
- Use strong `SECRET_KEY` in production
- Hash admin password in `.env`

**Validate all inputs:**
```python
from werkzeug.utils import secure_filename
filename = secure_filename(user_input)
```

### 4. Scalability

**Use connection pooling:**
```python
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_size': 10,
    'pool_recycle': 3600,
}
```

**Implement caching:**
```bash
pip install redis Flask-Caching
```

### 5. Monitoring

**Log all important events:**
```python
logger.info(f"Order created: {order_number}")
logger.error(f"AI failed: {error}")
logger.warning(f"Long response time: {time}ms")
```

**Monitor API usage:**
```python
import time

start = time.time()
response = huggingface_service.generate_response(msg)
elapsed = time.time() - start

if elapsed > 5:  # More than 5 seconds
    logger.warning(f"Slow AI response: {elapsed}s")
```

## Next Steps

1. **Customize FAQ responses** in `huggingface_service.py`
2. **Add more product categories**
3. **Implement email notifications** when orders arrive
4. **Add payment integration** (Stripe, PayPal)
5. **Multi-language support** using Hugging Face translation models
6. **Analytics dashboard** to track sales and popular products
7. **WhatsApp media handling** for product images
8. **Advanced AI features** like product recommendations

## Support & Resources

- **Twilio Docs**: https://www.twilio.com/docs/whatsapp
- **Flask Docs**: https://flask.palletsprojects.com
- **Hugging Face Docs**: https://huggingface.co/docs
- **SQLAlchemy ORM**: https://docs.sqlalchemy.org
- **PyQt5**: https://riverbankcomputing.com/software/pyqt/

## License

This project is open source. Feel free to modify and use for your business.

---

**Good luck with your WhatsApp AI system! 🚀**
