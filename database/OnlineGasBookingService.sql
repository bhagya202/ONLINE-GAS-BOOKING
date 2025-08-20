
-- Create Database
CREATE DATABASE IF NOT EXISTS OnlineGasBookingService;
USE OnlineGasBookingService;

-- 1. Admins Table
CREATE TABLE IF NOT EXISTS Admins (
    admin_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

-- 2. Bookings Table (without foreign keys first)
CREATE TABLE IF NOT EXISTS Bookings (
    booking_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    cylinder_id INT NOT NULL,
    booking_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('Pending', 'Confirmed', 'Delivered', 'Cancelled') DEFAULT 'Pending'
);

-- 3. Gas Cylinders Table
CREATE TABLE IF NOT EXISTS Gas_Cylinders (
    cylinder_id INT AUTO_INCREMENT PRIMARY KEY,
    company_name VARCHAR(100) NOT NULL,
    cylinder_type ENUM('Domestic', 'Commercial') NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    stock INT NOT NULL
);

-- Insert Gas Cylinders
INSERT INTO Gas_Cylinders (company_name, cylinder_type, price, stock) VALUES 
('HP Gas', 'Domestic', 500, 100),
('HP Gas', 'Commercial', 1000, 80),
('Indane Gas', 'Domestic', 480, 120),
('Indane Gas', 'Commercial', 950, 90),
('Bharat Gas', 'Domestic', 470, 110),
('Bharat Gas', 'Commercial', 920, 85);

-- 4. Payments Table (without foreign keys first)
CREATE TABLE IF NOT EXISTS Payments (
    payment_id INT AUTO_INCREMENT PRIMARY KEY,
    booking_id INT NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    payment_method ENUM('Cash', 'Card', 'UPI') NOT NULL,
    payment_status ENUM('Pending', 'Completed', 'Failed') DEFAULT 'Pending',
    payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 5. Settings Table
CREATE TABLE IF NOT EXISTS Settings (
    setting_id INT AUTO_INCREMENT PRIMARY KEY,
    setting_name VARCHAR(100) UNIQUE NOT NULL,
    setting_value VARCHAR(255) NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Insert Default Settings
INSERT INTO Settings (setting_name, setting_value) VALUES
('maintenance_mode', '0'),          
('max_bookings_per_day', '50'),     
('email_notifications', '1'),       
('domestic_price', '900.00'),       
('commercial_price', '1500.00');    

-- 6. Users Table
CREATE TABLE IF NOT EXISTS Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(15) UNIQUE NOT NULL,
    address TEXT NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 🔗 Add Foreign Keys After All Tables Exist
ALTER TABLE Bookings
    ADD CONSTRAINT fk_booking_user FOREIGN KEY (user_id) REFERENCES Users(user_id),
    ADD CONSTRAINT fk_booking_cylinder FOREIGN KEY (cylinder_id) REFERENCES Gas_Cylinders(cylinder_id);

ALTER TABLE Payments
    ADD CONSTRAINT fk_payment_booking FOREIGN KEY (booking_id) REFERENCES Bookings(booking_id);
