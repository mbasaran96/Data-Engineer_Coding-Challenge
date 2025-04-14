#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 14 19:47:18 2025

@author: mertali
"""

"""ETL PIPELINE STAR SCHEMA"""

import pandas as pd
import sqlite3
import os



# === PARAMETER ===
CSV_PATH = "munich_sales_cleaned.csv"
DB_PATH = "star_schema.db"
SQL_SCHEMA_PATH = "create_tables_StarSchema.sql"

    
# === CSV laden ===
df = pd.read_csv(CSV_PATH, sep=';')

# === Verbindung zu SQLite ===
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# === SQL-Schema aus Datei laden und ausführen ===
with open(SQL_SCHEMA_PATH, "r", encoding="utf-8") as file:
    create_table_sql = file.read()
cursor.executescript(create_table_sql)

# === Tabellen befüllen (Daten vorbereiten, Transformieren) ===
Dim_Customer = df[['customer_id', 'customer_name', 'customer_email', 'customer_loyalty_status']].drop_duplicates()
Dim_District = df[['district_id', 'district_name', 'postal_code']].drop_duplicates()
Dim_Product = df[['product_id', 'product_name', 'product_category', 'product_subcategory', 'product_brand', 'product_department']].drop_duplicates()
Dim_Promotion = df[['promotion_id', 'promotion_name']].drop_duplicates()
Dim_Sales_staff = df[['sales_staff_id', 'sales_staff_name']].drop_duplicates()
Dim_Store = df[['store_id', 'district_id', 'store_name', 'store_location', 'store_type', 'store_size_sqm']].drop_duplicates()
Dim_Supplier = df[['supplier_id', 'supplier_name']].drop_duplicates()

Facts_Transaction = df[['transaction_id', 'supplier_id', 'product_id', 'store_id','customer_id',   
                        'sales_staff_id',  'promotion_id', 'invoice_number', 'transaction_date', 
                        'transaction_time', 'transaction_status', 'quantity', 'unit_price', 
                        'base_price', 'discount_rate', 'discount_applied',
                        'total_amount', 'tax_rate', 'tax_amount', 'payment_method']]

# === Daten in Tabellen schreiben ===
Dim_Customer.to_sql('Dim_Customer', conn, if_exists='replace', index=False)
Dim_District.to_sql('Dim_District', conn, if_exists='replace', index=False)
Dim_Product.to_sql('Dim_Product', conn, if_exists='replace', index=False)
Dim_Promotion.to_sql('Dim_Promotion', conn, if_exists='replace', index=False)
Dim_Sales_staff.to_sql('Dim_Sales_staff', conn, if_exists='replace', index=False)
Dim_Store.to_sql('Dim_Store', conn, if_exists='replace', index=False)
Dim_Supplier.to_sql('Dim_Supplier', conn, if_exists='replace', index=False)
Facts_Transaction.to_sql('Facts_Transaction', conn, if_exists='replace', index=False)

# === Tabelleninhalte prüfen ===
print("\nTabelleninhalt (Anzahl Zeilen):")
for table in ['Dim_Customer', 'Dim_District', 'Dim_Product', 'Dim_Promotion', 
              'Dim_Sales_staff', 'Dim_Store', 'Dim_Supplier', 'Facts_Transaction']:
    count = cursor.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
    print(f"{table}: {count} Zeilen")

# === Abschließen ===
conn.commit()
conn.close()

print("\nETL-Prozess abgeschlossen: Datenbank erfolgreich erstellt.")