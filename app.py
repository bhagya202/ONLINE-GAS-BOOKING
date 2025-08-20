import re
import MySQLdb
from flask import Flask, json, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, current_user
from flask_session import Session
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash , check_password_hash

app = Flask(__name__)

# Set the secret key BEFORE initializing sessions
app.secret_key = 'supersecretkey'  # Use a strong key in production

# Configure Flask-Session (for server-side sessions)
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_PERMANENT"] = False
app.config['SESSION_COOKIE_SECURE'] = False  # Development mode over HTTP
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)
Session(app)

# MySQL Configuration  
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Admin1234'
app.config['MYSQL_DB'] = 'OnlineGasBookingService'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = "info"

# User Model
class User(UserMixin):
    def __init__(self, id, username, email, is_admin):
        self.id = str(id)  # Ensure ID is string for Flask-Login
        self.username = username
        self.email = email
        self.is_admin = is_admin
def get_user_by_email(email):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Users WHERE email = %s", (email,))
    user = cur.fetchone()
    cur.close()
    return user

# User Loader
@login_manager.user_loader
def load_user(user_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Users WHERE user_id = %s", (user_id,))
    user = cur.fetchone()
    cur.close()
    if user:
        return User(str(user['user_id']), user['name'], user['email'], user.get('is_admin', 0))
    return None

# Home Route
@app.route('/')
def home():
    return render_template('index.html')

# User Registration Route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        full_name = request.form['fullName']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']
        confirm_password = request.form['confirmPassword']
        

        # Validate email format
        if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash('Invalid email address!', 'danger')
            return redirect(url_for('register'))

        # Check if passwords match
        if password != confirm_password:
            flash('Passwords do not match!', 'danger')
            return redirect(url_for('register'))

       # Hash the password before saving
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)


        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM Users WHERE email = %s", (email,))
        existing_user = cursor.fetchone()


        if existing_user:
            flash('Email already registered! Please login.', 'warning')
            return redirect(url_for('login'))
        
         # Check if phone number already exists
        cursor.execute("SELECT * FROM users WHERE phone = %s", (phone,))
        existing_user = cursor.fetchone()
        
        if existing_user:
            flash("This phone number is already registered. Please use a different one.", "danger")
            return redirect(url_for('register'))

        # Insert new user into database
        cursor.execute("INSERT INTO Users (name, email, phone, password) VALUES (%s, %s, %s, %s)", 
               (full_name, email, phone, hashed_password))  

        mysql.connection.commit()
        cursor.close()

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

# ----------------------------------------
# ROUTE: Login User
# ----------------------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT user_id, name, email, password FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        cur.close()

        if user:
            stored_hash = user['password']  # Use dictionary key, not index
            if check_password_hash(stored_hash, password):  # Compare hashed password
                session['logged_in'] = True
                session['id'] = user['user_id']     # Use dictionary key
                session['name'] = user['name']       # Use dictionary key
                session['email'] = user['email']     # Use dictionary key
                return redirect(url_for('profile'))
            else:
                return 'Invalid password'
        else:
            return 'Invalid email'

    return render_template('login.html')


# Profile Route
@app.route('/profile')
def profile():
    if 'logged_in' in session and session['logged_in']:
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT user_id, name, email, phone FROM users WHERE user_id = %s", (session['id'],))
        user = cur.fetchone()

        # Get last booking details
        cur.execute("""
            SELECT booking_id, cylinder_id, booking_date, status, quantity, delivery_date 
            FROM Bookings 
            WHERE user_id = %s 
            ORDER BY booking_date DESC LIMIT 1
        """, (session['id'],))
        last_booking = cur.fetchone()

        payment_status = None
        payment_method = None

        if last_booking:
            cur.execute("SELECT payment_status, payment_method FROM Payments WHERE booking_id = %s", (last_booking['booking_id'],))
            payment = cur.fetchone()
            if payment:
                payment_status = payment['payment_status']
                payment_method = payment['payment_method']

        cur.close()

        return render_template(
        'profile.html', 
        user=user, 
        last_booking=last_booking if last_booking else {},  # Ensure last_booking is always a dictionary
        payment_status=payment_status, 
        payment_method=payment_method
    )

    else:
        return redirect(url_for('login'))



