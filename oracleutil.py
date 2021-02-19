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
def bbed():
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
    print("|----------------------------1、第一步安装bbed----------------------------------------------|")
    os.popen(f'cp static/Oracle/ssbbded.o {oracle_home}/rdbms/lib/ssbbded.o')
    os.popen(f'cp static/Oracle/sbbdpt.o {oracle_home}/rdbms/lib/sbbdpt.o')
    os.popen(f'cp static/Oracle/bbedus.msb {oracle_home}/rdbms/mesg/bbedus.msb')
    os.popen(f'cd {oracle_home}/rdbms/lib && /bin/make -f ins_rdbms.mk BBED={oracle_home}/bin/bbed')
    print("|----------------------------1、bbed安装结束----------------------------------------------|")
    os.popen(f"echo 'blocksize=8192' > {home}/par.txt")
    os.popen(f"echo 'listfile=filelist.txt' >> {home}/par.txt")
    os.popen(f"echo 'mode=edit' >> {home}/par.txt")
    os.popen(f"echo 'spool=yes' >> {home}/par.txt")
    print("")
    os.popen(f"""echo "alias bbed='bbed parfile=par.txt password=blockedit'" >> {home}/.bash_profile""")
