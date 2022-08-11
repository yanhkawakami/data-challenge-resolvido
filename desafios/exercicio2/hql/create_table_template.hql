CREATE EXTERNAL TABLE IF NOT EXISTS {table_name} ({columns_names_type})
STORED AS PARQUET
LOCATION 's3://iti-query-results/'
