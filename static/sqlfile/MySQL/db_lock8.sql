/*MySQL8.0锁信息查询*/
select
distinct concat_ws(':', pdl.object_schema,pdl.object_name, index_name) as b_res,
info2.trx_id as w_trx_id,
cast(info2.trx_mysql_thread_id as char) as w_waiter,
timestampdiff(second, info2.trx_wait_started, current_timestamp) as w_wait_time,
info2.trx_query as w_sql_text,
concat_ws('.',pdl.object_schema,pdl.object_name) as w_waiting_table_lock,
info1.trx_id as b_trx_id,
cast(info1.trx_mysql_thread_id as char) as b_blocker,
substring(ip.host, 1, instr(ip.host, ':') - 1) as b_host,
substring(ip.host, instr(ip.host, ':') +1) as b_port,
if(ip.command = "sleep", ip.time, 0) as b_idle_in_trx,
pe.sql_text as b_sql_text
from performance_schema.data_lock_waits as pd
inner join information_schema.innodb_trx as info1 on info1.trx_id = pd.blocking_engine_transaction_id
inner join information_schema.innodb_trx as info2 on info2.trx_id = pd.requesting_engine_transaction_id
inner join performance_schema.data_locks as pdl on pd.requesting_engine_lock_id = pdl.engine_lock_id
left join information_schema.processlist as ip on ip.id = info1.trx_mysql_thread_id
left join performance_schema.threads as pt on pt.processlist_id = info1.trx_mysql_thread_id
left join performance_schema.events_statements_current as pe on pt.thread_id = pe.thread_id
order by w_wait_time desc;