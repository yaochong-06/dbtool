#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2021/1/12 下午3:49
# @Author  : yaochong/Chongzi
# @FileName: doc.py
# @Software: PyCharm
# @Blog    ：https://github.com/yaochong-06/ ; http://blog.itpub.net/29990276
from docxtpl import DocxTemplate
from data import get_sys_message
# from data import get_oracle_result
from data import get_oracle_local_result
from data import get_mysql_result
from data import get_postgresql_result
from data import get_informix_result
import time

'''
生成Oracle巡检doc文档
'''
current_time = time.strftime('%Y-%m-%d %H:%M:%S')
check_time = time.strftime('%Y/%m/%d')


def get_ora_doc(company_name, oracle_home, sqlplus_path):
    try:
        # 定义模版
        tpl = DocxTemplate('static/tpl/Oracle_db_check_template.docx')

        context = {'company_name': company_name,
                   'check_time': check_time,
                   'df': get_sys_message('df'),
                   'release': get_sys_message('release'),
                   'top': get_sys_message('top'),
                   'vmstat': get_sys_message('vmstat'),
                   'hostname': get_sys_message('hostname'),
                   'free': get_sys_message('free'),
                   # memory
                   'node_memory_MemAvailable': get_sys_message('node_memory_MemAvailable'),
                   'node_memory_MemTotal': get_sys_message('node_memory_MemTotal'),
                   'node_memory_MemFree': get_sys_message('node_memory_MemFree'),
                   # swap
                   'node_memory_SwapTotal': get_sys_message('node_memory_SwapTotal'),
                   'node_memory_SwapFree': get_sys_message('node_memory_SwapFree'),
                   # load
                   'node_load1': get_sys_message('node_load1'),
                   'node_load5': get_sys_message('node_load5'),
                   'node_load15': get_sys_message('node_load15'),
                   # basic
                   'db_info': get_oracle_local_result('db_info', oracle_home, sqlplus_path),
                   'instance_info': get_oracle_local_result('instance_info', oracle_home, sqlplus_path),
                   'memory_info': get_oracle_local_result('memory_info', oracle_home, sqlplus_path),
                   'db_space': get_oracle_local_result('db_space', oracle_home, sqlplus_path),
                   'db_disk_group': get_oracle_local_result('db_disk_group', oracle_home, sqlplus_path),
                   'user_expire_days': get_oracle_local_result('user_expire_days', oracle_home, sqlplus_path),
                   'backup_info': get_oracle_local_result('backup_info', oracle_home, sqlplus_path),
                   # performance
                   'db_top_activity': get_oracle_local_result('db_top_activity',oracle_home, sqlplus_path),
                   'big_table_no_index': get_oracle_local_result('big_table_no_index',oracle_home, sqlplus_path)
                   }

    except Exception as result:
        print(result)
    finally:
        tpl.render(context)
        tpl.save(f'/tmp/Oracle_db_check{current_time}.docx')


def get_mysql_doc(company_name, username, password, ip, port, database):
    tpl = DocxTemplate('static/tpl/MySQL_db_check_template.docx')

    context = {'company_name': company_name,
               'check_time': check_time,
               'df': get_sys_message('df'),
               'release': get_sys_message('release'),
               'top': get_sys_message('top'),
               'vmstat': get_sys_message('vmstat'),
               'hostname': get_sys_message('hostname'),
               'free': get_sys_message('free'),

               # memory
               'node_memory_MemAvailable': get_sys_message('node_memory_MemAvailable'),
               'node_memory_MemTotal': get_sys_message('node_memory_MemTotal'),
               'node_memory_MemFree': get_sys_message('node_memory_MemFree'),
               # swap
               'node_memory_SwapTotal': get_sys_message('node_memory_SwapTotal'),
               'node_memory_SwapFree': get_sys_message('node_memory_SwapFree'),
               # load
               'node_load1': get_sys_message('node_load1'),
               'node_load5': get_sys_message('node_load5'),
               'node_load15': get_sys_message('node_load15'),

               'db_stats_counter': get_mysql_result(username, password, ip, port, database, 'db_stats_counter')

               }

    tpl.render(context)
    tpl.save(f'/tmp/MySQL_db_check{current_time}.docx')


def get_pg_doc(company_name, username, password, ip, port, database):
    tpl = DocxTemplate('static/tpl/PostgreSQL_db_check_template.docx')

    context = {'company_name': company_name,
               'check_time': check_time,
               'df': get_sys_message('df'),
               'release': get_sys_message('release'),
               'top': get_sys_message('top'),
               'vmstat': get_sys_message('vmstat'),
               'hostname': get_sys_message('hostname'),
               'free': get_sys_message('free'),

               # memory
               'node_memory_MemAvailable': get_sys_message('node_memory_MemAvailable'),
               'node_memory_MemTotal': get_sys_message('node_memory_MemTotal'),
               'node_memory_MemFree': get_sys_message('node_memory_MemFree'),
               # swap
               'node_memory_SwapTotal': get_sys_message('node_memory_SwapTotal'),
               'node_memory_SwapFree': get_sys_message('node_memory_SwapFree'),
               # load
               'node_load1': get_sys_message('node_load1'),
               'node_load5': get_sys_message('node_load5'),
               'node_load15': get_sys_message('node_load15'),

               'db_top_activity': get_postgresql_result(username, password, ip, port, database, 'db_top_activity'),
               'long_sql': get_postgresql_result(username, password, ip, port, database, 'long_sql')

               }

    tpl.render(context)
    tpl.save(f'/tmp/PostgreSQL_db_check{current_time}.docx')


def get_informix_doc(company_name):
    tpl = DocxTemplate('static/tpl/informix_db_check_template.docx')

    context = {'company_name': company_name,
               'check_time': check_time,
               'df': get_sys_message('df'),
               'release': get_sys_message('release'),
               'top': get_sys_message('top'),
               'vmstat': get_sys_message('vmstat'),
               'hostname': get_sys_message('hostname'),
               'free': get_sys_message('free'),

               # memory
               'node_memory_MemAvailable': get_sys_message('node_memory_MemAvailable'),
               'node_memory_MemTotal': get_sys_message('node_memory_MemTotal'),
               'node_memory_MemFree': get_sys_message('node_memory_MemFree'),
               # swap
               'node_memory_SwapTotal': get_sys_message('node_memory_SwapTotal'),
               'node_memory_SwapFree': get_sys_message('node_memory_SwapFree'),
               # load
               'node_load1': get_sys_message('node_load1'),
               'node_load5': get_sys_message('node_load5'),
               'node_load15': get_sys_message('node_load15'),

               'long_sql': get_informix_result()

               }

    tpl.render(context)
    tpl.save(f'/tmp/informix_db_check{current_time}.docx')