@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

from flask import Flask, render_template, request, redirect, url_for, session
import MySQLdb

# ... (other imports and app configuration)

@app.route('/bookinghistory')
def booking_history():
    if 'logged_in' in session:
        user_id = session['id']  # Use session to get user ID

        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("""
            SELECT b.booking_id, b.booking_date, b.status, g.company_name
            FROM Bookings b
            JOIN Gas_Cylinders g ON b.cylinder_id = g.cylinder_id
            WHERE b.user_id = %s
            ORDER BY b.booking_date DESC
        """, (user_id,))
        bookings = cur.fetchall()
        cur.close()

        return render_template('bookinghistory.html', bookings=bookings)
    else:
        return redirect(url_for('login'))

# Book Cylinder Route
@app.route('/bookcylinder', methods=['GET', 'POST'])
def bookcylinder():
    if request.method == 'POST':
        if 'logged_in' in session and session['logged_in']:
            try:
                user_id = session['id']
                

                # Get form data safely
                gas_company = request.form.get('gas_company', '').strip()
                cylinder_type = request.form.get('cylinder_type', '').strip()
                quantity = request.form.get('quantity', '1').strip()
                delivery_date = request.form.get('delivery_date', '').strip()
                address = request.form.get('address', '').strip()

                if not gas_company or not cylinder_type or not quantity or not delivery_date or not address:
                    flash('❗ Please fill in all fields before submitting.', 'danger')
                    return redirect(url_for('bookcylinder'))

                try:
                    quantity = int(quantity)
                except ValueError:
                    flash('❗ Invalid quantity. Please enter a valid number.', 'danger')
                    return redirect(url_for('bookcylinder'))

                booking_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                status = 'Pending'

                cur = mysql.connection.cursor()

                # Debugging: Print input values before querying
                print(f"Checking for: Gas Company: {gas_company}, Cylinder Type: {cylinder_type}")

                # Fetch cylinder_id properly
                cur.execute("""
                        SELECT cylinder_id FROM Gas_Cylinders 
                        WHERE company_name = %s AND cylinder_type = %s
                        """, (gas_company, cylinder_type))

                cylinder = cur.fetchone()

                if not cylinder:
                    flash('❗ Selected gas company and cylinder type not found. Please check your inputs.', 'danger')
                    return redirect(url_for('bookcylinder'))

                cylinder_id = cylinder['cylinder_id']


                # Insert booking into database
                cur.execute("""
                    INSERT INTO Bookings (user_id, cylinder_id, booking_date, status, quantity, delivery_date, address)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (user_id, cylinder_id, booking_date, status, quantity, delivery_date , address))
                mysql.connection.commit()

                booking_id = cur.lastrowid  # Get the last inserted booking ID

                # Store last booking in session
                session['last_booking'] = {
                    'booking_id': booking_id,
                    'cylinder_id': cylinder_id,
                    'booking_date': booking_date,
                    'status': status,
                    'quantity': quantity,
                    'delivery_date': delivery_date,
                    'address': address
                }

                cur.close()

                flash('✅ Your gas cylinder has been booked successfully!', 'success')
                return redirect(url_for('profile'))

            except Exception as e:
                import traceback
                traceback.print_exc()
                flash(f'❗ Error while booking: {repr(e)}', 'danger')
                return redirect(url_for('bookcylinder'))
        else:
            flash('⚠️ Please log in to book a cylinder.', 'warning')
            return redirect(url_for('login'))

    return render_template('bookcylinder.html')

@app.route('/payment/<int:booking_id>', methods=['GET', 'POST'])
def payment(booking_id):
    if 'logged_in' in session and session['logged_in']:
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        # Fetch booking details
        cur.execute("SELECT * FROM Bookings WHERE booking_id = %s", (booking_id,))
        booking = cur.fetchone()

        if not booking:
            flash('Booking not found.', 'danger')
            cur.close()
            return redirect(url_for('profile'))

        # Debugging - Check what booking contains
        print("Booking Data:", booking)

        amount = booking.get('amount', 900.00)  # Fetch amount dynamically, default to 900.00

        if request.method == 'POST':
            if 'payment_method' not in request.form or not request.form['payment_method']:
                flash('Please select a payment method.', 'danger')
                return redirect(url_for('payment', booking_id=booking_id))

            payment_method = request.form['payment_method']
            payment_status = 'Completed' if payment_method != 'cash' else 'Pending'

            # Additional payment details
            payment_details = {}
            if payment_method == 'card':
                payment_details['card_number'] = request.form.get('card_number', '')
                payment_details['card_holder'] = request.form.get('card_holder', '')
                payment_details['expiry'] = request.form.get('expiry', '')
                payment_details['cvv'] = request.form.get('cvv', '')
            elif payment_method == 'upi':
                payment_details['upi_id'] = request.form.get('upi_id', '')

            # Check if payment already exists
            cur.execute("SELECT * FROM Payments WHERE booking_id = %s", (booking_id,))
            existing_payment = cur.fetchone()

            print("Existing Payment:", existing_payment)  # Debugging

            if existing_payment:
                cur.execute("""
                    UPDATE Payments 
                    SET payment_method = %s, payment_status = %s, payment_details = %s 
                    WHERE booking_id = %s
                """, (payment_method, payment_status, json.dumps(payment_details), booking_id))
            else:
                cur.execute("""
                    INSERT INTO Payments (booking_id, amount, payment_method, payment_status, payment_details)
                    VALUES (%s, %s, %s, %s, %s)
                """, (booking_id, amount, payment_method, payment_status, json.dumps(payment_details)))

            mysql.connection.commit()
            cur.close()

            flash('Payment successful!' if payment_status == 'Completed' else 'Payment Pending (Cash on Delivery)', 'success')
            return redirect(url_for('profile'))

        cur.close()
        return render_template('payment.html', booking_id=booking_id, amount=amount)

    else:
        flash('Please log in to continue.', 'warning')
        return redirect(url_for('login'))
    
  # Payment History Route
@app.route('/payment_history')
def payment_history():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT p.payment_id, p.booking_id, p.amount, p.payment_method, p.payment_date 
        FROM Payments p 
        JOIN Bookings b ON p.booking_id = b.booking_id 
        WHERE b.user_id = %s 
        ORDER BY p.payment_date DESC
    """, (session['id'],))
    payments = cur.fetchall()
    cur.close()
    return render_template('payment_history.html', payments=payments)

