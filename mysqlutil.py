#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2021/1/19 下午3:33
# @Author  : yaochong/Chongzi
# @FileName: mysqlutil.py
# @Software: PyCharm
# @Blog    ：https://github.com/yaochong-06/ ; http://blog.itpub.net/29990276

"""
split -b 90m mysql-5.7.30-linux-glibc2.12-x86_64.tar.gz mysqlsplit
"""
import os
from data import remove_last_line
import time

"""
MySQL5.7安装
"""


##############################################################################################
# "Please Copy This File and mysql-5.7.30-linux-glibc2.12-x86_64.tar.gz Package to /usr/local"#
##############################################################################################

def mysql57install():
    print("|----------------------------------------------------------------------------------------------|")
    print("|本安装为Linux标准二进制安装，请将MySQL的tar.gz安装包放置/usr/local目录下，请用root用户执行安装|")
    print("|例如：/usr/local/mysql-5.7.30-linux-glibc2.12-x86_64.tar.gz                                   |")
    print("|----------------------------------------------------------------------------------------------|")
    name = input("|请输入安装包名称，比如：mysql-5.7.30-linux-glibc2.12-x86_64(不带.tar.gz)：")
    print("|----------------------------------------------------------------------------------------------|")
    print("|Step1、生成/etc/my.cnf文件...")
    os.system("cp static/MySQL/my.cnf /etc/my.cnf && chmod 755 /etc/my.cnf")
    print("|----------------------------------------------------------------------------------------------|")
    print('|Step2、MySQL系统用户添加...')
    os.popen("groupadd mysql && useradd -r -g mysql mysql", 'r', 100)
    print("|----------------------------------------------------------------------------------------------|")
    print('|Step3、创建MySQL系统目录...')
    os.system(
        "mkdir -p /data/undolog /data/redolog /data/mysql_data mkdir /var/run/mysqld/ && chown -R mysql:mysql /data/undolog /data/redolog /data/mysql_data /var/run/mysqld")
    print("|----------------------------------------------------------------------------------------------|")
    print("|Step4、数据目录是否为空检查...")
    aa = os.popen("ls -l /data/mysql_data/ | wc -l", 'r', 100).readlines()
    bb = os.popen("ls -l /data/undolog/ | wc -l", 'r', 100).readlines()
    cc = os.popen("ls -l /data/redolog/ | wc -l", 'r', 100).readlines()
    x = ''
    for a in aa:
        x = a
    y = ''
    for b in bb:
        y = b
    z = ''
    for c in cc:
        z = c
    if remove_last_line(x) == '1' and remove_last_line(y) == '1' and remove_last_line(z) == '1':
        print("|")
        print("|目录为空，检查通过...")
    else:
        print("|/data/undolog /data/redolog /data/mysql_data 目录下存在数据，自动清空中...")
        os.popen("/bin/rm -rf /data/undolog/*")
        os.popen("/bin/rm -rf /data/redolog/*")
        os.popen("/bin/rm -rf /data/mysql_data/*")
    print("|----------------------------------------------------------------------------------------------|")
    print('|Step5、MySQL安装包解压中...')
    os.popen(f"cd /usr/local && tar xzvf /usr/local/{name}.tar.gz", 'r', 100).readlines()
    print("|----------------------------------------------------------------------------------------------|")
    print("|Step6、MySQL初始化完成...")
    print("|----------------------------------------------------------------------------------------------|")
    os.system(
        f"cd /usr/local && ln -s {name} mysql && cd /usr/local/mysql && mkdir mysql-files && chmod 770 mysql-files && chown -R mysql . && chgrp -R mysql . && /usr/local/mysql/bin/mysqld --defaults-file=/etc/my.cnf --datadir=/data/mysql_data --initialize --user=mysql && /usr/local/mysql/bin/mysql_ssl_rsa_setup && cd /usr/local/mysql && chown -R root . && chown -R mysql mysql-files")
    print("|Step7、MySQL实例启动...")
    print("|/usr/local/mysql/bin/mysqld_safe --defaults-file=/etc/my.cnf --user=mysql &")
    os.popen("/usr/local/mysql/bin/mysqld_safe --defaults-file=/etc/my.cnf --user=mysql &")
    print("|----------------------------------------------------------------------------------------------|")
    print("|Step8、MySQL实例启动完毕...")
    print("|----------------------------------------------------------------------------------------------|")
    print("|Step9、生成MySQL初始密码")
    password = os.popen("cat /data/mysql_data/error.log | grep root@localhost: | awk '{print $NF}'", 'r',
                        100).readlines()
    pp = ''
    for p in password:
        pp = remove_last_line(p)
    print("|")
    print(f"|root@localhost密码为：{pp}")
    print("|----------------------------------------------------------------------------------------------|")
    print("|Step10、更新root@localhost密码...")
    print("|")
    print("|执行下面命令更改密码：/usr/local/mysql/bin/mysql -u root -p -S /tmp/mysql3306.sock")
    print("|set password = 'new_password';")
    print("|alter user root@localhost identified by 'new_password';")
    print("|create user 'chongzi'@'%' identified by 'chongzi';")
    print("|grant all privileges on chongzi.* to 'chongzi'@'%';")
    print("|----------------------------------------------------------------------------------------------|")


