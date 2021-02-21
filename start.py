#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2021/1/12 下午3:49
# @Author  : yaochong/Chongzi
# @FileName: start.py
# @Software: PyCharm
# @Blog    ：https://github.com/yaochong-06/ ; http://blog.itpub.net/29990276
from doc import get_ora_doc
from doc import get_mysql_doc
from doc import get_pg_doc
from doc import get_informix_doc
from datetime import datetime
import oracleutil
import mysqlutil
import os
from binlog2sql import *


def main():
    btime = datetime.datetime.now()
    database_type = ''
    try:
        while database_type not in ('1', '2', '3', '4', '5', '6', '7', '8', '9', '10'):
            database_type = input("""
            ####################dbtool功能列表如下：####################
            #1):Oracle巡检(请给予可执行权限并用Oracle系统用户执行)     #
            #2):MySQL巡检(请使用登陆数据库系统用户执行)                #
            #3):PostgreSQL巡检                                         #
            #4):informix巡检                                           #
            #5):MySQL一键安装(请用root用户执行)                        #
            #6):脚本智能搜索                                           #
            #7):一键MySQL主从                                          #
            #8):MySQL慢日志分析                                        #
            #9):binlog2sql闪回                                         #
            #10):数据库恢复，子功能：                                  #
            #    1、bbed初始化；                                       #
            #    2、controlfile丢失恢复；                              #
            #    3、system文件头损坏恢复
            #    4、跳过归档恢复
            #    5、手工修复block数据
            #    6、归档模式下缺失redo log后恢复
            #    7、Redo Architecture and Configuration
            #    8、Undo深入内部解析  
            #    9、恢复ora-600[4193][4194]错误
            #    10、ORA-8102 Index Corruption恢复
            #    11、Oracle坏块处理                          #  
            ############################################################
            根据提示输入对应功能：""")

            if database_type == '1':
                company_name = input("请输入公司名称:")
                oracle_home = input("请输入ORACLE_HOME路径：")
                sqlplus_path = input("请输入sqlplus的绝对路径：")
                while os.path.exists(oracle_home) and os.path.exists(sqlplus_path):
                    print('路径正确...正在巡检中...')
                    get_ora_doc(company_name, oracle_home, sqlplus_path)
                    break
                else:
                    print("请输入正确的路径...")
                    print("本次巡检失败,请重新开始...")

            elif database_type == '2':
                company_name = input("请输入公司名称:")
                username = input("输入用户名:")
                password = input("输入密码:")
                ip = input("输入ip：")
                port = input("输入端口:")
                database = input("输入数据库名称:")
                get_mysql_doc(company_name, username, password, ip, port, database)
            elif database_type == '3':
                company_name = input("请输入公司名称:")
                username = input("输入用户名:")
                password = input("输入密码:")
                ip = input("输入ip：")
                port = input("输入端口:")
                database = input("输入数据库名称:")
                get_pg_doc(company_name, username, password, ip, port, database)
            elif database_type == '4':
                company_name = input("请输入公司名称:")
                get_informix_doc(company_name)
            elif database_type == '5':
                mysqlutil.mysql57install()
            elif database_type == '6':
                oracleutil.search()
            elif database_type == '7':
                mysqlutil.mysqlrepl()
            elif database_type == '8':
                # 慢日志分析
                path = input("请输入慢日志路径：")
                hours = input("请输入要分析的时长：")
                mysqlutil.get_slow_analysis(path, hours)
            elif database_type == '9':
                # ./main -uroot -p123456 -dtest --start-file=bin.000001

                args = command_line_args(sys.argv[1:])
                conn_setting = {'host': args.host, 'port': args.port, 'user': args.user, 'passwd': args.password, 'charset': 'utf8'}
                binlog2sql = Binlog2sql(connection_settings=conn_setting, start_file=args.start_file,
                                        start_pos=args.start_pos,
                                        end_file=args.end_file, end_pos=args.end_pos, start_time=args.start_time,
                                        stop_time=args.stop_time, only_schemas=args.databases,
                                        only_tables=args.tables,
                                        no_pk=args.no_pk, flashback=args.flashback, stop_never=args.stop_never,
                                        back_interval=args.back_interval, only_dml=args.only_dml,
                                        sql_type=args.sql_type)
                binlog2sql.process_binlog()
            elif database_type == '10':
                subinput = ''
                while subinput not in ('1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'):
                    subinput = input("请选择子功能：")
                    if subinput == '1':
                        oracleutil.init_bbed()
                    elif subinput == '2':
                        oracleutil.recreate_controlfile()
                    elif subinput == '3':
                        oracleutil.system_block_header()
                    elif subinput == '4':
                        pass
                    elif subinput == '5':
                        pass
                    elif subinput == '6':
                        pass
                    elif subinput == '7':
                        pass
                    elif subinput == '8':
                        oracleutil.undo()
                    elif subinput == '9':
                        pass
                    elif subinput == '10':
                        pass
                    elif subinput == '11':
                        pass
            else:
                print("暂不支持其他数据库类型，请输入1、2、3、4、5")
    except Exception as re:
        print(re)
    finally:
        etime = datetime.datetime.now()
        print(f"本次操作完成，耗时{(etime - btime).seconds}秒")


if __name__ == '__main__':
    main()
