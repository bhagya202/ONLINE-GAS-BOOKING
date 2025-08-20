# 🏠 online_gas_booking_service

Flask project for online gas booking with user and admin login and booking system  

## 📌 Online Gas Booking Service  
A Flask-based web application for booking and tracking gas cylinders.  
This project provides separate **User** and **Admin** panels with authentication, booking, payment, and tracking features.

---

## ✨ Features

- 🔐 **User Authentication** (Register/Login)  
- 👤 **User Profile Management**  
- 📦 **Book Cylinder** (with unique Cylinder ID & Date)  
- 🔎 **Track Booking** (view status after booking)  
- 💳 **Payment Integration** (simulated)  
- 🛠️ **Admin Panel** for managing bookings and users  
- ⚡ Clean and modern frontend with HTML, CSS, and JavaScript  

---

## 🛠️ Tech Stack

- **Frontend:** HTML, CSS, JavaScript  
- **Backend:** Flask (Python)  
- **Database:** MySQL  
- **Other Tools:** Bootstrap (UI), Flask-Login (Authentication)  

---

## 📂 Project Structure
```
ONLINE_GAS_BOOKING/
│
├── static/
│   ├── CSS/
│   │   └── main.css
│   │
│   ├── image/
│   │
│   └── Js/
│       └── script.js
│
├── templates/
│   ├── admin_customers.html
│   ├── admin_inventory.html
│   ├── admin_orders.html
│   ├── admin_settings.html
│   ├── admin.html
│   ├── adminlogin.html
│   ├── bookcylinder.html
│   ├── bookinghistory.html
│   ├── index.html
│   ├── login.html
│   ├── newconnection.html
│   ├── passwordchange.html
│   ├── payment_history.html
│   ├── payment.html
│   ├── profile.html
│   ├── profileupdate.html
│   ├── register.html
│   └── trackbooking.html
│
├── app.py
└── OnlineGasBookingService.session.sql


--- 

⚙️ Installation & Setup


1. Clone the repository  
  
   git clone https://github.com/bhagya202/online_gas_booking_service.git
   cd online_gas_booking_service
