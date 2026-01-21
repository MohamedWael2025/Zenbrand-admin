# Code Sample: Advanced Features

This file contains code samples for extending the system.

## 1. Multi-Language Support

```python
# Add to huggingface_service.py

from transformers import pipeline

class MultiLanguageService:
    """Support multiple languages using free Hugging Face models"""
    
    def __init__(self):
        # These models are free on Hugging Face
        self.translator = pipeline(
            "translation_en_to_es",  # English to Spanish
            model="Helsinki-NLP/opus-mt-en-es"
        )
        self.language_detector = pipeline(
            "text-classification",
            model="papluca/xlm-roberta-base-language-detection"
        )
    
    def detect_language(self, text):
        """Detect customer's language"""
        result = self.language_detector(text)
        return result[0]['label']  # Returns: 'es', 'en', 'fr', etc.
    
    def translate_response(self, english_response, target_language):
        """Translate AI response to customer's language"""
        if target_language == 'en':
            return english_response
        
        # For other languages, use appropriate translator
        result = self.translator(english_response, max_length=512)
        return result[0]['translation_text']

# Usage in WhatsApp route:
"""
from app.services import MultiLanguageService

@bp.route('/webhook/whatsapp', methods=['POST'])
def whatsapp_webhook():
    ...
    multi_lang = MultiLanguageService()
    customer_language = multi_lang.detect_language(message_body)
    
    # Generate response in English
    response = ai_service.generate_response(message_body)
    
    # Translate if needed
    if customer_language != 'en':
        response = multi_lang.translate_response(response, customer_language)
    
    whatsapp_service.send_message(phone, response)
    ...
"""
```

## 2. AI Product Recommendations

```python
# Add to huggingface_service.py

from sklearn.cosine_similarity import cosine_similarity
import numpy as np
from sentence_transformers import SentenceTransformer

class RecommendationService:
    """AI-powered product recommendations"""
    
    def __init__(self):
        # Free embeddings model
        self.model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    
    def get_recommendations(self, customer_message, products):
        """Get product recommendations based on customer message"""
        
        # Embed customer message
        customer_embedding = self.model.encode([customer_message])
        
        # Embed product descriptions
        product_embeddings = self.model.encode(
            [p.description for p in products]
        )
        
        # Calculate similarity
        similarities = cosine_similarity(customer_embedding, product_embeddings)[0]
        
        # Get top 3 products
        top_indices = np.argsort(similarities)[-3:][::-1]
        
        recommendations = [
            {
                'product': products[i],
                'score': float(similarities[i])
            }
            for i in top_indices
        ]
        
        return recommendations

# Usage:
"""
rec_service = RecommendationService()

if message_mentions_hoodie:
    recommendations = rec_service.get_recommendations(
        message_body,
        ProductService.get_all_products()
    )
    
    response = "Here are some hoodies you might like:\n\n"
    for rec in recommendations:
        p = rec['product']
        response += f"• {p.name} - ${p.price}\n"
"""
```

## 3. Email Notifications

```python
# Create new file: backend/app/services/email_service.py

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

class EmailService:
    """Send email notifications"""
    
    def __init__(self):
        self.sender_email = os.getenv('EMAIL_ADDRESS')
        self.sender_password = os.getenv('EMAIL_PASSWORD')
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
    
    def send_email(self, recipient, subject, body, is_html=False):
        """Send email"""
        try:
            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = self.sender_email
            message["To"] = recipient
            
            mime_type = "html" if is_html else "plain"
            message.attach(MIMEText(body, mime_type))
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.sendmail(self.sender_email, recipient, message.as_string())
            
            return True
        except Exception as e:
            print(f"Email error: {e}")
            return False
    
    def send_order_notification(self, customer_email, order):
        """Notify admin of new order"""
        subject = f"New Order: {order.order_number}"
        
        body = f"""
        <h2>New Order Received!</h2>
        <p><b>Order ID:</b> {order.order_number}</p>
        <p><b>Total:</b> ${order.total_amount}</p>
        <p><b>Items:</b></p>
        <ul>
        """
        
        for item in order.items:
            body += f"<li>{item.product_name} x{item.quantity}</li>"
        
        body += "</ul>"
        
        self.send_email(customer_email, subject, body, is_html=True)

# Usage in order_service.py:
"""
email_service = EmailService()
email_service.send_order_notification(
    "admin@yourshop.com",
    new_order
)
"""
```

## 4. Sentiment Analysis

```python
# Add to huggingface_service.py

class SentimentService:
    """Analyze customer sentiment and satisfaction"""
    
    def __init__(self):
        from transformers import pipeline
        self.sentiment_analyzer = pipeline(
            "sentiment-analysis",
            model="distilbert-base-uncased-finetuned-sst-2-english"
        )
    
    def analyze_message(self, message):
        """Analyze customer sentiment"""
        result = self.sentiment_analyzer(message[:512])  # Limit to 512 chars
        
        return {
            'sentiment': result[0]['label'],  # POSITIVE or NEGATIVE
            'score': result[0]['score'],      # 0-1
            'is_satisfied': result[0]['label'] == 'POSITIVE'
        }
    
    def should_escalate(self, message):
        """Check if customer is angry/upset"""
        sentiment = self.analyze_message(message)
        
        # Escalate if very negative
        return (sentiment['sentiment'] == 'NEGATIVE' and 
                sentiment['score'] > 0.9)

# Usage:
"""
sentiment_service = SentimentService()

if sentiment_service.should_escalate(customer_message):
    # Transfer to human support
    response = "I understand you're frustrated. Let me connect you with our support team."
    whatsapp_service.send_message(phone, response)
    # Send alert to admin
"""
```

