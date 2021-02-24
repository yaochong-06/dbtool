-- 检查数据库一个月内告警日志中的ORA告警
SELECT
    'db_check_alert_check' as "db_check_alert_check",
	message_text message,
	to_char( ORIGINATING_TIMESTAMP, 'yyyy-mm-dd HH24:mi:ss' ) time,
	INST_ID
FROM
	v$diag_alert_ext
WHERE
	ORIGINATING_TIMESTAMP > ( SYSDATE - 30 )
	AND message_text LIKE '%ORA-%'
	AND trim(component_id) = 'rdbms';