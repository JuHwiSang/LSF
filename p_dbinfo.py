import pandas as pd
from tabulate import tabulate

"""
Database: exable_db
+--------------+---------------------------
| table        | column
+--------------+---------------------------
| exable_table | exable_col1
|              | exable_col2
+--------------+---------------------------
"""

# dict_test = {
#     'table': ["exable_table", ""],
#     'column': ['exable_col1', 'exable_col2'],
# }

# df_test = pd.DataFrame(dict_test)
# print(tabulate(df_test, headers='keys', tablefmt='psql', showindex=False))

def p_dbinfo(dbinfo: dict[str, dict[str, list[str]]]) -> None:
    for db_name, table_dict in dbinfo.items():
        if not table_dict: continue
        print(f"\nDatabase: {db_name}")

        ptable = []
        pcolumn = []
        for table_name, columns in table_dict.items():
            ptable.append(table_name)
            for i in range(len(columns)-1):
                ptable.append("")
            pcolumn.extend(columns)

        prc = {
            'table': ptable,
            'column': pcolumn
        }

        df_test = pd.DataFrame(prc)
        print(tabulate(df_test, headers='keys', tablefmt='psql', showindex=False))
        # print()