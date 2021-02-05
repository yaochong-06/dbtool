SELECT 'db_check_db_space' as "db_check_db_space",
       a.tablespace_name,
       Round((total - free ) / maxsize * 100, 1) USED_PCT,
       b.autoextensible,
       total total_mb,
       (total - free ) USED,
       free,
       b.cnt DATAFILE_COUNT,
       c.status,
       c.CONTENTS,
       c.extent_management,
       c.allocation_type,
       b.maxsize
FROM   (SELECT tablespace_name,
               Round(SUM(bytes) / ( 1024 * 1024 ), 1) free
        FROM   dba_free_space
        GROUP  BY tablespace_name) a,
       (SELECT tablespace_name,
               Round(SUM(bytes) / ( 1024 * 1024 ), 1) total,
               Count(*)                               cnt,
               Max(autoextensible)                  autoextensible,
               sum(decode(autoextensible, 'YES', floor(maxbytes/1048576), floor(bytes / 1048576 ))) maxsize
        FROM   dba_data_files
        GROUP  BY tablespace_name) b,
       dba_tablespaces c
WHERE  a.tablespace_name = b.tablespace_name
       AND a.tablespace_name = c.tablespace_name
UNION ALL
SELECT /*+ NO_MERGE */ 'db_check_db_space' as "db_check_db_space",
                       a.tablespace_name,
                       Round(100 * ( B.tot_gbbytes_used / A.maxsize ), 1) PERC_USED,
                       a.aet,
                       Round(A.avail_size_gb, 1),
                       Round(B.tot_gbbytes_used, 1),
                       ( Round(A.avail_size_gb, 1) - Round(B.tot_gbbytes_used, 1) ),
                       a.cnt DATAFILE_COUNT,
                       c.status,
                       c.CONTENTS,
                       c.extent_management,
                       c.allocation_type,
                       a.maxsize
FROM   (SELECT tablespace_name,
               SUM(bytes) / Power(2, 20) AVAIL_SIZE_GB,
               Max(autoextensible)       aet,
               Count(*)                  cnt,
               sum(decode(autoextensible, 'YES', floor(maxbytes/1048576), floor(bytes/1048576))) maxsize
        FROM dba_temp_files
        GROUP  BY tablespace_name) A,
       (SELECT tablespace_name,
               SUM(bytes_used) / Power(2, 20) TOT_GBBYTES_USED
        FROM   gv$temp_extent_pool
        GROUP  BY tablespace_name) B,
       dba_tablespaces c
WHERE  a.tablespace_name = b.tablespace_name
       AND a.tablespace_name = c.tablespace_name
order by 2 desc;