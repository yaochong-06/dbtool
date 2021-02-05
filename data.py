#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2021/1/12 下午3:49
# @Author  : yaochong/Chongzi
# @FileName: data.py
# @Software: PyCharm
# @Blog    ：https://github.com/yaochong-06/ ; http://blog.itpub.net/29990276
import os
# import cx_Oracle
import pymysql
import psycopg2


# 删除文件最后一行
def remove_last_line(s):
    return s[:s.rfind('\n')]


# 返回Oracle sql脚本内容
def get_oracle_file_contents(filename):
    try:
        file_f = open('static/sqlfile/Oracle/' + filename + '.sql', 'r')
        file_contents = file_f.read()
        file_f.close()
    except Exception as re:
        print(re)
    return file_contents


def get_mysql_file_contents(filename):
    try:
        file_f = open('static/sqlfile/MySQL/' + filename + '.sql', 'r')
        file_contents = file_f.read()
        file_f.close()
    except Exception as re:
        print(re)
    return file_contents


# 返回pg脚本内容
def get_postgresql_file_contents(filename):
    try:
        file_f = open('static/sqlfile/PostgreSQL/' + filename + '.sql', 'r')
        file_contents = file_f.read()
        file_f.close()
    except Exception as re:
        print(re)
    return file_contents


def get_sys_message(sysscripts):
    if sysscripts == 'df':
        return remove_last_line(os.popen('df -h', 'r', 100).read())
    elif sysscripts == 'release':
        return remove_last_line(os.popen('cat /etc/redhat-release', 'r', 100).read())
    elif sysscripts == 'top':
        return remove_last_line(os.popen('top -b -n 1 | head -n 16', 'r', 100).read())
    elif sysscripts == 'vmstat':
        return remove_last_line(os.popen('vmstat 1 5', 'r', 100).read())
    elif sysscripts == 'hostname':
        return remove_last_line(os.popen('hostname', 'r', 100).read())
    elif sysscripts == 'free':
        return remove_last_line(os.popen('free -g', 'r', 100).read())
    # 内存
    elif sysscripts == 'node_memory_MemAvailable':
        return remove_last_line(os.popen("cat /proc/meminfo |awk '/MemAvailable/{print $2}'", 'r', 100).read())
    elif sysscripts == 'node_memory_MemTotal':
        return remove_last_line(os.popen("cat /proc/meminfo |awk '/MemTotal/{print $2}'", 'r', 100).read())
    elif sysscripts == 'node_memory_MemFree':
        return remove_last_line(os.popen("cat /proc/meminfo | awk '/MemFree/{print $2}'", 'r', 100).read())
    # swap
    elif sysscripts == 'node_memory_SwapTotal':
        return remove_last_line(os.popen("cat /proc/meminfo |awk '/SwapTotal/{print $2}'", 'r', 100).read())
    elif sysscripts == 'node_memory_SwapFree':
        return remove_last_line(os.popen("cat /proc/meminfo |awk '/SwapFree/{print $2}'", 'r', 100).read())
    # load 1 5 15
    elif sysscripts == 'node_load1':
        return remove_last_line(os.popen("cat /proc/loadavg |awk '{print $1}'", 'r', 100).read())
    elif sysscripts == 'node_load5':
        return remove_last_line(os.popen("cat /proc/loadavg |awk '{print $2}'", 'r', 100).read())
    elif sysscripts == 'node_load15':
        return remove_last_line(os.popen("cat /proc/loadavg |awk '{print $3}'", 'r', 100).read())
    # filesystem
    elif sysscripts == 'node_filesystem_size_kb':
        return remove_last_line(
            os.popen("""df -T |awk 'NR>1{print "device:"$1",mountpoint:"$NF","$3}'""", 'r', 100).read())
    elif sysscripts == 'node_filesystem_avail_kb':
        return remove_last_line(
            os.popen("""df |awk 'NR>1{print "device:"$1",mountpoint:"$NF","$4}'""", 'r', 100).read())
    elif sysscripts == 'node_filesystem_files':
        return remove_last_line(
            os.popen("""df -iT |awk 'NR>1{print "device:"$1",fstype:"$2",mountpoint:"$NF","$3}'""", 'r', 100).read())

    elif sysscripts == 'node_filesystem_files_free':
        return remove_last_line(
            os.popen("""df -iT |awk 'NR>1{print "device:"$1",fstype:"$2",mountpoint:"$NF","$5}'""", 'r', 100).read())
    # cpu
    elif sysscripts == 'node_cpu':
        # r取消转义
        return remove_last_line(os.popen(
            r"""top -bn 2 -i -c | grep "Cpu(s):" | awk -F: '{print $2}' | tail -1 | sed 's/[\%a-z,]\+/\n/g' | sed 's/ \+//g' | awk 'BEGIN{mode[1]="user";mode[2]="system";mode[3]="nice";mode[4]="idle";mode[5]="iowait"}NR<=5{printf "cpu:cpus,mode:%s,%s\n",mode[NR],$0}'""",
            'r', 100).read())
    else:
        return ''


