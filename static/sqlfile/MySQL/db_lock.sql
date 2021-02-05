/*db_lock */
SELECT
distinct concat_ws(':', lock_table, lock_index, lock_space, lock_page, lock_rec) as B_RES,
r.trx_id AS W_TRX_ID,
cast(r.trx_mysql_thread_id as char) AS W_WAITER,
TIMESTAMPDIFF(SECOND, r.trx_wait_started, CURRENT_TIMESTAMP) AS W_WAIT_TIME,
r.trx_query AS W_SQL_TEXT,
l.lock_table AS W_WAITING_TABLE_LOCK,
b.trx_id AS B_TRX_ID,
ct.sql_text as B_SQL_TEXT,
cast(b.trx_mysql_thread_id as char) AS B_BLOCKER,
SUBSTRING(p.host, 1, INSTR(p.host, ':') - 1) AS B_HOST,
SUBSTRING(p.host, INSTR(p.host, ':') +1) AS B_PORT,
IF(p.command = "Sleep", p.time, 0) AS B_IDLE_IN_TRX

FROM INFORMATION_SCHEMA.INNODB_LOCK_WAITS AS w
INNER JOIN INFORMATION_SCHEMA.INNODB_TRX AS b ON b.trx_id = w.blocking_trx_id
INNER JOIN INFORMATION_SCHEMA.INNODB_TRX AS r ON r.trx_id = w.requesting_trx_id
INNER JOIN INFORMATION_SCHEMA.INNODB_LOCKS AS l ON w.requested_lock_id = l.lock_id
LEFT JOIN INFORMATION_SCHEMA.PROCESSLIST AS p ON p.id = b.trx_mysql_thread_id
left join performance_schema.threads as t on t.processlist_id = b.trx_mysql_thread_id
left join performance_schema.events_statements_current AS ct on t.thread_id = ct.thread_id
ORDER BY W_WAIT_TIME DESC;