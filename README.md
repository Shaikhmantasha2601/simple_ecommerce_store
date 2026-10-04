# Simple E-commerce Store

A complete beginner-friendly e-commerce website built according to the task requirements:

- Frontend: HTML, CSS, JavaScript
- Backend: Django (Python)
- Database: SQLite
- Product listings
- Product details page
- Shopping cart
- User registration/login/logout
- Order processing
- Database storage for products, users and orders
- Django admin panel

## 1. Create a virtual environment

### Windows CMD

```cmd
python -m venv venv
venv\Scripts\activate
```

### PowerShell

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

## 2. Install dependencies

```cmd
pip install -r requirements.txt
```

## 3. Create database tables

```cmd
python manage.py migrate
```

## 4. Add sample products

```cmd
python manage.py seed_products
```

## 5. Create an admin account

```cmd
python manage.py createsuperuser
```

Follow the prompts.

## 6. Start the website

```cmd
python manage.py runserver
```

Open:

http://127.0.0.1:8000/

Admin:

http://127.0.0.1:8000/admin/

## Main features

### Home / Product Listing
Shows all products with category, price, stock and an Add to Cart button.

### Product Details
Open a product to see a larger product view, description, price, stock and quantity selector.

### Shopping Cart
Cart is stored in the user's Django session. Users can update quantities, remove items and see totals.

### Authentication
Users can register, log in and log out.

### Order Processing
Logged-in users can enter a shipping address, review their cart and place an order. Orders and order items are stored in SQLite.

### Admin
Django admin lets you add/edit/delete products and inspect users, orders and order items.

## Project structure

```text
simple_ecommerce_store/
├── manage.py
├── requirements.txt
├── README.md
├── store_project/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── shop/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   └── management/
│       └── commands/
│           └── seed_products.py
├── templates/
│   ├── base.html
│   ├── shop/
│   │   ├── home.html
│   │   ├── product_detail.html
│   │   ├── cart.html
│   │   ├── checkout.html
│   │   ├── order_success.html
│   │   └── my_orders.html
│   └── registration/
│       ├── login.html
│       └── register.html
└── static/
    ├── css/style.css
    └── js/main.js
```
