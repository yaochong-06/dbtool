select 'db_check_db_top_activity' as "db_check_db_top_activity",
pid session_id,
datname, usename username,
application_name, client_hostname,
client_addr,
CASE WHEN EXTRACT(EPOCH FROM now() - query_start) < 0 THEN 0 ELSE EXTRACT(EPOCH FROM now() - query_start) END as sql_elapsed_time,
wait_event,
wait_event_type, state,
query sql_text,
md5(query) sql_id,
1 as value
from pg_stat_activity where pid <> pg_backend_pid() and state = 'active';