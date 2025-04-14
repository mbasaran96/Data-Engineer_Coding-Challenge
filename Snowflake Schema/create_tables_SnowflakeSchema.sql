-- Tabelle Dim_Customer erstellen.
DROP TABLE IF EXISTS Dim_Customer;
CREATE TABLE Dim_Customer (
Customer_ID INTEGER,
Customer_loyalty_status_ID INTEGER,
Customer_name VARCHAR (60),
Customer_email VARCHAR (60),
Date_from DATE,
Date_to DATE,
FOREIGN KEY (Customer_loyalty_status_ID) REFERENCES Dim_Customer_loyalty_status(Customer_loyalty_status_ID),
PRIMARY KEY (Customer_ID AUTOINCREMENT)
);

-- Tabelle Dim_Product erstellen.
DROP TABLE IF EXISTS Dim_Product;
CREATE TABLE Dim_Product (
Product_ID INTEGER,
Product_category_ID INTEGER,
Product_subcategory_ID INTEGER,
Product_brand_ID INTEGER,
Product_department_ID INTEGER,
Product_name VARCHAR (60),
Date_from DATE,
Date_to DATE,
FOREIGN KEY (Product_category_ID) REFERENCES Dim_Product_category(Product_category_ID),
FOREIGN KEY (Product_subcategory_ID) REFERENCES Dim_Product_subcategory(Product_subcategory_ID),
FOREIGN KEY (Product_brand_ID) REFERENCES Dim_Product_brand(Product_brand_ID),
FOREIGN KEY (Product_department_ID) REFERENCES Dim_Product_department(Product_department_ID),
PRIMARY KEY (Product_ID AUTOINCREMENT)
);

-- Tabelle Dim_Sales_staff erstellen.
DROP TABLE IF EXISTS Dim_Sales_staff;
CREATE TABLE Dim_Sales_staff (
Sales_staff_ID INTEGER,
Sales_staff_name VARCHAR (60),
Date_from DATE,
Date_to DATE,
PRIMARY KEY (Sales_staff_ID AUTOINCREMENT)
);

-- Tabelle Dim_Promotion erstellen.
DROP TABLE IF EXISTS Dim_Promotion;
CREATE TABLE Dim_Promotion (
Promotion_ID INTEGER,
Promotion_name VARCHAR (60),
Date_from DATE,
Date_to DATE,
PRIMARY KEY (Promotion_ID AUTOINCREMENT)
);

-- Tabelle Dim_Store erstellen.
DROP TABLE IF EXISTS Dim_Store;
CREATE TABLE Dim_Store (
Store_ID INTEGER,
District_ID INTEGER,
Store_location_ID INTEGER,
Store_type_ID INTEGER,
Store_name VARCHAR (60),
Store_size_sqm INTEGER,
Date_from DATE,
Date_to DATE,
FOREIGN KEY (District_ID) REFERENCES Dim_District(District_ID),
FOREIGN KEY (Store_location_ID) REFERENCES Dim_Store_location(Store_location_ID),
FOREIGN KEY (Store_type_ID) REFERENCES Dim_Store_type(Store_type_ID),
PRIMARY KEY (Store_ID AUTOINCREMENT)
);

-- Tabelle Dim_Supplier erstellen.
DROP TABLE IF EXISTS Dim_Supplier;
CREATE TABLE Dim_Supplier (
Supplier_ID INTEGER,
Supplier_name VARCHAR (60),
Date_from DATE,
Date_to DATE,
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
Payment_method_ID INTEGER,
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
FOREIGN KEY (Supplier_ID) REFERENCES Dim_Supplier(Supplier_ID),
FOREIGN KEY (Product_ID) REFERENCES Dim_Product(Product_ID),
FOREIGN KEY (Store_ID) REFERENCES Dim_Store(Store_ID),
FOREIGN KEY (Customer_ID) REFERENCES Dim_Customer(Customer_ID),
FOREIGN KEY (Sales_staff_ID) REFERENCES Dim_Sales_staff(Sales_staff_ID),
FOREIGN KEY (Promotion_ID) REFERENCES Dim_Promotion(Promotion_ID),
FOREIGN KEY (Payment_method_ID) REFERENCES Dim_Payment_method(Payment_method_ID),
PRIMARY KEY (Transaction_ID AUTOINCREMENT)
);

-- Tabelle Dim_District erstellen.
DROP TABLE IF EXISTS Dim_District;
CREATE TABLE Dim_District (
District_ID INTEGER,
District_name VARCHAR (60),
Postal_code VARCHAR (15),
Date_from DATE,
Date_to DATE,
PRIMARY KEY (District_ID AUTOINCREMENT)
);

-- Tabelle Dim_Product_category erstellen.
DROP TABLE IF EXISTS Dim_Product_category;
CREATE TABLE Dim_Product_category (
Product_category_ID INTEGER,
Product_category_name VARCHAR (60),
Date_from DATE,
Date_to DATE,
PRIMARY KEY (Product_category_ID AUTOINCREMENT)
);

-- Tabelle Dim_Product_subcategory erstellen.
DROP TABLE IF EXISTS Dim_Product_subcategory;
CREATE TABLE Dim_Product_subcategory (
Product_subcategory_ID INTEGER,
Product_subcategory_name VARCHAR (60),
Date_from DATE,
Date_to DATE,
PRIMARY KEY (Product_subcategory_ID AUTOINCREMENT)
);

-- Tabelle Dim_Product_brand erstellen.
DROP TABLE IF EXISTS Dim_Product_brand;
CREATE TABLE Dim_Product_brand (
Product_brand_ID INTEGER,
Product_brand_name VARCHAR (60),
Date_from DATE,
Date_to DATE,
PRIMARY KEY (Product_brand_ID AUTOINCREMENT)
);

-- Tabelle Dim_Product_department erstellen.
DROP TABLE IF EXISTS Dim_Product_department;
CREATE TABLE Dim_Product_department (
Product_department_ID INTEGER,
Product_department_name VARCHAR (60),
Date_from DATE,
Date_to DATE,
PRIMARY KEY (Product_department_ID AUTOINCREMENT)
);

-- Tabelle Dim_Store_location erstellen.
DROP TABLE IF EXISTS Dim_Store_location;
CREATE TABLE Dim_Store_location (
Store_location_ID INTEGER,
Store_location_name VARCHAR (60),
Date_from DATE,
Date_to DATE,
PRIMARY KEY (Store_location_ID AUTOINCREMENT)
);

-- Tabelle Dim_Store_type erstellen.
DROP TABLE IF EXISTS Dim_Store_type;
CREATE TABLE Dim_Store_type (
Store_type_ID INTEGER,
Store_type_name VARCHAR (60),
Date_from DATE,
Date_to DATE,
PRIMARY KEY (Store_type_ID AUTOINCREMENT)
);

-- Tabelle Dim_Customer_loyalty_status erstellen.
DROP TABLE IF EXISTS Dim_Customer_loyalty_status;
CREATE TABLE Dim_Customer_loyalty_status (
Customer_loyalty_status_ID INTEGER,
Customer_loyalty_status_name VARCHAR (15),
Date_from DATE,
Date_to DATE,
PRIMARY KEY (Customer_loyalty_status_ID AUTOINCREMENT)
);

-- Tabelle Dim_Payment_method erstellen.
DROP TABLE IF EXISTS Dim_Payment_method;
CREATE TABLE Dim_Payment_method (
Payment_method_ID INTEGER,
Payment_method_name VARCHAR (15),
Date_from DATE,
Date_to DATE,
PRIMARY KEY (Payment_method_ID AUTOINCREMENT)
);

