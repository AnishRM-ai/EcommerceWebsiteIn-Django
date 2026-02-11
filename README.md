# Django E-Commerce Website

A full-featured e-commerce platform built with Django, featuring shopping cart functionality, payment processing, and an admin dashboard for managing products and orders.

## What It Does

This e-commerce website provides a complete online shopping experience with both customer-facing and administrative capabilities. Customers can browse products, add items to their cart, and complete purchases through an integrated payment system. Administrators have access to a comprehensive dashboard for managing the entire store.

## Features

### Customer Features

- **User Authentication & Authorization**
  - User registration and login
  - User profile management
  - Session-based authentication

- **Product Browsing**
  - Browse products by categories
  - Product search functionality
  - Detailed product pages with images
  - Product reviews and ratings

- **Shopping Cart**
  - Add/remove items from cart
  - Update product quantities
  - Persistent cart for logged-in users
  - Session-based cart for guest users

- **Checkout & Payment**
  - Secure checkout process
  - Payment gateway integration
  - Order confirmation
  - Order history tracking

### Admin Features

- **Admin Dashboard**
  - Product management (create, read, update, delete)
  - Category management
  - Order processing and tracking
  - User management
  - Sales analytics and reporting

## Tech Stack

- **Backend:** Django (Python)
- **Frontend:** HTML, CSS, JavaScript
- **Database:** SQLite
- **Static Files:** CSS/JS assets

## Project Structure

```
EcommerceWebsiteIn-Django/
├── admin_dashboard/       # Admin panel for managing store
├── cart/                  # Shopping cart functionality
├── ecom/                  # Main project settings
├── payment/               # Payment processing
├── store/                 # Product catalog and storefront
├── static/                # Static files (CSS, JS, images)
├── media/                 # User-uploaded content
├── manage.py              # Django management script
├── requirements.txt       # Python dependencies
└── db.sqlite3            # SQLite database
```

## Installation & Setup

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/AnishRM-ai/EcommerceWebsiteIn-Django.git
   cd EcommerceWebsiteIn-Django
   ```

2. **Create and activate a virtual environment**
   
   On Windows:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```
   
   On macOS/Linux:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply database migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create a superuser (admin account)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Main site: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## How to Use

### As a Customer

1. Browse products on the homepage
2. Add items to your cart
3. Proceed to checkout
4. Complete payment to place order
5. View order history in your account

### As an Administrator

1. Log in to the admin dashboard at `/admin`
2. Add/edit/delete products
3. Manage product categories
4. Process and track orders
5. View sales reports

---

**Note:** This is a personal portfolio project demonstrating full-stack e-commerce development with Django.
