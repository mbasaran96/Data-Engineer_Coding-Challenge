#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 14 18:49:51 2025

@author: mertali
"""

import pandas as pd
import re

# Pfade
input_csv_path = 'munich_sales.csv'
output_csv_path = 'munich_sales_cleaned.csv'

# --- Währungs-Fix-Funktion ---
def fix_misformatted_currency(val):
    import datetime
    import pandas as pd

    # Wenn es ein Datum ist → extrahiere Monat/Jahr als Zahl
    if isinstance(val, (pd.Timestamp, datetime.datetime, datetime.date)):
        return float(f"{val.month}.{val.year % 100}")

    # Wenn es ein String ist
    if isinstance(val, str):
        months = {
            'jan': '01', 'feb': '02', 'mar': '03', 'apr': '04',
            'may': '05', 'jun': '06', 'jul': '07', 'aug': '08',
            'sep': '09', 'oct': '10', 'nov': '11', 'dec': '12'
        }

        match1 = re.match(r'([A-Za-z]{3})\s?(\d{1,2})', val)
        if match1:
            month = match1.group(1).lower()
            number = match1.group(2)
            if month in months:
                return float(f"{int(months[month])}.{number}")

        match2 = re.match(r'(\d{1,2})\.\s?([A-Za-z]{3})', val)
        if match2:
            number = match2.group(1)
            month = match2.group(2).lower()
            if month in months:
                return float(f"{number}.{int(months[month])}")

    try:
        return float(val)
    except:
        return None


# --- Hauptfunktion ---
def clean_munich_sales_data(input_csv_path: str, output_csv_path: str) -> None:
    df = pd.read_csv(input_csv_path, sep=';')

    # 1️⃣ Währungsformate korrigieren
    for col in ['unit_price', 'tax_amount', 'total_amount']:
        df[col] = df[col].apply(fix_misformatted_currency)

    # 2️⃣ Kunden-ID & E-Mail korrigieren
    valid_ids = df[
        df['customer_id'].notnull() &
        df['customer_name'].notnull() &
        df['customer_email'].notnull()
    ][['customer_name', 'customer_email', 'customer_id']]

    valid_ids['lookup_key_name'] = valid_ids['customer_name'].str.strip().str.lower()
    valid_ids['lookup_key_email'] = valid_ids['customer_email'].str.strip().str.lower()

    name_to_id = valid_ids.drop_duplicates('lookup_key_name').set_index('lookup_key_name')['customer_id'].to_dict()
    email_to_id = valid_ids.drop_duplicates('lookup_key_email').set_index('lookup_key_email')['customer_id'].to_dict()
    name_to_email = valid_ids.drop_duplicates('lookup_key_name').set_index('lookup_key_name')['customer_email'].to_dict()

    def fill_customer_id(row):
        if pd.isna(row['customer_id']):
            name_key = str(row['customer_name']).strip().lower()
            email_key = str(row['customer_email']).strip().lower()
            return name_to_id.get(name_key) or email_to_id.get(email_key)
        return row['customer_id']

    def fill_customer_email(row):
        if pd.isna(row['customer_email']):
            name_key = str(row['customer_name']).strip().lower()
            return name_to_email.get(name_key, None)
        return row['customer_email']

    # 3️⃣ Konvertieren & bereinigen
    for col in ['discount_rate', 'quantity', 'unit_price', 'total_amount', 'tax_rate', 'base_price', 'tax_amount']:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    df['quantity'] = df['quantity'].abs()
    df['unit_price'] = df['unit_price'].abs()

    # 4️⃣ Fehlende quantity berechnen
    df['quantity'] = df.apply(
        lambda row: row['total_amount'] / row['unit_price']
        if pd.isna(row['quantity']) and pd.notna(row['unit_price']) and row['unit_price'] != 0 and pd.notna(row['total_amount'])
        else row['quantity'],
        axis=1
    )

    # 5️⃣ total_amount neu berechnen, aber nur wenn leer oder negativ
    df['total_amount'] = df.apply(
        lambda row: row['unit_price'] * row['quantity']
        if pd.isna(row['total_amount']) or row['total_amount'] < 0
        else row['total_amount'],
        axis=1
    )

    # 6️⃣ tax_amount neu berechnen, aber nur wenn leer
    df['tax_amount'] = df.apply(
        lambda row: row['total_amount'] * row['tax_rate']
        if pd.isna(row['tax_amount']) and pd.notna(row['total_amount']) and pd.notna(row['tax_rate'])
        else row['tax_amount'],
        axis=1
    )

    # 7️⃣ discount_rate berechnen (wenn leer)
    df['discount_rate'] = df.apply(
        lambda row: (row['unit_price'] - row['base_price']) / row['unit_price']
        if pd.isna(row['discount_rate']) and pd.notna(row['unit_price']) and pd.notna(row['base_price']) and row['unit_price'] != 0
        else row['discount_rate'],
        axis=1
    )
    df['discount_rate'] = pd.to_numeric(df['discount_rate'], errors='coerce').round(2)

    # 8️⃣ Rabatt angewendet: True/False
    df['discount_applied'] = df['discount_rate'].apply(lambda x: True if x != 0.0 else False)

    # 9️⃣ Kunden-ID / E-Mail auffüllen
    df['customer_id'] = df.apply(fill_customer_id, axis=1)
    df['customer_email'] = df.apply(fill_customer_email, axis=1)

    # 🔟 Runden
    df['total_amount'] = df['total_amount'].round(2)
    df['quantity'] = df['quantity'].round(0)
    df['tax_amount'] = df['tax_amount'].round(2)

    # 🔄 Export
    df.to_csv(output_csv_path, index=False, sep=';')
    print(f"✔ Bereinigung abgeschlossen. Datei gespeichert unter: {output_csv_path}")

# 👉 Aufruf starten
clean_munich_sales_data(input_csv_path, output_csv_path)