"""
MySQL满日志分析，使用pt-query-digest工具
"""


def get_slow_analysis(slow_path, hours):
    # 默认分析1小时
    since = f'--since={hours}h'
    version = input("请输入操作系统大版本(比如：6、7)：")
    if version == '7':
        os.popen('rpm -ihv static/MySQL/perl-Digest-1.17-245.el7.noarch.rpm && rpm -ihv static/MySQL/perl-Digest-MD5-2.52-3.el7.x86_64.rpm')

    elif version == '6':
        os.popen('rpm -ivh static/MySQL/perl-')

    res = os.popen(f"""sleep 3 && ./static/MySQL/pt-query-digest {since} {slow_path}""", 'r', 1000).readlines()
    for re in res:
        print(remove_last_line(re))

    print("------------------------------------------------------------------------------------------------")


"""
MySQL主从搭建
"""


def mysqlrepl():
    print(
        "|--------------------('%Y-%m-%d %H:%M:%S')--------------------------------------------------------------------------|")
    current_time = time.strftime('%Y-%m-%d %H:%M:%S')
    master_password = input("输入主库repl密码：")
    mysqldump_path = input("|请输入mysqldump全路径比如/usr/local/mysql/bin/mysqldump：")
    pri_back_path = input("|请输入主库存放备份文件路径，确保空间充足，例如/backup：")
    master_host = input("|请输入主库ip：")
    slave_host = input("|请输入备库ip：")
    slave_back_path = input("|请输入备库存放备份文件路径，确保空间充足，例如/backup：")
    print("|----------------------------------------------------------------------------------------------|")
    print('|Step1、请确认复制参数是否正确...')
    print("|log-bin = mysql-bin")
    print("|server-id =1003306")
    print("|gitd-mode=on")
    print("|ecforce-gtid-consistency=1")
    print("|log-slave-updates=1")
    print("|----------------------------------------------------------------------------------------------|")
    print("|Step2、主库创建用户...")
    print(f"|create user 'repl'@'%' identified by '{primary_repl_pass}'; ")
    print("|grant replication slave on *.* to 'repl'@'%';")
    print("|----------------------------------------------------------------------------------------------|")
    print("|Step3、主备库查看状态...")
    print("|slave：show master status; ")
    print("|reset master;")
    print("|reset slave all;")
    print("|----------------------------------------------------------------------------------------------|")
    print("|Step4、主库用mysqldump导出数据...")
    print(
        f"|{mysqldump_path}| -S /tmp/mysql.sock -p --master-data=2 --single-transaction -A > {pri_back_path}/db_{current_time}.sql")
    os.popen(
        f"{mysqldump_path} -s /tmp/mysql.sock -p --master-data=2 --single-transaction -A > {pri_back_path}/db_{current_time}.sql")
    print("|----------------------------------------------------------------------------------------------|")
    print("|Step5、scp备份文件到备库")
    print(f"|scp {pri_back_path}/db_{current_time}.sql root@{slave_host}:{slave_back_path}")
    os.popen(f"scp {pri_back_path}/db_{current_time}.sql root@:{slave_host}:{slave_back_path}")
    print("|----------------------------------------------------------------------------------------------|")
    print("|Step6、登陆备库进行还原操作")
    print("|mysql -S /tmp/mysql.sock -p < db_20180923.sql")
    print("|如果mysql -S /tmp/mysql.sock -p < db_20180923.sql 报错如下：")
    print("|Enter password: ")
    print("|ERROR 1840 (HY000) at line 24: @@GLOBAL.GTID_PURGED can only be set when @@GLOBAL.GTID_EXECUTED is empty.")
    print("|reset master; 就好了")
    print("|----------------------------------------------------------------------------------------------|")
    print("Step7、备份执行reset master操作...")
    print(f"|change master to master_host='{master_host}',\\")
    print("|master_port=3306,\\")
    print("|master_user='repl',\\")
    print(f"|master_password='{master_password}',\\")
    print("|master_auto_position=1;")
    print("|----------------------------------------------------------------------------------------------|")
    print("Step8、备库启动IO和SQL线程...")
    print("|start slave io_thread;")
    print("|start slave sql_thread;")
    print("|show slave status;")
    print("|----------------------------------------------------------------------------------------------|")
