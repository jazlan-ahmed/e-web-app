# 🛒 Django E-Commerce Website

A simple and customizable e-commerce website built with Django. This project provides the core features of an online store, including product listings, shopping cart, user authentication, and order management.

---

![E-Commerce Web Preview](static/ecom_web.png)

---
## 📦 Features

- User Registration, Login, Logout
- Product Listing & Detail Pages
- Add to Cart / Remove from Cart
- Order Summary
- Checkout Process
- Address Management
- Admin Panel for Product & Order Management

---

## 🚀 Getting Started

### Prerequisites

Make sure you have the following installed:

- Python 3.8+
- pip
- virtual environment (optional but recommended)
- PostgreSQL (as per your config)

### Installation

**1. Clone the repository**

```bash
git clone https://github.com/MohamedAadil18/e-com-web.git
cd e-com-web
```
**2.Create virtual environment and activate**
```bash
python -m venv ven
source ven/Scripts/activate # windows
source env/bin/activate # MacOS
```
**3.Install dependencies**
```bash
pip install -r requirements.txt
```
**4.Configure database**
##### Connect to the database in settings.py by entering database credentials
```bash
python manage.py makemigrations
python manage.py migrate
```
**5.Create a superuser (admin)**
```bash
python manage.py createsuperuser
```
#### go to http://127.0.0.1:8000/admin/ to manage admin panel

**7.Run the server**
```bash
python manage.py runserver
```

**Tech Stack**
- Backend: Django, Python

- Frontend: HTML, CSS, JavaScript

- Database: PostgreSQL

- Authentication: Django Auth
  
- Admin Panel: Django Admin