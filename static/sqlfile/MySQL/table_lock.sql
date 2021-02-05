select 'Waiting for table' as STATE ,count(*) as COUNT
from information_schema.processlist
where (state='Waiting for table flush' or info='FLUSH TABLES WITH ');