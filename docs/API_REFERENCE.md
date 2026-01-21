# API Reference

## Authentication

Most endpoints require session authentication (login required). Use the admin login endpoint first.

## Endpoints

### WhatsApp Webhook

**POST** `/webhook/whatsapp`

Receives incoming WhatsApp messages from Twilio. This is where customer messages arrive.

**Request:** Form data from Twilio
```
From: whatsapp:+1234567890
Body: Customer's message
MessageSid: unique_message_id
NumMedia: number of media attachments
```

**Response:** TwiML response to Twilio
```xml
<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>AI generated response</Message>
</Response>
```

---

### Public API Endpoints

#### Get All Products

**GET** `/api/products`

Returns all active products.

**Query Parameters:**
- `category` (optional): Filter by category

**Response:**
```json
{
  "products": [
    {
      "id": 1,
      "name": "Classic Black Hoodie",
      "price": 49.99,
      "description": "100% cotton...",
      "category": "hoodies",
      "sizes": "XS,S,M,L,XL,XXL",
      "colors": "Black",
      "stock": 50,
      "is_active": true
    }
  ],
  "count": 3
}
```

---

#### Get Single Product

**GET** `/api/products/<product_id>`

**Response:**
```json
{
  "product": {
    "id": 1,
    "name": "Classic Black Hoodie",
    "price": 49.99,
    ...
  }
}
```

---

#### Get Customer Orders

**GET** `/api/customers/<phone>/orders`

Get all orders for a customer by phone number.

**Response:**
```json
{
  "customer": {
    "id": 1,
    "phone_number": "1234567890",
    "name": "John Doe",
    "created_at": "2024-01-15T10:30:00",
    "last_interaction": "2024-01-19T14:22:00",
    "order_count": 3
  },
  "orders": [
    {
      "id": 1,
      "order_number": "ORD-20240119-ABC12345",
      "total_amount": 99.98,
      "status": "confirmed",
      "created_at": "2024-01-19T10:00:00",
      "items": [
        {
          "product_name": "Classic Black Hoodie",
          "quantity": 2,
          "price_at_purchase": 49.99,
          "size": "L",
          "color": "Black",
          "subtotal": 99.98
        }
      ]
    }
  ]
}
```

---

#### Track Order

**GET** `/api/orders/<order_number>/track`

Get detailed tracking information for an order.

**Response:**
```json
{
  "order_number": "ORD-20240119-ABC12345",
  "current_status": "shipped",
  "timeline": [
    {
      "status": "Order Placed",
      "date": "2024-01-19T10:00:00"
    },
    {
      "status": "Confirmed",
      "date": "2024-01-19T11:00:00"
    },
    {
      "status": "Shipped",
      "date": "2024-01-19T14:00:00"
    }
  ]
}
```

---

#### Health Check

**GET** `/api/health`

Check if the system is running.

**Response:**
```json
{
  "status": "healthy",
  "message": "WhatsApp AI System is running"
}
```

---

### Admin Endpoints

All admin endpoints require login. Use `/admin/login` first.

#### Admin Login

**GET/POST** `/admin/login`

**POST Request:**
```
username=admin
password=your_password
```

**Response:** Redirects to `/admin/dashboard`

---

#### Get Dashboard

**GET** `/admin/dashboard`

Get system statistics and overview.

**Response:**
```json
{
  "total_customers": 42,
  "total_orders": 18,
  "pending_orders": 3,
  "orders": [...],
  "customers": [...]
}
```

---

#### Get Orders

**GET** `/admin/orders?status=<status>&limit=<limit>`

Get all orders with optional filtering.

**Query Parameters:**
- `status` (optional): pending, confirmed, shipped, delivered, cancelled
- `limit` (optional): Number of orders to return (default: 50)

**Response:**
```json
{
  "orders": [...],
  "count": 10
}
```

---

#### Update Order Status

**PUT** `/admin/orders/<order_id>/status`

Update the status of an order. Customer will be notified.

**Request Body:**
```json
{
  "status": "confirmed"
}
```

**Valid statuses:** pending, confirmed, shipped, delivered, cancelled

**Response:**
```json
{
  "success": true,
  "order": {
    "id": 1,
    "order_number": "ORD-20240119-ABC12345",
    "status": "confirmed",
    ...
  }
}
```

---

#### Get All Products (Admin)

**GET** `/admin/products`

Get all products including inactive ones.

**Response:**
```json
{
  "products": [...],
  "count": 10
}
```

---

#### Add Product

**POST** `/admin/products`