@app.route('/admin')
def admin_dashboard():
    if 'admin_logged_in' not in session:
        return redirect(url_for('admin_login'))

    cur = mysql.connection.cursor()
    cur.execute("SELECT COUNT(*) as total_users FROM users")
    total_users = cur.fetchone()['total_users']
    
    cur.execute("SELECT COUNT(*) as total_bookings FROM Bookings")
    total_bookings = cur.fetchone()['total_bookings']
    
    cur.execute("SELECT COUNT(*) as pending_bookings FROM Bookings WHERE status = 'Pending'")
    pending_bookings = cur.fetchone()['pending_bookings']
    
    cur.execute("SELECT SUM(stock) as total_stock FROM Gas_Cylinders")
    total_stock = cur.fetchone()['total_stock'] or 0
    
    cur.execute("""
        SELECT b.booking_id, u.name AS customer_name, g.company_name, g.cylinder_type, 
               b.booking_date, b.status
        FROM Bookings b
        JOIN Users u ON b.user_id = u.user_id
        JOIN Gas_Cylinders g ON b.cylinder_id = g.cylinder_id
        ORDER BY b.booking_date DESC
        LIMIT 5
    """)
    recent_bookings = cur.fetchall()
    
    cur.close()
    return render_template('admin.html', 
                         total_users=total_users,
                         total_bookings=total_bookings,
                         pending_bookings=pending_bookings,
                         total_stock=total_stock,
                         recent_bookings=recent_bookings)
    
    # Orders Route