## 5. Analytics Dashboard

```python
# Create new file: backend/app/routes/analytics.py

from flask import Blueprint, jsonify
from datetime import datetime, timedelta
from app.models import Order, ChatLog, Customer
from sqlalchemy import func

bp = Blueprint('analytics', __name__, url_prefix='/analytics')

@bp.route('/orders/daily', methods=['GET'])
def daily_orders():
    """Get orders per day for past 30 days"""
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    
    orders = db.session.query(
        func.date(Order.created_at).label('date'),
        func.count(Order.id).label('count'),
        func.sum(Order.total_amount).label('total')
    ).filter(
        Order.created_at >= thirty_days_ago
    ).group_by(
        func.date(Order.created_at)
    ).all()
    
    return jsonify({
        'daily_orders': [
            {
                'date': str(o.date),
                'count': o.count,
                'revenue': o.total
            }
            for o in orders
        ]
    })

@bp.route('/customers/growth', methods=['GET'])
def customer_growth():
    """Get new customers per day"""
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    
    customers = db.session.query(
        func.date(Customer.created_at).label('date'),
        func.count(Customer.id).label('count')
    ).filter(
        Customer.created_at >= thirty_days_ago
    ).group_by(
        func.date(Customer.created_at)
    ).all()
    
    return jsonify({
        'new_customers_daily': [
            {
                'date': str(c.date),
                'count': c.count
            }
            for c in customers
        ]
    })

@bp.route('/ai/performance', methods=['GET'])
def ai_performance():
    """Analyze AI response effectiveness"""
    logs = ChatLog.query.filter_by(
        ai_generated=True,
        message_type='outgoing'
    ).limit(1000).all()
    
    avg_confidence = sum([
        l.confidence_score for l in logs if l.confidence_score
    ]) / len([l for l in logs if l.confidence_score])
    
    return jsonify({
        'ai_responses_total': len(logs),
        'average_confidence': avg_confidence,
        'models_used': list(set([l.ai_model_used for l in logs]))
    })
```

## 6. Auto-Confirmation Feature

```python
# Add to huggingface_service.py

class OrderConfirmationService:
    """Automatic order confirmation based on confidence"""
    
    def should_auto_confirm(self, order, confidence_score):
        """
        Auto-confirm order if AI is very confident
        """
        # High confidence AND low value order = auto-confirm
        if confidence_score > 0.92 and order.total_amount < 100:
            return True
        return False
    
    def requires_human_review(self, order):
        """Flag orders needing human attention"""
        issues = []
        
        if not order.shipping_address:
            issues.append("No shipping address")
        if order.total_amount > 500:
            issues.append("High value order")
        if len(order.items) > 10:
            issues.append("Large order quantity")
        
        return len(issues) > 0, issues
```

## 7. Scheduled Tasks (Reminders, Notifications)

```python
# Create new file: backend/scheduler.py

from apscheduler.schedulers.background import BackgroundScheduler
from app.models import Order
from app.services import WhatsAppService
from datetime import datetime, timedelta

scheduler = BackgroundScheduler()
whatsapp_service = WhatsAppService()

@scheduler.scheduled_job('interval', minutes=30)
def check_pending_orders():
    """Notify about pending orders every 30 minutes"""
    pending = Order.query.filter_by(status='pending').all()
    
    for order in pending:
        age = datetime.utcnow() - order.created_at
        if age > timedelta(hours=2):  # More than 2 hours pending
            whatsapp_service.send_templated_message(
                f"whatsapp:{order.customer.phone_number}",
                'order_update',
                {'order_number': order.order_number}
            )

@scheduler.scheduled_job('interval', hours=24)
def send_daily_report():
    """Send daily report to admin"""
    # Implementation
    pass

def start_scheduler(app):
    """Start background tasks"""
    scheduler.start()
    print("Scheduler started!")

# In run.py:
"""
from scheduler import start_scheduler
...
start_scheduler(app)
"""
```

## 8. Payment Integration (Stripe)

```bash
pip install stripe
```

```python
# Create new file: backend/app/services/payment_service.py

import stripe
import os

stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

class PaymentService:
    """Handle payments via Stripe"""
    
    @staticmethod
    def create_checkout_session(order_id, customer_email):
        """Create Stripe checkout session"""
        try:
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': f'Order #{order_id}',
                        },
                        'unit_amount': 5000,  # $50.00
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url='https://yourdomain.com/success',
                cancel_url='https://yourdomain.com/cancel',
                customer_email=customer_email,
            )
            return session.url
        except Exception as e:
            print(f"Payment error: {e}")
            return None
```

---

These samples can be integrated into your system for advanced features!
