# Online Gas Booking 🚀  

An online gas booking management system built with **Flask (Python)** for the backend and **HTML, CSS, JavaScript** for the frontend.  
It provides both **User Panel** and **Admin Panel** with features like cylinder booking, payment, tracking, and inventory management.  

---

## 📂 Project Structure  

    ONLINE_GAS_BOOKING/
    │── flask_session/ # Flask session files
    │── static/ # Static assets (CSS, JS, Images)
    │ ├── CSS/main.css
    │ ├── Js/script.js
    │ └── image/
    │── templates/ # HTML templates
    │ ├── admin.html
    │ ├── admin_customers.html
    │ ├── admin_inventory.html
    │ ├── admin_orders.html
    │ ├── admin_settings.html
    │ ├── adminlogin.html
    │ ├── bookcylinder.html
    │ ├── bookinghistory.html
    │ ├── index.html
    │ ├── login.html
    │ ├── newconnection.html
    │ ├── passwordchange.html
    │ ├── payment.html
    │ ├── payment_history.html
    │ ├── profile.html
    │ ├── profileupdate.html
    │ └── trackbooking.html
    │── app.py # Main Flask application
    │── database.sql # Database schema
    └── OnlineGasBookingService.session.sql



---

## ✨ Features  

### 👤 User Panel  
- User registration & login  
- Book new cylinder online  
- View booking history  
- Track cylinder status  
- Online payment option  
- Update profile & change password  

### 🔑 Admin Panel  
- Secure admin login  
- Manage customers  
- Manage cylinder inventory  
- View and update orders  
- Manage settings  

---

## 🛠️ Tech Stack  

- **Frontend**: HTML5, CSS3, JavaScript  
- **Backend**: Python (Flask)  
- **Database**: MySQL / SQLite  
- **Version Control**: Git & GitHub  

---

## 🚀 Installation & Setup  

1. **Clone the repository**  
   ```
   git clone https://github.com/bhagya202/ONLINE-GAS-BOOKING.git
   cd Online-Gas-Booking
Create Virtual Environment & Install Dependencies

    python -m venv venv
    source venv/bin/activate  # On Linux/Mac
    venv\Scripts\activate     # On Windows
    pip install -r requirements.txt
    Setup Database

Import database.sql into MySQL or use SQLite.

Update database configuration in app.py.

Run Application

    python app.py
    Visit http://127.0.0.1:5000/ in your browser.

💡 Future Improvements
Email & SMS notifications for bookings

Payment gateway integration

Analytics dashboard for Admin

Deploy on cloud (Heroku/AWS/Render)

📜 License
This project is licensed under the MIT License – feel free to use and modify.

👤 Author
Bhagyashree Nikam

GitHub

LinkedIn

---
