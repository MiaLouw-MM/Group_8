create TABLE PRODUCTS(
product_id INTEGER PRIMARY KEY AUTOINCREMENT,
product_name VARCHAR(40) NOT NULL,
product_category VARCHAR(30) NOT NULL,
price DECIMAL(10, 2) NOT NULL,
stock_quantity INTEGER NOT NULL);

Insert into PRODUCTS VALUES (1, 'MShampoo', 'Shampoo', '200.00', 100);
Insert into PRODUCTS VALUES 
(2, 'smartyConditioner', 'Conditioner', '200.00', 100),
(3, 'M011TGel', 'Styling', '100.00', 150),
(4, 'HSerum', 'Treatment', '200.00', 80),
(5,'fabHairBrush', 'Equipment', '50.00', 50),
(6,'LAORIVHairMask', 'Treatment', '80.00', 60);

SELECT * FROM PRODUCTS; 

create TABLE VENDORS(
vendor_id INTEGER PRIMARY KEY AUTOINCREMENT,
vendor_name VARCHAR(100) NOT NULL,
contact_name VARCHAR(100),
contact_email VARCHAR(100) UNIQUE NOT NULL,
phone_number VARCHAR(15),
address TEXT,
created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO VENDORS (vendor_name, contact_name, contact_email, phone_number, address)
VALUES
('HairPro Supplies', 'Lerato Mokoena', 'lerato.m@hairpro.co.za', '+27 82 456 7890', '15 Strand Street, Cape Town, 8001'),
('Salon Essentials', 'Peter Naidoo', 'peter.n@salonessentials.co.za', '+27 83 345 2222', '101 Rivonia Road, Sandton, 2196'),
('Glow Beauty Distributors', 'Amy Jacobs', 'amy.j@glowbeauty.co.za', '+27 82 999 1212', '45 Florida Road, Durban, 4001'),
('ProStyle Products', 'Thabo Molefe', 'thabo.m@prostyle.co.za', '+27 84 321 6543', '89 Church Street, Pretoria, 0083'),
('Chic Hair & Spa Supplies', 'Natasha Daniels', 'natasha.d@chicsupplies.co.za', '+27 81 234 7788', '23 Main Road, Stellenbosch, 7600'),
('Urban Salon Goods', 'Jason Khumalo', 'jason.k@urbansalon.co.za', '+27 73 556 9821', '62 Glenwood Drive, Bloemfontein, 9301'),
('Elite Cosmetics SA', 'Fatima Essop', 'fatima.e@elitecosmetics.co.za', '+27 84 777 4432', '8 Longmarket Street, Cape Town, 8000'),
('TressCare Distribution', 'Sipho Dlamini', 'sipho.d@tresscare.co.za', '+27 82 880 2233', '120 Helen Joseph Ave, Johannesburg, 2000');

SELECT * FROM VENDORS;

CREATE TABLE purchase_orders (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    vendor_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    order_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    total_amount DECIMAL(10, 2) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (vendor_id) REFERENCES VENDORS(vendor_id),
    FOREIGN KEY (product_id) REFERENCES PRODUCTS(product_id)
);

INSERT INTO purchase_orders (vendor_id, product_id, quantity, total_amount, status)
VALUES
(1, 1, 50, 50 * 200.00, 'pending'),     
(2, 2, 40, 40 * 200.00, 'completed'),   
(3, 3, 100, 100 * 100.00, 'pending'),   
(4, 4, 30, 30 * 200.00, 'completed'),  
(5, 5, 20, 20 * 50.00, 'pending'),      
(6, 6, 25, 25 * 80.00, 'pending'),      
(7, 1, 60, 60 * 200.00, 'completed'),   
(8, 4, 15, 15 * 200.00, 'pending');

create TABLE services(
service_id INTEGER PRIMARY KEY AUTOINCREMENT,
service_name VARCHAR(40) NOT NULL,
service_category VARCHAR(30) NOT NULL,
price DECIMAL(10, 2) NOT NULL,
service_duration_min DECIMAL(10, 2) NOT NULL);

Insert into services  VALUES 
(1, 'WomanTrim', 'Cuts', '300.0', 60.0),
(2, 'WomanCut', 'Cuts', '500.00', 60.0),
(3, 'MenCut', 'Cuts', '400.00', 30.0),
(4, 'Balayage', 'Colours', '1100.00', 120.00),
(5, 'Highlights', 'Colours', '1000.00', 90.00),
(6, 'Semi-permanent colour', 'Colours', '600.00', 90.00),
(7, 'Toner', 'Colours', '800.00', '90.00'),
(8, 'Lowlights','Colours', '1000.00', 90.00),
(9, 'Permanent colour','Colours', '1100.00', 90.00 );

create TABLE goods_issued(
goods_issued_id INTEGER PRIMARY KEY AUTOINCREMENT,
product_id INTEGER NOT NULL,
quantity_issued INTEGER NOT NULL,
issued_to VARCHAR(100) NOT NULL,
issue_date DATETIME DEFAULT CURRENT_TIMESTAMP,
FOREIGN KEY (product_id) REFERENCES PRODUCTS(product_id)
);

INSERT INTO goods_issued (product_id, quantity_issued, issued_to, issue_date)
VALUES
(1, 5, 'Lerato Mokoena', '2025-10-18 10:15:00'),
(2, 3, 'Thabo Molefe', '2025-10-18 11:00:00'),
(3, 10, 'Amy Jacobs', '2025-10-19 09:45:00'),
(4, 2, 'Natasha Daniels', '2025-10-19 13:30:00'),
(5, 8, 'Jason Khumalo', '2025-10-20 14:00:00'),
(6, 4, 'Fatima Essop', '2025-10-20 15:45:00'),
(7, 6, 'Sipho Dlamini', '2025-10-21 10:20:00'),
(8, 3, 'Peter Naidoo', '2025-10-21 12:10:00'),
(1, 7, 'Lerato Mokoena', '2025-10-22 09:00:00'),
(5, 5, 'Natasha Daniels', '2025-10-22 16:40:00');

create table customer(
name varchar(100) NOT NULL,
surname varchar(100) NOT NULL,
email varchar(150) UNIQUE NOT NULL,
phone_number varchar(20) NOT NULL,
loyalty_points INTEGER DEFAULT 0,
created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
updated_at DATETIME DEFAULT CURRENT_TIMESTAMP);

INSERT INTO customer (name, surname, email, phone_number, loyalty_points)
VALUES 
('Alice', 'Johnson', 'alice.johnson@example.com', '555-1234', 120),
('Bob', 'Smith', 'bob.smith@example.com', '555-5678', 50),
('Carol', 'Williams', 'carol.williams@example.com', '555-9012', 200);


CREATE TABLE hairdressor (
    hairdressor_id INTEGER PRIMARY KEY AUTOINCREMENT,
    hairdressor_name VARCHAR(100) NOT NULL,
    hairdressor_surname VARCHAR(100) NOT NULL,
    hairdressor_phone VARCHAR(15),
    hairdressor_email VARCHAR(100),
    password VARCHAR(100) NOT NULL
);



INSERT INTO hairdressor (hairdressor_name, hairdressor_surname, hairdressor_phone, hairdressor_email, password)
VALUES 
('Caty', 'Brown', '0798888888', "catyBrown@hairdressor.com", 'password1'),
('Jake', 'White', '0797777777', "jakeWhite@hairdressor.com", 'password2'),
('Stacey', 'Green', '0796666666', "staceygreen@hairdressor.com", 'password3'),
('Josh', 'King', '0795555555', "joshB@hairdressor.com", 'password4');

CREATE TABLE Bookings (
    booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
    service_id INTEGER NOT NULL,
    hairdressor_id INTEGER NOT NULL,
    customer_id INTEGER NOT NULL,
    booking_date DATETIME NOT NULL,
    status VARCHAR(20) DEFAULT 'scheduled',
    FOREIGN KEY (service_id) REFERENCES services(service_id),
    FOREIGN KEY (hairdressor_id) REFERENCES hairdressor(hairdressor_id),
    FOREIGN KEY (customer_id) REFERENCES customer(customer_id)
);






DELETE FROM Bookings;
DROP TABLE Bookings;

PRAGMA foreign_keys=ON;

CREATE TABLE IF NOT EXISTS bookings (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  customer_email TEXT,
  service_id INTEGER NOT NULL,
  stylist_id INTEGER NOT NULL,
  start_datetime TEXT NOT NULL,    -- "YYYY-MM-DD HH:MM:SS"
  duration_min INTEGER NOT NULL,
  end_datetime TEXT,               -- computed
  status TEXT DEFAULT 'confirmed',
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY(service_id) REFERENCES services(service_id)
);

CREATE TRIGGER IF NOT EXISTS trg_bookings_after_insert
AFTER INSERT ON bookings
FOR EACH ROW
BEGIN
  UPDATE bookings
  SET end_datetime = datetime(NEW.start_datetime, '+' || NEW.duration_min || ' minutes')
  WHERE id = NEW.id;
END;





