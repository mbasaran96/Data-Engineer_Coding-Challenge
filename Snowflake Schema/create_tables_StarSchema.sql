-- Tabelle Dim_Customer erstellen.
DROP TABLE IF EXISTS Dim_Customer;
CREATE TABLE Dim_Customer (
Customer_ID INTEGER,
customer_name VARCHAR (60),
customer_email VARCHAR (60),
customer_loyalty_status VARCHAR (15),
PRIMARY KEY (Customer_ID AUTOINCREMENT)
);

-- Tabelle Dim_Product erstellen.
DROP TABLE IF EXISTS Dim_Product;
CREATE TABLE Dim_Product (
Product_ID INTEGER,
Product_name VARCHAR (60),
Product_category VARCHAR (60),
Product_subcategory VARCHAR (60),
Product_brand VARCHAR (60),
Product_department VARCHAR (60),
PRIMARY KEY (Product_ID AUTOINCREMENT)
);

-- Tabelle Dim_Sales Staff erstellen.
DROP TABLE IF EXISTS Dim_Sales Staff;
CREATE TABLE Dim_Sales Staff (
Sales_staff_ID INTEGER,
Sales_staff_name VARCHAR (60),
PRIMARY KEY (Sales_staff_ID AUTOINCREMENT)
);

-- Tabelle Dim_Promotion erstellen.
DROP TABLE IF EXISTS Dim_Promotion;
CREATE TABLE Dim_Promotion (
Promotion_ID INTEGER,
Promotion_name VARCHAR (60),
PRIMARY KEY (Promotion_ID AUTOINCREMENT)
);

-- Tabelle Dim_Store erstellen.
DROP TABLE IF EXISTS Dim_Store;
CREATE TABLE Dim_Store (
Store_ID INTEGER,
District_ID INTEGER,
Store_name VARCHAR (60),
Store_location VARCHAR (60),
Store_type VARCHAR (60),
Store_size_sqm INTEGER,
FOREIGN KEY (District_ID) REFERENCES Dim_District(District_ID),
PRIMARY KEY (Store_ID AUTOINCREMENT)
);

-- Tabelle Dim_Supplier erstellen.
DROP TABLE IF EXISTS Dim_Supplier;
CREATE TABLE Dim_Supplier (
Supplier_ID INTEGER,
Supplier_name VARCHAR (60),
PRIMARY KEY (Supplier_ID AUTOINCREMENT)
);

-- Tabelle Facts_Transaction erstellen.
DROP TABLE IF EXISTS Facts_Transaction;
CREATE TABLE Facts_Transaction (
Transaction_ID INTEGER,
Supplier_ID INTEGER,
Product_ID INTEGER,
Store_ID INTEGER,
Customer_ID INTEGER,
Sales_staff_ID INTEGER,
Promotion_ID INTEGER,
Invoice_number VARCHAR (15),
Transaction_date DATE,
Transaction_time VARCHAR (15),
Transaction_status VARCHAR (15),
quantity DECIMAL (10,2),
unit_price DECIMAL (10,2),
base_price DECIMAL (10,2),
discount_rate DECIMAL (4,2),
discount_applied VARCHAR (15),
total_amount DECIMAL (10,2),
tax_rate DECIMAL (4,2),
tax_amount DECIMAL (10,2),
payment_method VARCHAR (15),
FOREIGN KEY (Supplier_ID) REFERENCES Dim_Supplier(Supplier_ID),
FOREIGN KEY (Product_ID) REFERENCES Dim_Product(Product_ID),
FOREIGN KEY (Store_ID) REFERENCES Dim_Store(Store_ID),
FOREIGN KEY (Customer_ID) REFERENCES Dim_Customer(Customer_ID),
FOREIGN KEY (Sales_staff_ID) REFERENCES Dim_Sales Staff(Sales_staff_ID),
FOREIGN KEY (Promotion_ID) REFERENCES Dim_Promotion(Promotion_ID),
PRIMARY KEY (Transaction_ID AUTOINCREMENT)
);

-- Tabelle Dim_District erstellen.
DROP TABLE IF EXISTS Dim_District;
CREATE TABLE Dim_District (
District_ID INTEGER,
District_name VARCHAR (60),
Postal_code VARCHAR (15),
PRIMARY KEY (District_ID AUTOINCREMENT)
);

