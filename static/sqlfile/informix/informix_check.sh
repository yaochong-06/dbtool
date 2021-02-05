#!/bin/bash
mkdir -p ../../../xunjianinformix/
mkdir -p ../../../xunjianinformix/ses0
cd ../../../xunjianinformix/
rm -f ses0/*
rmdir ses0
rm -f *

userdblist_func(){
dbaccess sysmaster <<!
unload to tmpselectlog
select * from sysdatabases;
!
cat tmpselectlog |awk -F \| 'BEGIN {printf("%20s%20s%20s%20s%20s%20s%20s%20s%20s%20s\n","dbname","partnum","owner","created","is_logging","is_buff_log","is_ansi","is_nls","is_case_insens","flags")} ; {printf("%20s%20s%20s%20s%20s%20s%20s%20s%20s%20s\n",$1,$2,$3,$4,$5,$6,$7,$8,$9,$10)}'
dbaccess sysmaster <<!
unload to userdblist select name from sysdatabases where name not in ("sysmaster","sysutils","sysadmin","sysuser");
!
}

dbspace_func(){
dbaccess sysmaster <<!
unload to tmpselectlog
select
d.name,d.pagesize,trunc(sum(c.chksize*(select pagesize from sysdbspaces where dbsnum='1'))/1024/1024/1024,1) dbssize_G,trunc(sum(nfree*(select pagesize from sysdbspaces where dbsnum='1'))/1024/1024/1024,1) dbsfree_G ,trunc(sum(chksize-nfree)/sum(chksize)*100,2) used_ratio
from
sysdbspaces d, syschunks c
where
d.dbsnum=c.dbsnum
group by d.name,d.pagesize
order by 5 desc;
!
cat tmpselectlog |awk -F \| 'BEGIN {printf("%20s%20s%20s%20s%20s\n","name","pagesize","dbssize_G","dbsfree_G","used_ratio")} ; {printf("%20s%20s%20s%20s%20.2f\n",$1,$2,$3,$4,$5)}'
}

tablespace_func(){
dbaccess sysmaster <<!
SELECT first 20 b.pe_partnum ptn,
            count(b.pe_size) exts,
              sum(b.pe_size) pages
          FROM sysptnext b
         GROUP BY 1
         order by 3 desc
          INTO TEMP tmp_pt WITH NO LOG;
          unload to tmpselectlog
          SELECT a.dbsname, a.tabname, a.partnum, b.exts, b.pages
            FROM sysptprof a, tmp_pt b
           WHERE a.partnum = b.ptn
           order by 5 desc;
!
cat tmpselectlog |awk -F \| 'BEGIN {printf("%20s%40s%20s%20s%20s\n","dbname","tabname","partnum","exts","pages")} ; {printf("%20s%40s%20s%20s%20s\n",$1,$2,$3,$4,$5)}'
}


tablescan_func(){
cat userdblist |awk -F \| '{print $1}'| while read vdbname
do
echo "\nbegin big table scan in DB: $vdbname"
echo "
unload to tmpselectlog
SELECT FIRST 20 p.dbsname, p.tabname,t.nrows, sum(p.seqscans) tot_seqscans
FROM sysmaster:sysptprof p,systables t
WHERE p.dbsname NOT LIKE 'sys%'
AND p.dbsname = '$vdbname'
AND p.tabname = t.tabname
AND t.tabname NOT LIKE 'sys%'
GROUP BY 1,2,3
ORDER BY 4 DESC,3 DESC
;" |dbaccess $vdbname
cat tmpselectlog |awk -F \| 'BEGIN {printf("%20s%40s%20s%20s%20s\n","dbname","tabname","nrows","tot_seqscans","n*s")} ; {printf("%20s%40s%20s%20s%20s\n",$1,$2,$3,$4,$3*$4)}'
echo "\nend big table scan in DB: $vdbname"
done
}



indexuniq_func(){
cat userdblist |awk -F \| '{print $1}'| while read vdbname
do
echo "\nbegin index uniq in DB: $vdbname"
dbaccess $vdbname <<!
unload to tmpselectlog
SELECT FIRST 20 t.tabname, i.idxname, t.nrows, i.nunique, (i.nunique/t.nrows)*100 pcniq
FROM systables t, sysindexes i
WHERE t.tabid =i.tabid
AND t.tabid > 99
and t.nrows > 100
ORDER BY 5 , 3 ;
!
cat tmpselectlog |awk -F \| 'BEGIN {printf("%40s%40s%20s%20s%20s\n","tabname","idxname","nrows","nunique","pcniq")} ; {printf("%40s%40s%20s%20s%20.2f\n",$1,$2,$3,$4,$5)}'
echo "\nend index uniq in DB: $vdbname"
done
}



indexlevel_func(){
cat userdblist |awk -F \| '{print $1}'| while read vdbname
do
echo "\nbegin index level in DB: $vdbname"
echo "unload to tmpselectlog
select first 20 '$vdbname' dbname, idxname, levels from sysindexes order by 3 desc
;" |dbaccess $vdbname
cat tmpselectlog |awk -F \| 'BEGIN {printf("%20s%40s%20s\n","dbname","idxname","levels")} ; {printf("%20s%40s%20s\n",$1,$2,$3)}'
echo "\nend index level in DB: $vdbname"
done
}


dbsize_func(){
dbaccess sysmaster <<!
unload to tmpselectlog
select database_name[1,15] ,round(sum(pe_size*pagesize)/1024/1024/1024) size_G
from
   sysptnext,
   (select partnum,dbsname database_name from systabnames ) wa,
   (select b.dbsname,a.name,a.pagesize from sysdbspaces a,systabnames b where a.dbsnum=partdbsnum(b.partnum) and b.tabname="systables") wb
where pe_partnum = partnum and wa.database_name = wb.dbsname group by database_name;
!
cat tmpselectlog |awk -F \| 'BEGIN {printf("%20s%20s\n","database_name","size_G")} ; {printf("%20s%20s\n",$1,$2)}'
}


big_object_func(){
dbaccess sysmaster <<!
unload to tmpselectlog
select first 20 sd.name,
st.dbsname databasename,st.tabname,
format_units(sum(sin.ti_npused),max(sd.pagesize)) used_size
from systabnames st,sysdbspaces sd,systabinfo sin
where sd.dbsnum = trunc(st.partnum/1048576)
and st.partnum=sin.ti_partnum
and st.tabname not matches 'sys*'
and st.tabname<>'TBLSpace'
group by 1,2,3
order by 1,sum(sin.ti_npused) desc;
!
cat tmpselectlog |awk -F \| 'BEGIN {printf("%20s%20s%40s%20s\n","dbspaces","databasename","tabname","used_size")} ; {printf("%20s%20s%40s%20s\n",$1,$2,$3,$4)}'
}


extens_func(){
dbaccess sysmaster <<!
unload to tmpselectlog
SELECT FIRST 20 t.dbsname, t.tabname, count(*)
FROM sysmaster:systabnames t, sysmaster:sysextents e
WHERE t.dbsname = e.dbsname
AND t.tabname = e.tabname
AND t.tabname[1,3] != "sys"
GROUP BY 1,2
ORDER BY 3 DESC;
!
cat tmpselectlog |awk -F \| 'BEGIN {printf("%20s%40s%20s\n","dbname","tabname","extens")} ; {printf("%20s%40s%20s\n",$1,$2,$3)}'
}


ses0_func(){
mkdir -p ses0
cd ses0
i=100
while [ $i -le 160 ]
do
echo "巡检脚本采集中，请耐心等待..."
onstat -g ses 0 > ses_${i}
let i=$i+1
sleep 1
done
cd ../..
}

onlinelog_func(){
online_log=$(onstat -m |grep "^Message Log File:"|awk '{print $NF}')
tail -100000 ${online_log}|grep -E "Error|Thread|err|Assert|Aborting|[0-2][0-9]:[0-6][0-9]:[0-6][0-9] 20[12][0-9]$"
onstat -d |grep PD
}


tabnames_func(){
dbaccess sysmaster <<!
unload to tmpselectlog
select hex(partnum),* from systabnames;
!
cat tmpselectlog |awk -F \| 'BEGIN {printf("%20s%20s%20s%20s%40s%20s%20s\n","partnum","partnum","dbname","owner","tabname","collate","dbsnum")} ; {printf("%20s%20s%20s%20s%40s%20s%20s\n",$1,$2,$3,$4,$5,$6,$7)}'
}

# 实例名称
onstat -       > a1.instance
# 操作系统资源
onstat -g osi  > a2.osi
# 数据库运行概要
onstat -p      > a3.p
# 当前会话数量及状态分类
onstat -u      > a4.u
# 当前事务数量
onstat -x      > a5.x
# 当前锁数量
onstat -k      > a6.k
# CPU使用情况
vmstat 1 10    > a7.vmstat &
# 内存使用情况
free           > a8.free
# 磁盘IO情况
sar -d 1 10     > a9.sar_d  &
# 网络IO情况
sar -n DEV 1 10 > b1.sar_n  &
# 数据库V段数
onstat -g seg   > b2.seg
# 检查点情况
onstat -g ckp   > b3.ckp
# 线程队列
onstat -g ath   > b4.ath
# 用户数据库列表
userdblist_func > b5.userdblist_func
# DBSPACE空间检查
dbspace_func    > b6.dbspace_func
# TABLESPACE检查
tablespace_func > b7.tablespace_func
# 大表顺序扫描检查
tablescan_func  > b8.tablescan_func
# 索引唯一性检查
indexuniq_func  > b9.indexuniq_func
# 索引层次检查
indexlevel_func > c1.indexlevel_func
# 数据库大小检查
echo 'flag 888888888888'
dbsize_func     > c2.dbsize_func
# TOP前20:对象大小
echo 'flag 999999999999'
big_object_func > c3.big_object_func
# TOP前20:对象分段数
extens_func     > c4.extens_func
# TOP前20:对象IO量
onstat -g ppf   > c5.ppf
onstat -l      > c6.l
onstat -d      > c7.d
onstat -D      > c8.D
onstat -P      > c9.P
onstat -g tpf  > d1.tpf
onstat -g buf  > d2.buf
onstat -g ioq  > d3.ioq
onstat -g iof  > d4.iof
onstat -g iov  > d5.iov
onstat -F      > d6.F
onstat -R      > d7.R
onstat -C      > d8.C
onstat -g glo  > d9.glo
onstat -g wst  > e1.wst
onstat -g cpu  > e2.cpu
onstat -g ntt  > e3.ntt
onstat -g ntu  > e4.ntu
onstat -g ntd  > e5.ntd
onstat -c      > e6.c
tabnames_func  > e7.tabnames_func
onstat -g dri  > e8.dri
onstat -g rss  > e9.rss
# TOP前20:并发SQL
ses0_func
# TOP前20:慢SQL(同上不用单独收集)
# 数据库运行日志检查
onlinelog_func > f1.onlinelog
# 数据库备份情况检查
onstat -g arc  > f2.arc
echo "关于数据库数据的备份情况，请备份岗同事保证数据安全。"

#onstat -g spi  > f3.spi
rm userdblist
rm tmpselectlog

tar zcvf xunjianinformix`date '+%Y%m%d_%H%M%S'`.tar.gz xunjianinformix
