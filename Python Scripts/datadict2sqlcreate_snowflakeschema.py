import pandas as pd
from icecream import ic

def write_sqlcreate_for_table(table: pd.DataFrame, fk_dict: dict):
    """Writes SQL Create statement for one table."""
    table_name = table.Tabellenname.unique()[0]
    create_statement = f'-- Tabelle {table_name} erstellen.\n'
    create_statement += f'DROP TABLE IF EXISTS {table_name};\n'
    create_statement += f'CREATE TABLE {table_name} (\n'
    pks = []
    fks = []
    for row in table.index:
        #ic(row)
        if table.loc[row, "Spaltentyp"].upper() in ['VARCHAR', 'TEXT']:
            row_sql = f'{table.loc[row, "Spaltenname"]} {table.loc[row, "Spaltentyp"].upper()} ({int(table.loc[row, "Zeichenlaenge"])}),\n'
        elif table.loc[row, "Spaltentyp"].upper() == 'DECIMAL':
            row_sql = f'{table.loc[row, "Spaltenname"]} {table.loc[row, "Spaltentyp"].upper()} ({table.loc[row, "Zeichenlaenge"]}),\n'
        else:
            row_sql = f'{table.loc[row, "Spaltenname"]} {table.loc[row, "Spaltentyp"].upper()},\n'
        if table.loc[row, 'PK'] == 'PK':
            pks.append(table.loc[row, "Spaltenname"])
        if table.loc[row, 'FK'] == 'FK':
            fks.append(table.loc[row, "Spaltenname"])
        create_statement += row_sql
    for fk in fks:
        fk_sql = f'FOREIGN KEY ({fk}) REFERENCES {fk_dict[fk]}({fk}),\n'
        create_statement += fk_sql
    if len(pks) == 1:
        create_statement += f'PRIMARY KEY ({pks[0]} AUTOINCREMENT)\n'
    else:
        create_statement += f'PRIMARY KEY ({", ".join(pks)})\n'
    create_statement += ');\n\n'
    return create_statement

def get_primary_table_for_FK(data_dict: pd.DataFrame, FK_name: str) -> str:
    """Returns primary table for given FK. If no table is found raises error."""
    prim_table = data_dict.loc[(data_dict.Spaltenname == FK_name) & (data_dict.PK == 'PK') & (data_dict.FK != 'FK') , 'Tabellenname']
    if len(prim_table.values) != 1:
        ic(f'Check FK  - PK naming for {FK_name}. {len(prim_table.values)}')
    return prim_table.values[0] 

def build_FK_dict(data_dict: pd.DataFrame) -> dict:
    """Function to collect primary table for Foreign Keys and save into dict."""
    with_FK = data_dict.loc[data_dict.FK == 'FK']
    list_of_fks = with_FK.Spaltenname.unique()
    fk_prim_table = {}
    for fk in list_of_fks:
        fk_prim_table[fk] = get_primary_table_for_FK(data_dict, fk)
    return fk_prim_table

def write_create_table_statements(data_dict: pd.DataFrame, dd_name: str):
    """Writes all create table statements to sql file."""
    fk_dict = build_FK_dict(data_dict)
    with open(f"create_tables_{dd_name}.sql", 'w') as w_file:
        for t_name in data_dict.Tabellenname.unique():
            table_df = data_dict.loc[data_dict.Tabellenname == t_name]
            w_file.write(write_sqlcreate_for_table(table_df, fk_dict ))

def main():
    pass

if __name__=='__main__':
    datadict_path = 'SnowflakeSchema.csv' # Name vom Datadict
    dd_name = datadict_path.split('/')[-1][:-4]
    data_dict = pd.read_csv(datadict_path, sep=';')
    write_create_table_statements(data_dict, dd_name)
    main()