@app.route('/admin/orders')
def admin_orders():
    if 'admin_logged_in' not in session:
        return redirect(url_for('admin_login'))
    
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT b.booking_id, u.name AS customer_name, g.company_name, g.cylinder_type, 
               b.booking_date, b.status
        FROM Bookings b
        JOIN Users u ON b.user_id = u.user_id
        JOIN Gas_Cylinders g ON b.cylinder_id = g.cylinder_id
        ORDER BY b.booking_date DESC
    """)
    orders = cur.fetchall()
    cur.close()
    return render_template('admin_orders.html', orders=orders)

# Customers Route
@app.route('/admin/customers')
def admin_customers():
    if 'admin_logged_in' not in session:
        return redirect(url_for('admin_login'))
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT user_id, name, email, phone FROM users")
    customers = cur.fetchall()
    cur.close()
    return render_template('admin_customers.html', customers=customers)

# Inventory Route
@app.route('/admin/inventory')
def admin_inventory():
    if 'admin_logged_in' not in session:
        return redirect(url_for('admin_login'))
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT cylinder_id, company_name, cylinder_type, price, stock FROM Gas_Cylinders")
    inventory = cur.fetchall()
    cur.close()
    return render_template('admin_inventory.html', inventory=inventory)

# Settings Route
@app.route('/admin/settings', methods=['GET', 'POST'])
def admin_settings():
    if 'admin_logged_in' not in session:
        return redirect(url_for('admin_login'))

    cur = mysql.connection.cursor()

    if request.method == 'POST':
        maintenance_mode = '1' if request.form.get('maintenance_mode') else '0'
        max_bookings = request.form.get('max_bookings', '50')
        email_notifications = '1' if request.form.get('email_notifications') else '0'
        domestic_price = request.form.get('domestic_price', '900.00')
        commercial_price = request.form.get('commercial_price', '1500.00')

        # Update settings in the database
        cur.execute("INSERT INTO Settings (setting_name, setting_value) VALUES (%s, %s) ON DUPLICATE KEY UPDATE setting_value = %s", 
                    ('maintenance_mode', maintenance_mode, maintenance_mode))
        cur.execute("INSERT INTO Settings (setting_name, setting_value) VALUES (%s, %s) ON DUPLICATE KEY UPDATE setting_value = %s", 
                    ('max_bookings_per_day', max_bookings, max_bookings))
        cur.execute("INSERT INTO Settings (setting_name, setting_value) VALUES (%s, %s) ON DUPLICATE KEY UPDATE setting_value = %s", 
                    ('email_notifications', email_notifications, email_notifications))
        cur.execute("INSERT INTO Settings (setting_name, setting_value) VALUES (%s, %s) ON DUPLICATE KEY UPDATE setting_value = %s", 
                    ('domestic_price', domestic_price, domestic_price))
        cur.execute("INSERT INTO Settings (setting_name, setting_value) VALUES (%s, %s) ON DUPLICATE KEY UPDATE setting_value = %s", 
                    ('commercial_price', commercial_price, commercial_price))
        
        mysql.connection.commit()
        flash('Settings updated successfully!', 'success')

    # Fetch current settings
    cur.execute("SELECT setting_name, setting_value FROM Settings")
    settings = {row['setting_name']: row['setting_value'] for row in cur.fetchall()}
    cur.close()

    return render_template('admin_settings.html', settings=settings)

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == "admin" and password == "admin123":
            session['admin_logged_in'] = True
            flash('Admin logged in successfully!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            return render_template('adminlogin.html', error="Invalid credentials")
    return render_template('adminlogin.html')


@app.route('/adminlogout')
def admin_logout():
    session.pop('admin_logged_in', None)
    session.pop('admin_username', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))
    
    
@app.route('/newconnection')
def new_connection():
    return render_template('newconnection.html')

# Password Change Route
@app.route('/passwordchange', methods=['GET', 'POST'])
def password_change():
    if 'logged_in' in session and session['logged_in']:
        if request.method == 'POST':
            # Debugging line
            print(request.form)  # Print form data to check if it's received

            # Fetch form data
            current_password = request.form.get('current_password')
            new_password = request.form.get('new_password')
            confirm_password = request.form.get('confirm_password')

            if not current_password or not new_password or not confirm_password:
                flash('All fields are required.', 'danger')
                return redirect(url_for('password_change'))

            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute("SELECT password FROM users WHERE user_id = %s", (session['id'],))
            user = cur.fetchone()

            if user and check_password_hash(user['password'], current_password):
                if new_password == confirm_password:
                    hashed_password = generate_password_hash(new_password)

                    cur.execute("UPDATE users SET password = %s WHERE user_id = %s",
                                (hashed_password, session['id']))
                    mysql.connection.commit()
                    cur.close()

                    flash('Password changed successfully!', 'success')
                    return redirect(url_for('profile'))
                else:
                    flash('New password and confirm password do not match.', 'danger')
            else:
                flash('Current password is incorrect.', 'danger')

        return render_template('passwordchange.html')
    else:
        flash('Please log in first.', 'warning')
        return redirect(url_for('login'))


@app.route('/profileupdate', methods=['GET', 'POST'])
def profile_update():
    if 'logged_in' in session and session['logged_in']:
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        if request.method == 'POST':
            new_name = request.form['name']
            new_email = request.form['email']

            # Check if email is already in use
            cur.execute("SELECT user_id FROM users WHERE email = %s AND user_id != %s",
                        (new_email, session['id']))
            existing_email = cur.fetchone()

            if existing_email:
                flash('Email already exists. Try another.', 'danger')
            else:
                cur.execute("UPDATE users SET name = %s, email = %s WHERE user_id = %s",
                            (new_name, new_email, session['id']))
                mysql.connection.commit()
                flash('Profile updated successfully!', 'success')
                cur.close()
                return redirect(url_for('profile'))  # ✅ redirect to profile page after success

        # For GET method or if email exists
        cur.execute("SELECT name, email FROM users WHERE user_id = %s", (session['id'],))
        user = cur.fetchone()
        cur.close()
        return render_template('profileupdate.html', user=user)

    else:
        flash('Please log in first.', 'warning')
        return redirect(url_for('login'))



# Track Booking Route
@app.route('/trackbooking', methods=['GET'])
def track_booking():
    if 'logged_in' in session and session['logged_in']:
        booking_id = request.args.get('booking_id')  # Get booking ID from query params

        if not booking_id:
            flash("⚠️ Please enter a valid Booking ID.", "warning")
            return render_template('trackbooking.html', tracking=False)

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Bookings WHERE booking_id = %s", (booking_id,))
        booking = cur.fetchone()
        cur.close()

        if not booking:
            flash("❗ No booking found for the entered ID.", "danger")
            return render_template('trackbooking.html', tracking=False)

        # Example status (Replace with actual DB status if available)
        delivery_status = "Out for Delivery"
        estimated_time = "6th January 2025, 4:00 PM"
        current_location = "Near ABC Street, Mumbai"

        return render_template(
            'trackbooking.html',
            tracking=True,
            booking_id=booking_id,
            status=delivery_status,
            estimated_time=estimated_time,
            current_location=current_location
        )
    else:
        flash("⚠️ Please log in to continue.", "warning")
        return redirect(url_for('login'))



# Debug Session Route
@app.route('/debug-session')
def debug_session():
    print("DEBUG: Flask Session Data:", session)
    print("DEBUG: current_user.is_authenticated =", current_user.is_authenticated)
    print("DEBUG: current_user.get_id() =", current_user.get_id() if current_user.is_authenticated else None)
    return str(session)

# Test Route to Verify Login Persistence
@app.route('/test')
def test():
    return "Logged in as " + current_user.get_id()

if __name__ == '__main__':
    app.run(debug=True)
