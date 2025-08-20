-- Active: 1739507411076@@127.0.0.1@3306@onlinegasbookingservice
ALTER TABLE bookings ADD CONSTRAINT fk_cylinder FOREIGN KEY (cylinder_id) REFERENCES Gas_Cylinders(cylinder_id) ON DELETE CASCADE ON UPDATE CASCADE;



-- Use the created database

USE online_gas_booking;

SELECT * FROM Gas_Cylinders;