Create a new product.

**Request Body:**
```json
{
  "name": "Premium Red Hoodie",
  "price": 59.99,
  "description": "Premium cotton blend hoodie",
  "category": "hoodies",
  "sizes": "XS,S,M,L,XL,XXL",
  "colors": "Red,Dark Red",
  "stock": 30,
  "image_url": "https://..."
}
```

**Response:**
```json
{
  "success": true,
  "product": {...}
}
```

---

#### Update Product

**PUT** `/admin/products/<product_id>`

Update product information.

**Request Body:** (any fields to update)
```json
{
  "price": 54.99,
  "stock": 25,
  "is_active": false
}
```

---

#### Delete Product

**DELETE** `/admin/products/<product_id>`

Deactivate a product (soft delete).

---

#### Get Chat Logs

**GET** `/admin/chat-logs?customer_id=<id>&limit=<limit>`

Get chat history.

**Query Parameters:**
- `customer_id` (optional): Filter by specific customer
- `limit` (optional): Number of logs (default: 100)

**Response:**
```json
{
  "logs": [
    {
      "id": 1,
      "customer_id": 1,
      "message_type": "incoming",
      "message_content": "Hi, do you have size L?",
      "ai_generated": false,
      "timestamp": "2024-01-19T14:22:00"
    },
    {
      "id": 2,
      "customer_id": 1,
      "message_type": "outgoing",
      "message_content": "Yes, we have size L available...",
      "ai_generated": true,
      "ai_model_used": "mistral-7b-instruct",
      "confidence_score": 0.87,
      "timestamp": "2024-01-19T14:22:05"
    }
  ],
  "count": 2
}
```

---

#### Get All Customers

**GET** `/admin/customers?limit=<limit>`

Get all customers.

**Query Parameters:**
- `limit` (optional): Number of customers (default: 100)

**Response:**
```json
{
  "customers": [
    {
      "id": 1,
      "phone_number": "1234567890",
      "name": "John Doe",
      "created_at": "2024-01-15T10:30:00",
      "last_interaction": "2024-01-19T14:22:00",
      "order_count": 3
    }
  ],
  "count": 1
}
```

---

### Error Responses

All errors follow this format:

```json
{
  "error": "Description of the error"
}
```

**Common HTTP Status Codes:**
- `200` - Success
- `201` - Created
- `400` - Bad request
- `401` - Not authenticated
- `403` - Not authorized
- `404` - Not found
- `500` - Server error

---

## Example Integration

### JavaScript (Frontend)

```javascript
// Get all products
fetch('http://localhost:5000/api/products')
  .then(r => r.json())
  .then(data => console.log(data.products));

// Track order
fetch('http://localhost:5000/api/orders/ORD-20240119-ABC12345/track')
  .then(r => r.json())
  .then(data => console.log(data));

// Admin: Update order status
fetch('http://localhost:5000/admin/orders/1/status', {
  method: 'PUT',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ status: 'confirmed' })
})
  .then(r => r.json())
  .then(data => console.log(data));
```

### Python

```python
import requests

API_BASE = 'http://localhost:5000'

# Get products
response = requests.get(f'{API_BASE}/api/products')
products = response.json()['products']

# Track order
response = requests.get(f'{API_BASE}/api/orders/ORD-20240119-ABC12345/track')
tracking = response.json()

# Admin: Update status
response = requests.put(
    f'{API_BASE}/admin/orders/1/status',
    json={'status': 'confirmed'}
)
```

### cURL

```bash
# Get products
curl http://localhost:5000/api/products

# Track order
curl http://localhost:5000/api/orders/ORD-20240119-ABC12345/track

# Update order status (with admin session)
curl -X PUT http://localhost:5000/admin/orders/1/status \
  -H "Content-Type: application/json" \
  -d '{"status":"confirmed"}'
```

---

## Rate Limiting

No rate limiting is implemented in the free version. For production, add:

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/api/products')
@limiter.limit("10 per minute")
def get_products():
    ...
```

---

## Webhook Signature Verification

Twilio signs all webhook requests. Verify them:

```python
from twilio.request_validator import RequestValidator

@app.before_request
def verify_twilio_request():
    validator = RequestValidator(auth_token)
    url = request.url
    params = request.form.to_dict()
    request_valid = validator.validate(url, params, request.headers.get('X-Twilio-Signature', ''))
    
    if not request_valid:
        abort(403)
```

---

This API documentation is complete for the free tier system. For advanced features like webhooks, batch operations, and real-time updates, see ADVANCED_FEATURES.md
