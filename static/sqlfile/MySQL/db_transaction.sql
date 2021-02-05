/*活跃事务*/
select
    trx_id,
    trx_state,
    DATE_FORMAT(trx_started, '%Y-%m-%d %T') TRX_STARTED,
    trx_requested_lock_id,
    DATE_FORMAT(trx_wait_started, '%Y-%m-%d %T') TRX_WAIT_STARTED,
    trx_mysql_thread_id as SESSION_ID,
    trx_query,
    trx_operation_state,
    trx_tables_in_use,
    trx_tables_locked,
    trx_rows_locked,
    TRX_ROWS_MODIFIED,
    trx_isolation_level,
    TIMESTAMPDIFF(SECOND, trx_started, CURRENT_TIMESTAMP) AS TRX_SECONDS,
    trx.trx_mysql_thread_id
from information_schema.innodb_trx trx;