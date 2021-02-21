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
            print(f"""
        说明：1、数据库名PROD对应 参数文件中DB_NAME，或者去数据文件1号块头查看；2、resetlogs 如果日志文件丢失了，就要resetlogs，否则NORESETLOGS；
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
        CHARACTER SET {charset}	;
        """)

            print("noresetlogs手工恢复控制文件，需手工注册归档文件：alter database register physical logfile /arch/1.dbf;")
            print("或者批量注册：catalog start with '/arch/*.dbf';")
            print("恢复数据库：recover database;")
            print("所有redo归档：alter system archive log all;")
            print("alter database open;")
            print("增加临时文件：alter tablespace temp add tempfile '/****.dbf' size 10G autoextend on maxsize 30G;")

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
        print(f"""步骤1、数据库启动到nomount使用如下语句创建controlfile
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
        CHARACTER SET {charset}	;
        """)
        print("步骤2、resetlogs恢复数据库：RECOVER DATABASE USING BACKUP controlfile until cancel;")
        print("步骤3、打开数据库：alter database open resetlogs;")
    print("备份控制文件语句：alter database backup controlfile to trace as '/home/oracle/controlfile.sql';")


"""
system文件头损坏
"""


def system_block_header():
    print("#")
    print("################BBED修复文件头主步骤如下：###############")
    print("1、rdba_kcbh(offset 4) 文件头block的rdba地址")
    print("2、kccfhfsz(offset 44) 文件大小")
    print("3、kccfhfno(offset 52) datafile文件号")
    print("4、kcvfhrdb(offset 96) root dba")
    print("5、kscnbas(offset 100) v$datafile.creation_change#")
    print("6、kcvfhcrt (offset 108) v$datafile.creation_time")
    print("7、kcvfhsta (offset 138) 文件状态")
    print("8、kcvfhtsn (offset 332) 表空间号v$datafile.ts#")
    print("9、kcvfhtIn (offset 336) 表空间名称字符长度")
    print("10、kcvfhtnm (offset 338) 表空间名称v$tablespace.name")
    print("11、kcvfhrfn (offset 368) 相对文件号v$datafile.rfile#")
    print("12、kscnbas (offset 484) checkpoint scn")
    print("13、kcvcptim (offset 492) last checkpoint time")
    print("14、kcvfhcpc (offset 144) Datafile checkpoint count")
    step = input("请输入对应数字查看每项具体操作步骤：")
    if step == '1':
        pass
    elif step == '2':
        pass
    elif step == '3':
        pass
    elif step == '4':
        pass
    elif step == '5':
        pass
    elif step == '6':
        pass
    elif step == '7':
        pass
    elif step == '8':
        pass
    elif step == '9':
        pass
    elif step == '10':
        pass
    elif step == '11':
        pass
    elif step == '12':
        pass


# system_block_header()



def block_recovery():
    pass