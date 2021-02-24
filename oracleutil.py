#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2021/2/1 下午3:55
# @Author  : yaochong/Chongzi
# @FileName: oracleutil.py.py
# @Software: PyCharm
# @Blog    ：https://github.com/yaochong-06/ ; http://blog.itpub.net/29990276

import os
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import re
from data import remove_last_line

"""
搜索脚本
"""


def search():
    input_str = input("请输入要搜索内容：")
    lines = open('static/search.txt').readlines()
    for l in lines:
        tmp_str = l[0:50].replace('#', '')
        score = fuzz.ratio(tmp_str, input_str)
        if score > 30:
            res_list = ''.join(l).split('&&')
            for res in res_list:
                print(res.lstrip())


"""
bbed初始化
"""


def init_bbed():
    oracle_home = input("请输入$ORACLE_HOME：")
    sqlplus_path = input("请输入sqlplus的绝对路径：")
    home = '/home/oracle'
    flag = input("Oracle家目录是否为/home/oracle (Y/实际家目录)：")
    if flag == 'Y':
        home = '/home/oracle'
    else:
        home = flag
    print(flag)
    os.popen(f"""echo '' > {home}/filelist.txt""")
    res = os.popen(f"""
export ORACLE_HOME={oracle_home} && {sqlplus_path} / as sysdba <<EOF
set colsep "|"
set linesize 32767
set pages 20000
@static/sqlfile/Oracle/bbed.sql
EOF""", 'r', 100).readlines()
    # 生成二维列表
    for re in res:
        if re[0].isdigit():
            os.popen(f"""echo '{remove_last_line(re)}' >> {home}/filelist.txt""")
    print(f'1、生成{home}/filelist.txt')
    os.popen(f'cat {home}/filelist.txt')
    print("2、拷贝依赖文件ssbbded.o sbbdpt.o bbedus.msb")
    os.popen(f'cp static/Oracle/ssbbded.o {oracle_home}/rdbms/lib/ssbbded.o')
    os.popen(f'cp static/Oracle/sbbdpt.o {oracle_home}/rdbms/lib/sbbdpt.o')
    os.popen(f'cp static/Oracle/bbedus.msb {oracle_home}/rdbms/mesg/bbedus.msb')
    print('3、需手工执行如下语句')
    print(f'cd {oracle_home}/rdbms/lib && make -f ins_rdbms.mk BBED={oracle_home}/bin/bbed {oracle_home}/bin/bbed')
    print('4、生成/home/oracle/par.txt')
    os.popen(f"echo 'blocksize=8192' > {home}/par.txt")
    os.popen(f"echo 'listfile=filelist.txt' >> {home}/par.txt")
    os.popen(f"echo 'mode=edit' >> {home}/par.txt")
    os.popen(f"echo 'spool=yes' >> {home}/par.txt")
    os.popen(f'cat {home}/par.txt')
    print('5、.bash_profile添加bbed环境变量')
    os.popen(f"""echo "alias bbed='bbed parfile=par.txt password=blockedit'" >> {home}/.bash_profile""")


"""
重建控制文件
"""


