# New feature implementation

# put this in a function to write multiple tables to SQL

def write_tables_to_sql(tables_dict, connection):
    """
    Write multiple DataFrames to SQL tables.

    Parameters:
    tables_dict (dict): A dictionary where keys are table names and values are DataFrames.
    connection (sqlite3.Connection): SQLite database connection object.
    """
    for table_name, df in tables_dict.items():
        df.to_sql(table_name, connection, if_exists='replace', index=False)