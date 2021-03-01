-- 检查数据库一个月内告警日志中的ORA告警
col message for a100
col time for a20
set linesize 200
set pages 100
SELECT
	message_text message,
	to_char( ORIGINATING_TIMESTAMP, 'yyyy-mm-dd HH24:mi:ss' ) time,
	INST_ID
FROM
	v$diag_alert_ext
WHERE
	ORIGINATING_TIMESTAMP > ( SYSDATE - 30 )
	AND message_text LIKE '%ORA-%'
	AND trim(component_id) = 'rdbms';