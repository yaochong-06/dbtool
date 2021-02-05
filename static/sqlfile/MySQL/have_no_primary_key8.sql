select
ta.name as table_name,
ta.name as MESSAGE
from information_schema.innodb_indexes ind,
information_schema.innodb_tables ta
where ind.table_id=ta.table_id
and ind.name='GEN_CLUST_INDEX';