#!/bin/bash


state=`cat /home/mysql/state`

case $state in
master)
mysql -e "show status;" > /dev/null 2>&1
i=$?
ps aux | grep mysqld | grep -v grep > /dev/null 2>&1
j=$?
#systemctl status proxysql >  /dev/null 2>&1
#k=$?

if [ $i = 0 ] && [ $j = 0 ]
then
   exit 0
else
   systemctl stop keepalived.service
fi


        exit 0
;;
*)
        exit 0
;;
esac