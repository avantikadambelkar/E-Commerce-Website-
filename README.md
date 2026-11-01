# ✦ AURA LUXE — Contemporary Luxury E-Commerce & Shopping App

Built with **Python 3.14**, **Django 6.1**, **SQL (Django ORM)**, **HTML5**, **Bootstrap 5.3**, and **Custom Glassmorphism CSS**. Designed specifically with **Indian Rupee (₹ / INR)** pricing, Pan-India courier integration, Indian payment methods (UPI / QR, Cards, Netbanking, COD), and a dedicated **Catalog CRUD Management Dashboard**.

---

## 🌟 Key Features
- **Distinct Aesthetic Design**: Editorial dark glassmorphism, warm gold accents, and Outfit/Plus Jakarta typography (avoiding the cluttered look of Amazon/Flipkart).
- **Shopping App Feel**: Story category bubbles, sticky mobile bottom navigation bar, and instant AJAX bag & wishlist updates.
- **Indian Rupee (₹ / INR)**: All items, variants, GST breakdown (12%), and free shipping progress thresholds calculated in Indian currency.
- **Full CRUD Suite**:
  - Products: Create, Read, Update, Delete in custom manager (`/manage/products/`) & Django admin.
  - Cart: Dynamic quantity steppers, item removal, and promotional coupon codes (`AURA10`, `WELCOME500`).
  - Wishlist: Instant 1-click toggle with toast notifications.
  - Reviews: Submit star ratings and feedback with verified buyer badges.
  - Checkout & Orders: Comprehensive shipping address form with Indian state dropdown and real-time consignment tracker.

---

## 🚀 Quick Start
```bash
# Apply Database Migrations
python manage.py migrate

# Seed Curated Catalog Data with Indian Rupee Prices
python manage.py seed_data

# Run Unit Test Suite
python manage.py test

# Start Development Server
python manage.py runserver 127.0.0.1:8000
```

- **Storefront**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Catalog CRUD Portal**: [http://127.0.0.1:8000/manage/products/](http://127.0.0.1:8000/manage/products/)
- **Django Admin**: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) (User: `admin` | Password: `admin123`)