'''
# 获取Oracle执行结果，使用cx_Oracle方式暂时注释掉
def get_oracle_result(username, password, ip, port, service_name, sqlscripts):
    try:
        url = f"""{ip}:{port}/{service_name}"""
        # 建立数据库链接
        connection = cx_Oracle.connect(username, password, url)
        cur = connection.cursor()
        print("连接创建成功，正在巡检中...")
    except Exception as re:
        print(re)
        print("连接创建失败,请检查用户名、密码、IP、端口等信息是否正确...")
        # 查询sql
    try:
        sql_text = get_oracle_file_contents(sqlscripts)
        rows = cur.execute(sql_text)
        # 获得当前sql的列名
        title = [i[0] for i in cur.description]

        result_list = []
        for row in rows:
            # 生成二维列表
            result_list.append(row)

        # 将二维嵌套列表[['name','age'],['tom','11']]转换为列表包含字典[{'name':'tom','age':'11'}]
        list_oracle_result_dict = []
        for i in result_list:
            tmp_dict = dict(zip(title, i))
            list_oracle_result_dict.append(tmp_dict)

        return list_oracle_result_dict

    except Exception as re:
        print(re)
    finally:
        cur.close()
        connection.close()

'''


# 获得mysql脚本执行结果
def get_mysql_result(username, password, ip, port, database, sqlscripts):
    try:

        # 打开数据库连接
        connection = pymysql.connect(host=ip, port=int(port), user=username, password=password, database=database)
        cursor = connection.cursor()
        print("连接创建成功，正在巡检中...")
    except Exception as re:
        print(re)
        print("连接创建失败,请检查用户名、密码、IP、端口等信息是否正确...")

    try:
        sql_text = get_mysql_file_contents(sqlscripts)

        rows = cursor.execute(sql_text)
        # 获得当前sql的列名
        title = [i[0] for i in cursor.description]
        rows = cursor.fetchall()
        result_list = []
        for row in rows:
            # 生成二维列表
            result_list.append(list(row))

        # 将二维嵌套列表[['name','age'],['tom','11']]转换为列表包含字典[{'name':'tom','age':'11'}]
        list_mysql_result_dict = []
        for i in result_list:
            tmp_dict = dict(zip(title, i))
            list_mysql_result_dict.append(tmp_dict)
    except Exception as re:
        print(re)
    finally:
        cursor.close()
        connection.close()
        return list_mysql_result_dict


# 获得pg脚本执行结果
def get_postgresql_result(username, password, ip, port, database, sqlscripts):
    try:
        connection = psycopg2.connect(database=database, user=username, password=password, host=ip, port=port)
        cur = connection.cursor()
        cur.execute(get_postgresql_file_contents(sqlscripts))
        print("连接创建成功，正在巡检中...")
    except Exception as re:
        print(re)
        print("连接创建失败,请检查用户名、密码、IP、端口等信息是否正确...")
    try:
        # 查询sql
        rows = cur.fetchall()
        # 获得当前sql的列名
        title = [i[0] for i in cur.description]
        result_list = []
        for row in rows:
            # 生成二维列表
            result_list.append(row)
        # 将二维嵌套列表[['name','age'],['tom','11']]转换为列表包含字典[{'name':'tom','age':'11'}]
        list_postgres_result_dict = []
        for i in result_list:
            tmp_dict = dict(zip(title, i))
            list_postgres_result_dict.append(tmp_dict)
        return list_postgres_result_dict
    except Exception as re:
        print('PostgreSQL Exception:', re)
    finally:
        cur.close()
        connection.close()


# 获得informix执行结果
def get_informix_result():
    os.popen('/bin/sh static/sqlfile/informix/informix_check.sh', 'r', 100).read()


# 获取Oracle执行结果
def get_oracle_local_result(sqlscripts, oracle_home, sqlplus_path):

    res = os.popen(f"""
export ORACLE_HOME={oracle_home} && {sqlplus_path} / as sysdba <<EOF
set colsep "|"
set linesize 32767
set pages 20000
@static/sqlfile/Oracle/{sqlscripts}.sql
EOF""", 'r', 100).readlines()
    # 生成二维列表
    result_list = []
    for re in res:
        if re.startswith('db_check_'):
            result_list.append(re.replace('\t', '').strip().replace(' ', '').split('|'))

    # 将二维嵌套列表[['name','age'],['tom','11']]转换为列表包含字典[{'name':'tom','age':'11'}]
    # 取第一行字典
    list_oracle_result_dict = []
    # 判断以下result_list是否为空，也就意味着巡检的sql是否有返回值
    if result_list:
        title = result_list[0]

        for i in result_list:
            tmp_dict = dict(zip(title, i))
        list_oracle_result_dict.append(tmp_dict)

    return list_oracle_result_dict

