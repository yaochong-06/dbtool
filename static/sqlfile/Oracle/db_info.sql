select
'db_check_db_info' as "db_check_db_info",
name,
(select count(*) from gv$instance) inst_cnt,
(SELECT version platform FROM PRODUCT_COMPONENT_VERSION where product like 'Oracle%') VERSION,
log_mode,
open_mode,
DATABASE_ROLE,
FORCE_LOGGING,
FLASHBACK_ON from v$database;