def recreate_controlfile():
    db_name = 'DB_NAME'
    flag = input("第一步，请输入db_name，可通过参数文件DB_NAME或BBED查询，BBED查询步骤请输入1：")
    if flag == '1':
        print("""
BBED> info
 File#  Name                                                        Size(blks)
 -----  ----                                                        ----------
     1  /u01/app/oracle/oradata/prod/system01.dbf                        96000
     2  /u01/app/oracle/oradata/prod/sysaux01.dbf                        96000
     3  /u01/app/oracle/oradata/prod/undotbs01.dbf                        8960
     4  /u01/app/oracle/oradata/prod/users01.dbf                           640

BBED> set file 1 block 1 
	FILE#          	1
	BLOCK#         	1

BBED> map /v 
 File: /u01/app/oracle/oradata/prod/system01.dbf (1)
 Block: 1                                     Dba:0x00400001
------------------------------------------------------------
 Data File Header

 struct kcvfh, 860 bytes                    @0       
    struct kcvfhbfh, 20 bytes               @0       
    struct kcvfhhdr, 76 bytes               @20      
    ub4 kcvfhrdb                            @96      
    struct kcvfhcrs, 8 bytes                @100     
    ub4 kcvfhcrt                            @108     
    ub4 kcvfhrlc                            @112     
    struct kcvfhrls, 8 bytes                @116     
    ub4 kcvfhbti                            @124     
    struct kcvfhbsc, 8 bytes                @128     
    ub2 kcvfhbth                            @136     
    ub2 kcvfhsta                            @138     
    struct kcvfhckp, 36 bytes               @484     
    ub4 kcvfhcpc                            @140     
    ub4 kcvfhrts                            @144     
    ub4 kcvfhccc                            @148     
    struct kcvfhbcp, 36 bytes               @152     
    ub4 kcvfhbhz                            @312     
    struct kcvfhxcd, 16 bytes               @316     
    sword kcvfhtsn                          @332     
    ub2 kcvfhtln                            @336     
    text kcvfhtnm[30]                       @338     
    ub4 kcvfhrfn                            @368     
    struct kcvfhrfs, 8 bytes                @372     
    ub4 kcvfhrft                            @380     
    struct kcvfhafs, 8 bytes                @384     
    ub4 kcvfhbbc                            @392     
    ub4 kcvfhncb                            @396     
    ub4 kcvfhmcb                            @400     
    ub4 kcvfhlcb                            @404     
    ub4 kcvfhbcs                            @408     
    ub2 kcvfhofb                            @412     
    ub2 kcvfhnfb                            @414     
    ub4 kcvfhprc                            @416     
    struct kcvfhprs, 8 bytes                @420     
    struct kcvfhprfs, 8 bytes               @428     
    ub4 kcvfhtrt                            @444     

 ub4 tailchk                                @8188    


BBED> p kcvfh
struct kcvfh, 860 bytes                     @0       
   struct kcvfhbfh, 20 bytes                @0       
      ub1 type_kcbh                         @0        0x0b
      ub1 frmt_kcbh                         @1        0xa2
      ub1 spare1_kcbh                       @2        0x00
      ub1 spare2_kcbh                       @3        0x00
      ub4 rdba_kcbh                         @4        0x00400001
      ub4 bas_kcbh                          @8        0x00000000
      ub2 wrp_kcbh                          @12       0x0000
      ub1 seq_kcbh                          @14       0x01
      ub1 flg_kcbh                          @15       0x04 (KCBHFCKV)
      ub2 chkval_kcbh                       @16       0xffc1
      ub2 spare3_kcbh                       @18       0x0000
   struct kcvfhhdr, 76 bytes                @20      
      ub4 kccfhswv                          @20       0x00000000
      ub4 kccfhcvn                          @24       0x0b200400
      ub4 kccfhdbi                          @28       0x1c510511
      text kccfhdbn[0]                      @32      P
      text kccfhdbn[1]                      @33      R
      text kccfhdbn[2]                      @34      O
      text kccfhdbn[3]                      @35      D
      text kccfhdbn[4]                      @36       
      text kccfhdbn[5]                      @37       
      text kccfhdbn[6]                      @38       
      text kccfhdbn[7]                      @39       
... ...
        """)
        db_name = input("请输入通过bbed方式查看出的DB_NAME值：")
    else:
        db_name = flag

    resetlogs = ''
    charset = ''
    flag_resetlogs = ''
    while flag_resetlogs not in ('1', '2'):
        flag_resetlogs = input("第二步，表示是否重置redo日志,日志损坏需要resetlogs(1、RESETLOGS/2、NORESETLOGS)输入对应数字：")
        if flag_resetlogs == '1':
            resetlogs = 'RESETLOGS'

            charset = 'charset'
            flag_char = input("输入字符集(比如AL32UTF8/ZHS16GBK)，通过BBED查看步骤请输入1：")
            if flag_char == '1':
                print(f"""
        select * from v$version;
        select distinct dbms_rowid.rowid_relative_fno(rowid) file#,dbms_rowid.rowid_block_number(rowid) block# from props$;
          FILE#     BLOCK#
        ---------- ----------
        	 1	  801

        dd if=/u01/app/oracle/oradata/prod/system01.dbf of=/tmp/props bs=8192 skip=801 count=1
        strings /tmp/props | more 
        NLS_CHARACTERSET
        AL32UTF8
        """)
            else:
                charset = flag_char

            print("###################################正式恢复步骤###################################")
            print("说明：1、数据库名PROD对应 参数文件中DB_NAME，或者去数据文件1号块头查看；2、resetlogs 如果日志文件丢失了，就要resetlogs，否则NORESETLOGS；")
            print(f"""步骤1、数据库启动到nomount使用如下语句创建controlfile,注意调整数据文件和控制文件数量和名称
        STARTUP NOMOUNT
        CREATE CONTROLFILE REUSE DATABASE "{db_name}" {resetlogs} ARCHIVELOG  
            MAXLOGFILES 16
            MAXLOGMEMBERS 3
            MAXDATAFILES 5000
            MAXINSTANCES 8
            MAXLOGHISTORY 292
        LOGFILE
          GROUP 1 '/u01/app/oracle/oradata/prod/redo01.log'  SIZE 50M BLOCKSIZE 512,
          GROUP 2 '/u01/app/oracle/oradata/prod/redo02.log'  SIZE 50M BLOCKSIZE 512,
          GROUP 3 '/u01/app/oracle/oradata/prod/redo03.log'  SIZE 50M BLOCKSIZE 512
        -- STANDBY LOGFILE
        DATAFILE
          '/u01/app/oracle/oradata/prod/system01.dbf',
          '/u01/app/oracle/oradata/prod/sysaux01.dbf',                
          '/u01/app/oracle/oradata/prod/undotbs01.dbf',
          '/u01/app/oracle/oradata/prod/users01.dbf'
        CHARACTER SET {charset};
        """)
            print("步骤2、resetlogs恢复数据库：RECOVER DATABASE USING BACKUP controlfile until cancel;")
            print("步骤3、打开数据库：alter database open resetlogs;")


        elif flag_resetlogs == '2':
            resetlogs = 'NORESETLOGS'

            charset = 'charset'
            flag_charset = input("输入字符集(比如AL32UTF8/ZHS16GBK)，通过BBED查看步骤请输入1查看：")
            if flag_charset == '1':
                print(f"""
        select * from v$version;
        select distinct dbms_rowid.rowid_relative_fno(rowid) file#,dbms_rowid.rowid_block_number(rowid) block# from props$;
          FILE#     BLOCK#
        ---------- ----------
        	 1	  801

        dd if=/u01/app/oracle/oradata/prod/system01.dbf of=/tmp/props bs=8192 skip=801 count=1
        strings /tmp/props | more 
        NLS_CHARACTERSET
        AL32UTF8
            """)
            else:
                charset = flag_charset

        print("###################################正式恢复步骤###################################")
        print("说明：1、数据库名PROD对应 参数文件中DB_NAME，或者去数据文件1号块头查看；2、resetlogs 如果日志文件丢失了，就要resetlogs，否则NORESETLOGS；")
        print(f"""步骤1、数据库启动到nomount使用如下语句创建controlfile,注意调整数据文件和控制文件数量和名称
        STARTUP NOMOUNT
        CREATE CONTROLFILE REUSE DATABASE "{db_name}" {resetlogs} ARCHIVELOG  
            MAXLOGFILES 16
            MAXLOGMEMBERS 3
            MAXDATAFILES 5000
            MAXINSTANCES 8
            MAXLOGHISTORY 292
        LOGFILE
          GROUP 1 '/u01/app/oracle/oradata/prod/redo01.log'  SIZE 500M BLOCKSIZE 512,
          GROUP 2 '/u01/app/oracle/oradata/prod/redo02.log'  SIZE 500M BLOCKSIZE 512,
          GROUP 3 '/u01/app/oracle/oradata/prod/redo03.log'  SIZE 500M BLOCKSIZE 512
        -- STANDBY LOGFILE
        DATAFILE
          '/u01/app/oracle/oradata/prod/system01.dbf',
          '/u01/app/oracle/oradata/prod/sysaux01.dbf',                
          '/u01/app/oracle/oradata/prod/undotbs01.dbf',
          '/u01/app/oracle/oradata/prod/users01.dbf'
        CHARACTER SET {charset};
        """)
        print("步骤2、noresetlogs手工恢复控制文件，需手工注册归档文件：alter database register physical logfile /arch/1.dbf;")
        print("或者批量注册：catalog start with '/arch/*.dbf';")
        print("步骤3、恢复数据库：recover database;")
        print("步骤4、所有redo归档：alter system archive log all;")
        print("步骤5、alter database open;")
        print("步骤6、增加临时文件：alter tablespace temp add tempfile '/****.dbf' size 10G autoextend on maxsize 30G;")
    print("数据库平时维护也需要定期备份控制文件，语句：alter database backup controlfile to trace as '/home/oracle/controlfile.sql';")


