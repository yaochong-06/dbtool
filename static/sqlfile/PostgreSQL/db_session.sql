/*数据库连接数*/
select 'db_check_db_session' as "db_check_db_session",
count(*)  as VALUE from pg_stat_activity;