# ✦ AURA — Modern Full-Stack E-Commerce Platform

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.0-092E20?logo=django&logoColor=white)](https://www.djangoproject.com/)
[![JavaScript](https://img.shields.io/badge/JavaScript-ES6%2B-F7DF1E?logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-7952B3?logo=bootstrap&logoColor=white)](https://getbootstrap.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A production-grade, full-stack contemporary e-commerce web application built using **Python, Django, and JavaScript**. Designed with a focus on real-world business logic, seamless state persistence for guest & authenticated users, dynamic price/tax engines, and backend database query optimization.

---

## 🌟 Key Features

### 🛒 1. Hybrid Cart & Session Management
- **Guest-to-User State Persistence:** Anonymous visitors can browse and add items to their shopping bag using Django session keys (`request.session.session_key`). Upon registration or login, their items are preserved.
- **Asynchronous AJAX Updates:** Real-time quantity increments/decrements, item removal, and promotional code application without full page reloads.
- **Global Context Processors:** Cart item counts and subtotal summaries are globally accessible across all views and navbar templates without repetitive ORM queries.

### 💰 2. Promotional & Dynamic Pricing Engine
- **Automated Tax Calculation:** Real-time 12% GST computation on checkout subtotal.
- **Tiered Shipping Rules:** Dynamic shipping cost calculation with complimentary shipping for orders exceeding ₹1,499.
- **Coupon Validation Engine:** Supports percentage-based and flat-rate promo codes with minimum cart threshold validation (e.g., `AURA10`, `FESTIVE500`).

### 📦 3. Order Lifecycle & Stock Integrity
- **Atomic Stock Decrement:** Decrements available stock upon order confirmation to prevent overselling.
- **Price Snapshotting:** Captures an immutable record of product prices and variant attributes in `OrderItem` at checkout time, insulating past receipts against future catalog price changes.
- **Unique Tracking Tokens:** Auto-generates unique order numbers (`AURA-XXXX`) and express courier tracking identifiers (`EXP-IN-XXXX`) using UUIDs.
- **Multiple Payment Choices:** Supports Instant UPI/QR, Debit/Credit Card, Net Banking, and Cash on Delivery with Express Handling fees.

### 🔍 4. Catalog, Search & Filtering
- **Multi-Attribute Search:** Fast keyword search across product title, brand, description, and category name powered by Django `Q` objects.
- **Parametric Filtering:** Filter products by category slug, custom price ranges (INR), and in-stock status.
- **Product Variants & Gallery:** Dynamic selection of sizes, colors, and variant-specific price adjustments.

---

## 🏗️ Architecture & Database Design

```
Category (1) ────< Product (N) ────< ProductVariant (N)
                      │
                      ├────< ProductImage (Gallery)
                      ├────< Review (Ratings & Verification)
                      │
Cart (1) ────────< CartItem (N) >──── Product (Snapshot)
                      │
Order (1) ───────< OrderItem (N) >──── Product (Snapshot & Decoupled Price)
```

- **Query Optimization:** Implemented `select_related('category')` across catalog views to eliminate **N+1 query** bottlenecks.
- **Safe Object Handling:** Comprehensive usage of `get_object_or_404` and Django forms with CSRF validation.

---

## 🛠️ Tech Stack

- **Backend:** Python, Django (MVT Architecture), Django ORM
- **Frontend:** HTML5, CSS3, JavaScript (Fetch API / AJAX), Bootstrap 5, Bootstrap Icons
- **Database:** SQLite (Development) / PostgreSQL-ready schema
- **Authentication:** Django Authentication & Session Framework

---

## 🚀 Quickstart & Installation

### 1. Clone the repository
```bash
git clone https://github.com/avantikadambelkar/E-Commerce-Website-.git
cd E-Commerce-Website-
```

### 2. Create and activate a virtual environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install django pillow
```

### 4. Run migrations & start server
```bash
python manage.py migrate
python manage.py runserver
```

Open your browser at `http://127.0.0.1:8000/` to explore the storefront.

---

## 👤 Author

**Avantika Dambelkar**
- LinkedIn: [linkedin.com/in/avantika-dambelkar-6a8024263](https://linkedin.com/in/avantika-dambelkar-6a8024263)
- GitHub: [@avantikadambelkar](https://github.com/avantikadambelkar)
