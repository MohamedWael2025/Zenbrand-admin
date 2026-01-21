# 📱 WhatsApp Admin - Quick Reference Card

## 🔐 Login
```
Admin login
→ Ma23072007@admin
```

## 📦 Product Commands

| Command | Description | Example |
|---------|-------------|---------|
| `list products` | View all products | `list products` |
| `add product` | Create new product (5-step flow) | `add product` |
| `edit product [name]` | Modify existing product | `edit product Blue Hoodie` |
| `delete product [name]` | Remove product | `delete product Old Style` |
| `admin logout` | End admin session | `admin logout` |

---

## ➕ Add Product Flow

1. **Name:** `Premium Black Hoodie`
2. **Price:** `49.99` (or `$49.99`)
3. **Description:** `Soft cotton hoodie with front pocket`
4. **Stock:** `100`
5. **Category:** `Hoodies`

✅ Done! Product created.

---

## ✏️ Edit Product Options

After `edit product [name]`:
- `edit name` - Change product name
- `edit price` - Update price
- `edit description` - Modify description
- `edit stock` - Update inventory
- `edit image` - Upload photo (coming soon)
- `done` - Finish editing

---

## ❌ Delete Product

```
delete product Old Hoodie
→ yes    (confirm)
→ no     (cancel)
```

---

## 💡 Quick Tips

### ✅ DO
- Use exact product names (case-insensitive)
- Include $ or just numbers for price
- Logout when done: `admin logout`
- Check `list products` after changes

### ❌ DON'T
- Use commas in prices: `1,299.99` ❌ → `1299.99` ✅
- Leave sessions idle (expires in 2 hours)
- Share password in chat
- Forget to confirm deletions

---

## 🆘 Common Issues

| Problem | Solution |
|---------|----------|
| "Unknown command" | Not logged in - send `Admin login` |
| Password fails | Check caps/spaces: `Ma23072007@admin` |
| Product not found | Verify name with `list products` |
| Session expired | Login again after 2 hours |

---

## 🔒 Security

- **Password:** `Ma23072007@admin` (change in `.env`)
- **Session:** 2 hours timeout
- **Failed attempts:** 3 max, then lockout
- **Logout:** Always logout when done

---

## 📊 Example Session

```
You: Admin login
Bot: Enter password:
You: Ma23072007@admin
Bot: ✅ Login successful!

You: list products
Bot: [Shows all products]

You: edit product Classic Hoodie
Bot: What to edit? (name/price/stock/...)

You: edit price
Bot: Enter new price:
You: 59.99
Bot: ✅ Updated! Continue or type 'done'

You: done
Bot: ✅ Editing complete!

You: admin logout
Bot: 👋 Logged out
```

---

## 🚀 Customer Impact

When you make changes, customers see updates **immediately**:

| Your Action | Customer Sees |
|-------------|---------------|
| Add product | Searchable in catalog right away |
| Edit price | New price shown instantly |
| Update stock to 0 | "Out of stock" message |
| Delete product | Removed from search results |

---

## 📝 Notes

- Products are **soft-deleted** (data preserved)
- Changes take effect **immediately**
- All actions are **logged**
- Multiple admins can login **simultaneously**

---

**Need help?** See [Full Admin Guide](./ADMIN_WHATSAPP_GUIDE.md)
