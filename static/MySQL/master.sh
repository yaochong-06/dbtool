#!/bin/bash

Master_Log_File=$(mysql -e "show slave status\G" | grep -w Master_Log_File | awk -F": " '{print $2}')
Relay_Master_Log_File=$(mysql -e "show slave status\G" | grep -w Relay_Master_Log_File | awk -F": " '{print $2}')
Read_Master_Log_Pos=$(mysql -e "show slave status\G" | grep -w Read_Master_Log_Pos | awk -F": " '{print $2}')
Exec_Master_Log_Pos=$(mysql -e "show slave status\G" | grep -w Exec_Master_Log_Pos | awk -F": " '{print $2}')
#60s waiting slave relay log exe
i=1
while true
do
if [ $Master_Log_File = $Relay_Master_Log_File ] && [ $Read_Master_Log_Pos -eq $Exec_Master_Log_Pos ]
then
   echo "ok"

echo "master" > /home/mysql/state
#stop slave replication,change read only pro
mysql -e "stop slave;"
mysql -e "set global read_only=0;"

   break
else
      sleep 1
   if [ $i -gt 120 ]
   then
      break
   fi
   continue
   let i++
fi
done

#systemctl restart proxysql