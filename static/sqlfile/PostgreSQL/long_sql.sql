SELECT
client_addr, usename, datname,
clock_timestamp() - xact_start AS xact_age,
clock_timestamp() - query_start AS query_age,
round(date_part('epoch', NOW() - query_start)::NUMERIC / 60) AS VALUE,
state, query
FROM pg_stat_activity
where state='active'
ORDER BY coalesce(xact_start, query_start)