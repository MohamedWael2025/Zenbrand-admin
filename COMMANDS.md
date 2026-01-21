# WhatsApp AI System - Useful Commands

## Development Commands

```bash
# Setup virtual environment
cd backend
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run development server
python run.py

# Run admin console
cd admin
python admin_console.py

# Reset database
del whatsapp_ai.db
python -c "from app import create_app, db; app = create_app(); db.create_all()"
```

## Database Commands

```bash
# Interactive SQLite shell
sqlite3 whatsapp_ai.db

# Query customers
SELECT * FROM customers;

# Query orders
SELECT * FROM orders;

# Count messages
SELECT COUNT(*) FROM chat_logs;

# Export data
.headers on
.mode csv
.output export.csv
SELECT * FROM orders;
.quit
```

## API Testing

```bash
# Test health endpoint
curl http://localhost:5000/api/health

# Get products
curl http://localhost:5000/api/products

# Track order
curl http://localhost:5000/api/orders/ORD-20240119-ABC12345/track

# Get customer orders
curl http://localhost:5000/api/customers/1234567890/orders
```

## Admin API

```bash
# Login
curl -c cookies.txt -X POST http://localhost:5000/admin/login \
  -d "username=admin&password=admin123"

# Get orders (using saved cookies)
curl -b cookies.txt http://localhost:5000/admin/orders

# Update order status
curl -b cookies.txt -X PUT http://localhost:5000/admin/orders/1/status \
  -H "Content-Type: application/json" \
  -d '{"status":"confirmed"}'

# Add product
curl -b cookies.txt -X POST http://localhost:5000/admin/products \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","price":49.99,"category":"hoodies","stock":10}'
```

## Troubleshooting

```bash
# Check Python version
python --version

# List installed packages
pip list

# Check port usage (Windows)
netstat -ano | findstr :5000

# Kill process on port 5000 (Windows)
taskkill /PID <PID> /F

# View Flask debug info
export FLASK_ENV=development
export FLASK_DEBUG=True

# Run with verbose logging
FLASK_ENV=development python run.py
```

## Production Commands

```bash
# Install production server
pip install gunicorn

# Run with gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 run:app

# Run with auto-reload
gunicorn -w 4 -b 0.0.0.0:5000 --reload run:app

# Run on specific port
gunicorn -w 4 -b 0.0.0.0:8000 run:app

# Check gunicorn config
gunicorn --help
```

## Docker Commands (if using Docker)

```bash
# Build image
docker build -t whatsapp-ai .

# Run container
docker run -p 5000:5000 -e TWILIO_ACCOUNT_SID=xxx whatsapp-ai

# With docker-compose
docker-compose up -d
docker-compose logs -f
docker-compose stop
```

## Useful Python Commands

```bash
# Start Python interactive shell
python

# In shell:
from app import create_app, db
from app.models import Product
from app.services import ProductService

app = create_app()
with app.app_context():
    # List all products
    products = Product.query.all()
    for p in products:
        print(f"{p.name} - ${p.price}")
    
    # Add product
    ProductService.add_product(
        name="New Product",
        price=39.99,
        description="Description",
        category="hoodies"
    )
    
    # Query orders
    from app.models import Order
    orders = Order.query.all()

exit()
```

## Git Commands

```bash
# Initialize git repo
git init
git add .
git commit -m "Initial commit"

# Push to GitHub
git remote add origin https://github.com/username/whatsapp-ai.git
git push -u origin main

# Update from remote
git pull origin main
```

## Environment Setup

```bash
# Copy example env
copy .env.example .env

# Or on Mac/Linux
cp .env.example .env

# Edit with your values
# Required:
# - TWILIO_ACCOUNT_SID
# - TWILIO_AUTH_TOKEN
# - TWILIO_WHATSAPP_NUMBER
# - HUGGINGFACE_API_KEY
# - SECRET_KEY
# - ADMIN_PASSWORD
```

## Performance Monitoring

```bash
# Check database size
ls -lh whatsapp_ai.db

# Check system resources
top  # Linux/Mac
taskmgr  # Windows

# Profile Python code
python -m cProfile -s cumulative run.py

# Memory usage
pip install memory-profiler
python -m memory_profiler run.py
```

## Backup & Recovery

```bash
# Backup database
cp whatsapp_ai.db whatsapp_ai.db.backup

# Backup env file
cp .env .env.backup

# Restore from backup
cp whatsapp_ai.db.backup whatsapp_ai.db

# List database tables
sqlite3 whatsapp_ai.db ".tables"

# Export database
sqlite3 whatsapp_ai.db ".dump" > backup.sql

# Import database
sqlite3 new.db < backup.sql
```

## Common Issues

```bash
# ModuleNotFoundError - reinstall dependencies
pip install --force-reinstall -r requirements.txt

# Port 5000 in use - find and kill process
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Database locked - delete and recreate
del whatsapp_ai.db

# Import error - check Python path
python -m app

# SSL certificate error
pip install --upgrade certifi
```

## Logging

```bash
# Enable debug logging in Python
import logging
logging.basicConfig(level=logging.DEBUG)

# View Flask logs
export FLASK_ENV=development
python run.py 2>&1 | tee app.log

# Tail logs (Unix)
tail -f app.log

# Search logs for errors
grep "ERROR" app.log
```

This file is for quick reference. For detailed guides, see the docs/ folder.
