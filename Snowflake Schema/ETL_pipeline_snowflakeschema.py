#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 14 21:49:30 2025

@author: mertali
"""

"""ETL PIPELINE SNOWFLAKE SCHEMA"""

import pandas as pd
import sqlite3

# === PARAMETER ===
CSV_PATH = "munich_sales_cleaned.csv"
DB_PATH = "snowflake_schema.db"
SQL_SCHEMA_PATH = "create_tables_SnowflakeSchema.sql"

# === CSV laden ===
df = pd.read_csv(CSV_PATH, sep=';')

# === Verbindung zu SQLite ===
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# === SQL-Schema aus Datei laden und ausführen ===
with open(SQL_SCHEMA_PATH, "r", encoding="utf-8") as file:
    create_table_sql = file.read()
cursor.executescript(create_table_sql)

# === Funktion zum Erstellen von Dimensionstabellen mit IDs ===
def create_dim_table(df, column_name, id_name):
    unique_values = df[column_name].dropna().drop_duplicates().reset_index(drop=True)
    dim_table = pd.DataFrame({
        id_name: range(1, len(unique_values) + 1),
        column_name: unique_values
    })
    value_to_id_map = dict(zip(dim_table[column_name], dim_table[id_name]))
    return dim_table, value_to_id_map

# === Dimensionstabellen erstellen und Mappings anwenden ===
columns_to_extract = {
    'customer_loyalty_status': 'customer_loyalty_status_ID',
    'product_category': 'product_category_ID',
    'product_subcategory': 'product_subcategory_ID',
    'product_brand': 'product_brand_ID',
    'product_department': 'product_department_ID',
    'store_location': 'store_location_ID',
    'store_type': 'store_type_ID',
    'payment_method': 'payment_method_ID'
}

dim_tables = {}
mappings = {}

for column, id_col in columns_to_extract.items():
    dim_table, mapping = create_dim_table(df, column, id_col)
    dim_tables[column] = dim_table
    mappings[column] = mapping

# === Dim_Customer (inkl. Mapping Loyalty Status) ===
Dim_Customer = df[['customer_id', 'customer_name', 'customer_email', 'customer_loyalty_status']].drop_duplicates()
Dim_Customer['customer_loyalty_status_ID'] = Dim_Customer['customer_loyalty_status'].map(mappings['customer_loyalty_status'])
Dim_Customer = Dim_Customer.drop(columns=['customer_loyalty_status'])

# === Dim_Product (mit Produkt-Subdimensionen) ===
Dim_Product = df[['product_id', 'product_name']].drop_duplicates()
Dim_Product['product_category_ID'] = df['product_category'].map(mappings['product_category'])
Dim_Product['product_subcategory_ID'] = df['product_subcategory'].map(mappings['product_subcategory'])
Dim_Product['product_brand_ID'] = df['product_brand'].map(mappings['product_brand'])
Dim_Product['product_department_ID'] = df['product_department'].map(mappings['product_department'])

# === Dim_Store (inkl. Subdimensionen) ===
Dim_Store = df[['store_id', 'district_id', 'store_name']].drop_duplicates()
Dim_Store['store_location_ID'] = df['store_location'].map(mappings['store_location'])
Dim_Store['store_type_ID'] = df['store_type'].map(mappings['store_type'])
Dim_Store['store_size_sqm'] = df['store_size_sqm']

# === Facts_Transaction (Mapping von payment_method) ===
Facts_Transaction = df[['transaction_id', 'supplier_id', 'product_id', 'store_id', 'customer_id',   
                        'sales_staff_id', 'promotion_id', 'invoice_number', 'transaction_date', 
                        'transaction_time', 'transaction_status', 'quantity', 'unit_price', 
                        'base_price', 'discount_rate', 'discount_applied',
                        'total_amount', 'tax_rate', 'tax_amount']].copy()

Facts_Transaction['payment_method_ID'] = df['payment_method'].map(mappings['payment_method'])

# === Weitere Dimensionen ===
Dim_District = df[['district_id', 'district_name', 'postal_code']].drop_duplicates()
Dim_Promotion = df[['promotion_id', 'promotion_name']].drop_duplicates()
Dim_Sales_staff = df[['sales_staff_id', 'sales_staff_name']].drop_duplicates()
Dim_Supplier = df[['supplier_id', 'supplier_name']].drop_duplicates()

# === Alle Dimensionstabellen in Datenbank schreiben ===
Dim_Customer.to_sql('Dim_Customer', conn, if_exists='replace', index=False)
Dim_District.to_sql('Dim_District', conn, if_exists='replace', index=False)
Dim_Product.to_sql('Dim_Product', conn, if_exists='replace', index=False)
Dim_Promotion.to_sql('Dim_Promotion', conn, if_exists='replace', index=False)
Dim_Sales_staff.to_sql('Dim_Sales_staff', conn, if_exists='replace', index=False)
Dim_Store.to_sql('Dim_Store', conn, if_exists='replace', index=False)
Dim_Supplier.to_sql('Dim_Supplier', conn, if_exists='replace', index=False)
Facts_Transaction.to_sql('Facts_Transaction', conn, if_exists='replace', index=False)

# === Neue Subdimensionen schreiben ===
dim_tables['customer_loyalty_status'].to_sql('Dim_Customer_loyalty_status', conn, if_exists='replace', index=False)
dim_tables['product_category'].to_sql('Dim_Product_category', conn, if_exists='replace', index=False)
dim_tables['product_subcategory'].to_sql('Dim_Product_subcategory', conn, if_exists='replace', index=False)
dim_tables['product_brand'].to_sql('Dim_Product_brand', conn, if_exists='replace', index=False)
dim_tables['product_department'].to_sql('Dim_Product_department', conn, if_exists='replace', index=False)
dim_tables['store_location'].to_sql('Dim_Store_location', conn, if_exists='replace', index=False)
dim_tables['store_type'].to_sql('Dim_Store_type', conn, if_exists='replace', index=False)
dim_tables['payment_method'].to_sql('Dim_Payment_method', conn, if_exists='replace', index=False)

# === Tabelleninhalte prüfen ===
print("\nTabelleninhalt (Anzahl Zeilen):")
tables = ['Dim_Customer', 'Dim_District', 'Dim_Product', 'Dim_Promotion', 
          'Dim_Sales_staff', 'Dim_Store', 'Dim_Supplier', 'Facts_Transaction'] + \
         ['Dim_Customer_Loyalty_Status', 'Dim_Product_Category', 'Dim_Product_Subcategory',
          'Dim_Product_Brand', 'Dim_Product_Department', 'Dim_Store_Location', 'Dim_Store_Type', 'Dim_Payment_Method']

for table in tables:
    count = cursor.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
    print(f"{table}: {count} Zeilen")

# === Abschließen ===
conn.commit()
conn.close()

print("\nETL-Prozess abgeschlossen: Snowflake-Schema-Datenbank erfolgreich erstellt.")