"""
system文件头损坏
"""


def block_header_repair():
    print("################BBED修复文件头主步骤如下：###############")
    print("0、模拟system表空间文件头损坏")
    print("1、rdba_kcbh(offset 4) 更改文件头block中记录的rdba地址")
    print("2、kccfhfsz(offset 44)  修复文件头中记录的文件大小")
    print("3、kccfhfno(offset 52) 修改datafile文件号")
    print("4、kcvfhrdb(offset 96) 修改root dba，只有system文件有root dba地址")
    print("5、kscnbas(offset 100) 修改1号文件创建时刻的scn，v$datafile.creation_change#")
    print("6、kcvfhcrt (offset 108) v$datafile.creation_time")
    print("7、kcvfhsta (offset 138) 修改文件状态")
    print("8、kcvfhtsn (offset 332) 修改表空间号v$datafile.ts#")
    print("9、kcvfhtIn (offset 336) 修改表空间名称字符长度")
    print("10、kcvfhtnm (offset 338) 修改表空间名称，取自v$tablespace.name")
    print("11、kcvfhrfn (offset 368) 修改文件头相对文件号，取自v$datafile.rfile#")
    print("12、kscnbas (offset 484) 修复文件头检查点scn，checkpoint scn")
    print("13、kcvcptim (offset 492) 修复文件头检查点时间，last checkpoint time")
    print("14、使用dbv校验块是否更改好")
    print("15、校验成功但报ORA-01207: file is more recent than control file - old control file错误")
    step = ''
    while step not in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15'):
        step = input("请输入对应数字查看每项具体操作步骤：")
        if step == '0':
            print("""
0、模拟system表空间文件头即file 1 block 1 损坏
BBED> info
 File#  Name                                                        Size(blks)
 -----  ----                                                        ----------
     1  /u01/app/oracle/oradata/prod/system01.dbf                        96000
     2  /u01/app/oracle/oradata/prod/sysaux01.dbf                        96000
     3  /u01/app/oracle/oradata/prod/undotbs01.dbf                        8960
     4  /u01/app/oracle/oradata/prod/users01.dbf                           640

BBED> copy file 4 block 10 to file 1 block 1
 File: /u01/app/oracle/oradata/prod/system01.dbf (1)
 Block: 1                Offsets:    0 to  511           Dba:0x00400001
------------------------------------------------------------------------
 1ea20000 0a000001 203f0000 00000104 a6010000 04000000 80403600 00000000 
 00000000 00f80000 00000000 00000000 00000000 00000000 00000000 00000000 
 00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000000 
 00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000000 
 00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000000 
 00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000000 
 00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000000 
 00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000000 
 00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000000 
 00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000000 
 00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000000 
 00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000000 
 00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000000 
 00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000000 
 00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000000 
 00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000000 

 <32 bytes per line>

BBED> sum apply
Check value for File 1, Block 1:
current = 0x01a6, required = 0x01a6

BBED> set file 1 block 1 
	FILE#          	1
	BLOCK#         	1

BBED> map /v 
 File: /u01/app/oracle/oradata/prod/system01.dbf (1)
 Block: 1                                     Dba:0x00400001
------------------------------------------------------------
BBED-00400: invalid blocktype (30)

说明：数据库此时无法启动，因为open时要往数据文件头块写检查点信息
            """)
        elif step == '1':
            print("""
第一步、拷贝其他数据文件头到system表空间文件头
BBED> set file 2 block 1 
	FILE#          	2
	BLOCK#         	1

BBED> map /v 
 File: /u01/app/oracle/oradata/prod/sysaux01.dbf (2)
 Block: 1                                     Dba:0x00800001
------------------------------------------------------------
 Data File Header

 struct kcvfh, 860 bytes                    @0       
    struct kcvfhbfh, 20 bytes               @0       
    struct kcvfhhdr, 76 bytes               @20      
    ub4 kcvfhrdb                            @96      
    struct kcvfhcrs, 8 bytes                @100     
    ub4 kcvfhcrt                            @108     
    ub4 kcvfhrlc                            @112     
    struct kcvfhrls, 8 bytes                @116     
    ub4 kcvfhbti                            @124     
    struct kcvfhbsc, 8 bytes                @128     
    ub2 kcvfhbth                            @136     
    ub2 kcvfhsta                            @138     
    struct kcvfhckp, 36 bytes               @484     
    ub4 kcvfhcpc                            @140     
    ub4 kcvfhrts                            @144     
    ub4 kcvfhccc                            @148     
    struct kcvfhbcp, 36 bytes               @152     
    ub4 kcvfhbhz                            @312     
    struct kcvfhxcd, 16 bytes               @316     
    sword kcvfhtsn                          @332     
    ub2 kcvfhtln                            @336     
    text kcvfhtnm[30]                       @338     
    ub4 kcvfhrfn                            @368     
    struct kcvfhrfs, 8 bytes                @372     
    ub4 kcvfhrft                            @380     
    struct kcvfhafs, 8 bytes                @384     
    ub4 kcvfhbbc                            @392     
    ub4 kcvfhncb                            @396     
    ub4 kcvfhmcb                            @400     
    ub4 kcvfhlcb                            @404     
    ub4 kcvfhbcs                            @408     
    ub2 kcvfhofb                            @412     
    ub2 kcvfhnfb                            @414     
    ub4 kcvfhprc                            @416     
    struct kcvfhprs, 8 bytes                @420     
    struct kcvfhprfs, 8 bytes               @428     
    ub4 kcvfhtrt                            @444     

 ub4 tailchk                                @8188    


BBED> copy file 2 block 1 to file 1 block 1 
Warning: contents of previous BIFILE will be lost. Proceed? (Y/N) Y
 File: /u01/app/oracle/oradata/prod/system01.dbf (1)
 Block: 1                Offsets:    0 to  511           Dba:0x00400001
------------------------------------------------------------------------
 0ba20000 01008000 00000000 00000104 22a70000 00000000 0004200b 1105511c 
 50524f44 00000000 792e0000 00810100 00200000 02000300 00000000 00000000 
 00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000000 
 00000000 2a070000 00000000 81c92131 145d7c3f d5dc1e00 00000000 00000000 
 00000000 00000000 00000400 95000000 9ea0783f 94000000 00000000 00000000 
 00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000000 
 00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000000 
 00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000000 
 00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000000 
 00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000000 
 00000000 00000000 00000000 01000000 06005359 53415558 00000000 00000000 
 00000000 00000000 00000000 00000000 02000000 00000000 00000000 00000000 
 00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000000 
 93a75f3f 06200e00 00000000 00000000 00000000 00000000 00000000 00000000 
 00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000000 
 00000000 dfde1e00 00000000 555d7c3f 01000000 0a000000 73010000 10000000 

 <32 bytes per line>

BBED> sum apply
Check value for File 1, Block 1:
current = 0xa722, required = 0xa722

BBED> set file 1 block 1 
	FILE#          	1
	BLOCK#         	1

BBED> map /v 
 File: /u01/app/oracle/oradata/prod/system01.dbf (1)
 Block: 1                                     Dba:0x00400001
------------------------------------------------------------
 Data File Header

 struct kcvfh, 860 bytes                    @0       
    struct kcvfhbfh, 20 bytes               @0       
    struct kcvfhhdr, 76 bytes               @20      
    ub4 kcvfhrdb                            @96      
    struct kcvfhcrs, 8 bytes                @100     
    ub4 kcvfhcrt                            @108     
    ub4 kcvfhrlc                            @112     
    struct kcvfhrls, 8 bytes                @116     
    ub4 kcvfhbti                            @124     
    struct kcvfhbsc, 8 bytes                @128     
    ub2 kcvfhbth                            @136     
    ub2 kcvfhsta                            @138     
    struct kcvfhckp, 36 bytes               @484     
    ub4 kcvfhcpc                            @140     
    ub4 kcvfhrts                            @144     
    ub4 kcvfhccc                            @148     
    struct kcvfhbcp, 36 bytes               @152     
    ub4 kcvfhbhz                            @312     
    struct kcvfhxcd, 16 bytes               @316     
    sword kcvfhtsn                          @332     
    ub2 kcvfhtln                            @336     
    text kcvfhtnm[30]                       @338     
    ub4 kcvfhrfn                            @368     
    struct kcvfhrfs, 8 bytes                @372     
    ub4 kcvfhrft                            @380     
    struct kcvfhafs, 8 bytes                @384     
    ub4 kcvfhbbc                            @392     
    ub4 kcvfhncb                            @396     
    ub4 kcvfhmcb                            @400     
    ub4 kcvfhlcb                            @404     
    ub4 kcvfhbcs                            @408     
    ub2 kcvfhofb                            @412     
    ub2 kcvfhnfb                            @414     
    ub4 kcvfhprc                            @416     
    struct kcvfhprs, 8 bytes                @420     
    struct kcvfhprfs, 8 bytes               @428     
    ub4 kcvfhtrt                            @444     

 ub4 tailchk                                @8188    

第二步、计算更改并更改rdba地址
BBED> set file 1 block 1 
... ...
BBED> map  /v 
... ...
BBED> p kcvfhbfh
struct kcvfhbfh, 20 bytes                   @0       
   ub1 type_kcbh                            @0        0x0b
   ub1 frmt_kcbh                            @1        0xa2
   ub1 spare1_kcbh                          @2        0x00
   ub1 spare2_kcbh                          @3        0x00
   ub4 rdba_kcbh                            @4        0x00800001
... ... 
说明：0x00800001为16进制，前10bit为文件号，后22bit为块号
00800001，二进制为0000 0000 1000 0000 0000 0000 0000 0001，2号文件1号块
00400001，二进制为0000 0000 0100 0000 0000 0000 0000 0001，1号文件1号块
select 
dbms_utility.data_block_address_file(to_number('800001','XXXXXXXX')) file_id,
dbms_utility.data_block_address_block(to_number('800001','XXXXXXXX')) block_id 
from dual;

BBED> set file 1 block 1 offset 4 count 32
	FILE#          	1
	BLOCK#         	1
	OFFSET         	4
	COUNT          	32

BBED> dump
 File: /u01/app/oracle/oradata/prod/system01.dbf (1)
 Block: 1                Offsets:    4 to   35           Dba:0x00400001
------------------------------------------------------------------------
 01008000 00000000 00000104 22a70000 00000000 0004200b 1105511c 50524f44 

 <32 bytes per line>

BBED> modify /x 01004000 offset 4 
 File: /u01/app/oracle/oradata/prod/system01.dbf (1)
 Block: 1                Offsets:    4 to   35           Dba:0x00400001
------------------------------------------------------------------------
 01004000 00000000 00000104 22a70000 00000000 0004200b 1105511c 50524f44 

 <32 bytes per line>

BBED> sum apply 
Check value for File 1, Block 1:
current = 0xa7e2, required = 0xa7e2

            """)
        elif step == '2':
            print("""
第二步、修复文件头中记录的文件大小
[oracle@VM-0-3-centos prod]$ ls -l | grep system
-rw-r----- 1 oracle oinstall 786440192 Feb 21 19:06 system01.dbf

select to_char((786440192-8192)/8192,'XXXXXXXXXXXXXXXXXXXXXXX') from dual;

TO_CHAR((786440192-8192)
------------------------
		   17700

17700为16进制，00 01 77 00 倒过来为，00770100 
BBED> set file 1 block 1 offset 44 count 32 
	FILE#          	1
	BLOCK#         	1
	OFFSET         	44
	COUNT          	32

BBED> dump
 File: /u01/app/oracle/oradata/prod/system01.dbf (1)
 Block: 1                Offsets:   44 to   75           Dba:0x00400001
------------------------------------------------------------------------
 00810100 00200000 02000300 00000000 00000000 00000000 00000000 00000000 

 <32 bytes per line>

BBED> modify /x 00770100
Warning: contents of previous BIFILE will be lost. Proceed? (Y/N) Y
 File: /u01/app/oracle/oradata/prod/system01.dbf (1)
 Block: 1                Offsets:   44 to   75           Dba:0x00400001
------------------------------------------------------------------------
 00770100 00200000 02000300 00000000 00000000 00000000 00000000 00000000 

 <32 bytes per line>

BBED> sum apply 
Check value for File 1, Block 1:
current = 0x51e2, required = 0x51e2
            """)
        elif step == '3':
            print("""
第一步、修改偏移量offset 52位置datafile文件号

BBED> p offset 52 
kcvfh.kcvfhhdr.kccfhfno
-----------------------
ub2 kccfhfno                                @52       0x0002

BBED> dump
 File: /u01/app/oracle/oradata/prod/system01.dbf (1)
 Block: 1                Offsets:   52 to   83           Dba:0x00400001
------------------------------------------------------------------------
 02000300 00000000 00000000 00000000 00000000 00000000 00000000 00000000 

 <32 bytes per line>

BBED> modify /x 01
 File: /u01/app/oracle/oradata/prod/system01.dbf (1)
 Block: 1                Offsets:   52 to   83           Dba:0x00400001
------------------------------------------------------------------------
 01000300 00000000 00000000 00000000 00000000 00000000 00000000 00000000 

 <32 bytes per line>

BBED> sum apply
Check value for File 1, Block 1:
current = 0x51e1, required = 0x51e1
            """)
        elif step == '4':
            print("""
步骤一、计算修改值，修改root dba地址，只有system有root dba地址           
select to_char((select fhrdb from x$kcvfh where fhfno = 1),'XXXXXXXXXXXXXXXXXX') from dual;

TO_CHAR((SELECTFHRD
-------------------
       400208

select 
dbms_utility.data_block_address_file(to_number('400208','XXXXXXXX')) file_id,
dbms_utility.data_block_address_block(to_number('400208','XXXXXXXX')) block_id 
from dual;

   FILE_ID   BLOCK_ID
---------- ----------
        1    520
位于1号文件520号块上

select to_char(520,'XXXXXX') from dual;

TO_CHAR
-------
    208
16进制带上1号文件就是 00400208 ，后面是二进制 0000 0000 0100 0000 0000 0010 0000 1000      

步骤二、下面正式修改
BBED> p kcvfhrdb
ub4 kcvfhrdb                                @96       0x00000000

BBED> set file 1 block 1 offset 96 count 32
	FILE#          	1
	BLOCK#         	1
	OFFSET         	96
	COUNT          	32

BBED> dump
 File: /u01/app/oracle/oradata/prod/system01.dbf (1)
 Block: 1                Offsets:   96 to  127           Dba:0x00400001
------------------------------------------------------------------------
 00000000 2a070000 00000000 81c92131 145d7c3f d5dc1e00 00000000 00000000 

 <32 bytes per line>

BBED> modify /x 08024000
 File: /u01/app/oracle/oradata/prod/system01.dbf (1)
 Block: 1                Offsets:   96 to  127           Dba:0x00400001
------------------------------------------------------------------------
 08024000 2a070000 00000000 81c92131 145d7c3f d5dc1e00 00000000 00000000 

 <32 bytes per line>

BBED> sum apply
Check value for File 1, Block 1:
current = 0x53a9, required = 0x53a9

BBED> dump
 File: /u01/app/oracle/oradata/prod/system01.dbf (1)
 Block: 1                Offsets:   96 to  127           Dba:0x00400001
------------------------------------------------------------------------
 08024000 2a070000 00000000 81c92131 145d7c3f d5dc1e00 00000000 00000000 

 <32 bytes per line>     
            """)
        elif step == '5':
            print("""
修改1号文件创建时刻的scn
数据库启动到mount，从控制文件中读取file 1 创建时间scn，如下为7
SQL> select file#,creation_change# from v$datafile;

     FILE# CREATION_CHANGE#
---------- ----------------
	 1		      7
	 2	       1834
	 3	     923328
	 4	      16143

SQL> select to_char('1834','XXXXXXXXXX') from dual;

TO_CHAR('18
-----------
	72A
第二步、讲creation scn 改为7，72A为2号文件创建时到scn，需要将其替换掉

BBED> p kcvfhcrs
struct kcvfhcrs, 8 bytes                    @100     
   ub4 kscnbas                              @100      0x0000072a
   ub2 kscnwrp                              @104      0x0000

BBED> set file 1 block 1 offset 100 count 32
	FILE#          	1
	BLOCK#         	1
	OFFSET         	100
	COUNT          	32

BBED> dump
 File: /u01/app/oracle/oradata/prod/system01.dbf (1)
 Block: 1                Offsets:  100 to  131           Dba:0x00400001
------------------------------------------------------------------------
 2a070000 00000000 81c92131 145d7c3f d5dc1e00 00000000 00000000 00000000 

 <32 bytes per line>

BBED> modify /x 07000000 offset 100
Warning: contents of previous BIFILE will be lost. Proceed? (Y/N) Y
 File: /u01/app/oracle/oradata/prod/system01.dbf (1)
 Block: 1                Offsets:  100 to  131           Dba:0x00400001
------------------------------------------------------------------------
 07000000 00000000 81c92131 145d7c3f d5dc1e00 00000000 00000000 00000000 

 <32 bytes per line>

BBED> sum apply
Check value for File 1, Block 1:
current = 0x5484, required = 0x5484

BBED> dump
 File: /u01/app/oracle/oradata/prod/system01.dbf (1)
 Block: 1                Offsets:  100 to  131           Dba:0x00400001
------------------------------------------------------------------------
 07000000 00000000 81c92131 145d7c3f d5dc1e00 00000000 00000000 00000000 

 <32 bytes per line>
            """)
        elif step == '6':
            print("""
修复文件头创建时间，从控制文件中读取1号文件创建时的时间:
数据库启动到mount，然后进行查询
select file#,
to_char(creation_time,'yyyy-mm-dd hh24:mi:ss') creation_time_file,
(to_char(creation_time,'yyyy') - 1988) *12*31*24*3600 +
(to_char(creation_time,'mm') - 1) *31*24*3600 +
(to_char(creation_time,'dd') - 1) *24*3600 +
to_char(creation_time,'hh24') *3600 +
to_char(creation_time,'mi') *60 +
to_char(creation_time,'ss') creation_time_scn 
from v$datafile order by 1; 

     FILE# CREATION_TIME_FILE  CREATION_TIME_SCN
---------- ------------------- -----------------
	 1 2013-08-24 11:37:33	       824297853
	 2 2013-08-24 11:37:37	       824297857
	 3 2013-08-24 12:07:19	       824299639
	 4 2013-08-24 11:37:49	       824297869
将1号文件创建时的scn转换为16进制
SQL> select to_char(824297853,'XXXXXXXXXXX') from dual;

TO_CHAR(8242
------------
    3121C97D

第二步、正式修改
BBED> set file 1 block 1 offset 108 count 32
	FILE#          	1
	BLOCK#         	1
	OFFSET         	108
	COUNT          	32

BBED> p kcvfhcrt
ub4 kcvfhcrt                                @108      0x3121c981

BBED> modify /x 7DC92131 offset 108
Warning: contents of previous BIFILE will be lost. Proceed? (Y/N) Y
 File: /u01/app/oracle/oradata/prod/system01.dbf (1)
 Block: 1                Offsets:  108 to  139           Dba:0x00400001
------------------------------------------------------------------------
 7dc92131 145d7c3f d5dc1e00 00000000 00000000 00000000 00000000 00000400 

 <32 bytes per line>
 
BBED> sum apply
Check value for File 1, Block 1:
current = 0x5478, required = 0x5478
            """)
        elif step == '7':
            print("""
#define KCVFHHBP 0x01 /*hotbackup-in-process on file(fuzzy file)*/
#define KCVFHOFZ 0x04 /*Online Fuzzy because it was online and db open*/
#define KCVFHMFZ 0x10 /*Media recovery Fuzzy -file in media recovery*/
#define KCVFHAFZ 0x40 /*Absolutely Fuzzy -fuzzyness from file scan */
当一个datafile处于fuzzy模糊状态的时候，其kcvfhsta为0x04
BBED> p offset 138
kcvfh.kcvfhsta
--------------
ub2 kcvfhsta                                @138      0x0004 (KCVFHOFZ)

BBED> set file 1 block 1 offset 138 count 32
	FILE#          	1
	BLOCK#         	1
	OFFSET         	138
	COUNT          	32

BBED> dump
 File: /u01/app/oracle/oradata/prod/system01.dbf (1)
 Block: 1                Offsets:  138 to  169           Dba:0x00400001
------------------------------------------------------------------------
 04009500 00009ea0 783f9400 00000000 00000000 00000000 00000000 00000000 

 <32 bytes per line>
            """)
        elif step == '8':
            print("""
更改表空间号，1号文件对应0号表空间
SQL> select file#,ts# from v$datafile;

     FILE#	  TS#
---------- ----------
	 1	    0
	 2	    1
	 3	    2
	 4	    4
查询得知1号文件对应0号表空间号，按照下面步骤修改
BBED> p kcvfhtsn
sword kcvfhtsn                              @332      1

BBED> set file 1 block 1 offset 332 count 32
	FILE#          	1
	BLOCK#         	1
	OFFSET         	332
	COUNT          	32

BBED> dump
 File: /u01/app/oracle/oradata/prod/system01.dbf (1)
 Block: 1                Offsets:  332 to  363           Dba:0x00400001
------------------------------------------------------------------------
 01000000 06005359 53415558 00000000 00000000 00000000 00000000 00000000 

 <32 bytes per line>

BBED> modify /x 00 offset 332
 File: /u01/app/oracle/oradata/prod/system01.dbf (1)
 Block: 1                Offsets:  332 to  363           Dba:0x00400001
------------------------------------------------------------------------
 00000000 06005359 53415558 00000000 00000000 00000000 00000000 00000000 

 <32 bytes per line>

BBED> sum apply
Check value for File 1, Block 1:
current = 0x5479, required = 0x5479
            """)
        elif step == '9':
            print("""
SYSTEM和SYSAUX长度一样,所以不修改了
BBED> p offset 336 
pad
---
ub1 pad                                     @336      0x06

BBED> p kcvfhtln
ub2 kcvfhtln                                @336      0x0006

BBED> p kcvfhtnm
text kcvfhtnm[0]                            @338     S
text kcvfhtnm[1]                            @339     Y
text kcvfhtnm[2]                            @340     S
text kcvfhtnm[3]                            @341     A
text kcvfhtnm[4]                            @342     U
text kcvfhtnm[5]                            @343     X
text kcvfhtnm[6]                            @344      
text kcvfhtnm[7]                            @345      
text kcvfhtnm[8]                            @346      
text kcvfhtnm[9]                            @347  
            """)
        elif step == '10':
            print("""
修改文件头记录的表空间名称
SQL> select dump('SYSTEM', 16) from dual;

DUMP('SYSTEM',16)
-------------------------------
Typ=96 Len=6: 53,59,53,54,45,4d

BBED> set file 1 block 1 offset 338 count 32
	FILE#          	1
	BLOCK#         	1
	OFFSET         	338
	COUNT          	32

BBED> dump
 File: /u01/app/oracle/oradata/prod/system01.dbf (1)
 Block: 1                Offsets:  338 to  369           Dba:0x00400001
------------------------------------------------------------------------
 53595341 55580000 00000000 00000000 00000000 00000000 00000000 00000200 

 <32 bytes per line>
 
BBED> p kcvfhtnm
text kcvfhtnm[0]                            @338     S
text kcvfhtnm[1]                            @339     Y
text kcvfhtnm[2]                            @340     S
text kcvfhtnm[3]                            @341     A
text kcvfhtnm[4]                            @342     U
text kcvfhtnm[5]                            @343     X

BBED> dump offset 338 count 32
 File: /u01/app/oracle/oradata/prod/system01.dbf (1)
 Block: 1                Offsets:  338 to  369           Dba:0x00400001
------------------------------------------------------------------------
 53595341 55580000 00000000 00000000 00000000 00000000 00000000 00000200 

 <32 bytes per line>

BBED> modify /x 53 offset 338
Warning: contents of previous BIFILE will be lost. Proceed? (Y/N) Y
 File: /u01/app/oracle/oradata/prod/system01.dbf (1)
 Block: 1                Offsets:  338 to  369           Dba:0x00400001
------------------------------------------------------------------------
 53595341 55580000 00000000 00000000 00000000 00000000 00000000 00000200 

 <32 bytes per line>

BBED> modify /x 54454d offset 341
 File: /u01/app/oracle/oradata/prod/system01.dbf (1)
 Block: 1                Offsets:  341 to  372           Dba:0x00400001
------------------------------------------------------------------------
 54454d00 00000000 00000000 00000000 00000000 00000000 00000002 00000000 

 <32 bytes per line>

BBED> sum apply
Check value for File 1, Block 1:
current = 0x5469, required = 0x5469

BBED> p kcvfhtnm
text kcvfhtnm[0]                            @338     S
text kcvfhtnm[1]                            @339     Y
text kcvfhtnm[2]                            @340     S
text kcvfhtnm[3]                            @341     T
text kcvfhtnm[4]                            @342     E
text kcvfhtnm[5]                            @343     M
            """)
        elif step == '11':
            print("""
通过下面sql查询相对文件号：
SQL> select file#,rfile# from v$datafile;

     FILE#     RFILE#
---------- ----------
	 1	    1
	 2	    2
	 3	    3
	 4	    4
	 
BBED> set file 1 block 1 offset 368 count 32
	FILE#          	1
	BLOCK#         	1
	OFFSET         	368
	COUNT          	32

BBED> dump
 File: /u01/app/oracle/oradata/prod/system01.dbf (1)
 Block: 1                Offsets:  368 to  399           Dba:0x00400001
------------------------------------------------------------------------
 02000000 00000000 00000000 00000000 00000000 00000000 00000000 00000000 

 <32 bytes per line>
 
 BBED> modify /x 01 
Warning: contents of previous BIFILE will be lost. Proceed? (Y/N) Y
 File: /u01/app/oracle/oradata/prod/system01.dbf (1)
 Block: 1                Offsets:  368 to  399           Dba:0x00400001
------------------------------------------------------------------------
 01000000 00000000 00000000 00000000 00000000 00000000 00000000 00000000 

 <32 bytes per line>

BBED> sum apply
Check value for File 1, Block 1:
current = 0x546a, required = 0x546a
            """)
        elif step == '12':
            print("""
通过下面sql查询控制文件中记录的1号文件的checkpoint_change#
select file#,creation_change#,checkpoint_change#,unrecoverable_change#,last_change#,offline_change#
from v$datafile order by 1

     FILE# CREATION_CHANGE# CHECKPOINT_CHANGE# UNRECOVERABLE_CHANGE# LAST_CHANGE# OFFLINE_CHANGE#
---------- ---------------- ------------------ --------------------- ------------ ---------------
	    1   		      7	           2023135			           0			          2022612
	    2	           1834	           2023135			           0			          2022612
	    3	         923328	           2023135			           0			          2022612
	    4	          16143	           2023135			           0			          2022612

SQL> select to_char(2023135,'XXXXXXXXXXXXXXXXXX') from dual;

TO_CHAR(2023135,'XX
-------------------
	     1EDEDF
	     
下面是进行修改scn的步骤，不修改的话，如果归档完整，直接recover datafile 1 也可以
BBED> set file 1 block 1 offset 484 count 32
	FILE#          	1
	BLOCK#         	1
	OFFSET         	484
	COUNT          	32

BBED> modify /x dfde1e offset 484
Warning: contents of previous BIFILE will be lost. Proceed? (Y/N) Y
 File: /u01/app/oracle/oradata/prod/system01.dbf (1)
 Block: 1                Offsets:  484 to  515           Dba:0x00400001
------------------------------------------------------------------------
 dfde1e00 00000000 555d7c3f 01000000 0a000000 73010000 10000000 02000000 

 <32 bytes per line>

BBED> sum apply
Check value for File 1, Block 1:
current = 0x546a, required = 0x546a

BBED> dump
 File: /u01/app/oracle/oradata/prod/system01.dbf (1)
 Block: 1                Offsets:  484 to  515           Dba:0x00400001
------------------------------------------------------------------------
 dfde1e00 00000000 555d7c3f 01000000 0a000000 73010000 10000000 02000000 

 <32 bytes per line>
            """)
        elif step == '13':
            print("""
查询控制文件中记录scn值，此值与12一样，不修改应用归档日志也是可以自动修复的
select file#,
to_char(checkpoint_time,'yyyy-mm-dd hh24:mi:ss') checkpoint_time_file,
(to_char(checkpoint_time,'yyyy') - 1988) *12*31*24*3600 +
(to_char(checkpoint_time,'mm') - 1) *31*24*3600 +
(to_char(checkpoint_time,'dd') - 1) *24*3600 +
to_char(checkpoint_time,'hh24') *3600 +
to_char(checkpoint_time,'mi') *60 +
to_char(checkpoint_time,'ss') checkpoint_time_scn 
from v$datafile order by 1; 
     FILE# CHECKPOINT_TIME_FIL CHECKPOINT_TIME_SCN
---------- ------------------- -------------------
	    1  2021-02-21 17:16:05		1065114965
	    2  2021-02-21 17:16:05		1065114965
	    3  2021-02-21 17:16:05		1065114965
	    4  2021-02-21 17:16:05		1065114965

SQL> select to_char(1065114965,'XXXXXXXXXXXXXX') from dual;

TO_CHAR(1065114
---------------
       3F7C5D55

 File: /u01/app/oracle/oradata/prod/system01.dbf (1)
 Block: 1                Offsets:  492 to  523           Dba:0x00400001
------------------------------------------------------------------------
 555d7c3f 01000000 0a000000 73010000 10000000 02000000 00000000 00000000 

 <32 bytes per line>

BBED> modify /x 555d7c3f offset 492
Warning: contents of previous BIFILE will be lost. Proceed? (Y/N) Y
 File: /u01/app/oracle/oradata/prod/system01.dbf (1)
 Block: 1                Offsets:  492 to  523           Dba:0x00400001
------------------------------------------------------------------------
 555d7c3f 01000000 0a000000 73010000 10000000 02000000 00000000 00000000 

 <32 bytes per line>

BBED> sum apply
Check value for File 1, Block 1:
current = 0x546a, required = 0x546a
            """)
        elif step == '14':
            print("""
使用dbv校验块是否更改好
dbv file=/u01/app/oracle/oradata/prod/system01.dbf start=1 end=2

DBVERIFY: Release 11.2.0.4.0 - Production on Mon Feb 22 14:49:42 2021

Copyright (c) 1982, 2011, Oracle and/or its affiliates.  All rights reserved.

DBVERIFY - Verification starting : FILE = /u01/app/oracle/oradata/prod/system01.dbf


DBVERIFY - Verification complete

Total Pages Examined         : 2
Total Pages Processed (Data) : 0
Total Pages Failing   (Data) : 0
Total Pages Processed (Index): 0
Total Pages Failing   (Index): 0
Total Pages Processed (Other): 2
Total Pages Processed (Seg)  : 0
Total Pages Failing   (Seg)  : 0
Total Pages Empty            : 0
Total Pages Marked Corrupt   : 0
Total Pages Influx           : 0
Total Pages Encrypted        : 0
Highest block SCN            : 1225671 (0.1225671)
            """)
        elif step == '15':
            print("""
如果校验成功但是报 ORA-01207: file is more recent than control file - old control file错误
方法一：手工创建控制文件
方法二：修改checkpoint count
kcvfhcpc (offset 144) Datafile checkpoint count
kcvfhccc (offset 148) Controlfile Checkpoint Count

BBED> p kcvfhcpc
ub4 kcvfhcpc                                @140      0x00000098

BBED> p kcvfhccc
ub4 kcvfhccc                                @148      0x00000097
正确的值：数据文件中记录的要比控制文件中记录的值相等，或大于1，在更新scn的时候要把文件头计数器原来的值拷贝到控制文件
然后再加1，所以数据文件头的值要比控制文件大1
            """)


"""
跳过归档恢复
"""


def archive():
    print("""
场景：在做恢复的时候，发现丢失部分归档日志，无法正常恢复，使用bbed跳过归档    
    """)


archive()

"""
坏块处理
"""


def block_recovery():
    print("物理坏块：通常是由于硬件损坏如磁盘异常导致，内存有问题、存储链路有问题、IO问题、文件系统有问题、Oracle本身问题等。")
    print("逻辑坏块：可能都是软件问题导致通常是由于Oracle bug导致，比如data block和index block数据不一致")


def undo():
    print("Undo回滚段作用：1、事务回滚；2、实例恢复,利用回滚来恢复未提交的数据；3、读一致性，构造CR块；4、数据库闪回查询；5、数据库闪回恢复逻辑错误")
    print("深入理解Oracle中事务：")
    print("undo段头块深入理解：")
    print("undo块深入解析")
    print("深入理解Oracle的回滚操作：")
    print("读一致性(构造CR)：")
    print("为什么我的undo不够了--Undo段内部重用规则：")
    print("undo表空间的大小估算以及创建：")
