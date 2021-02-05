#!/bin/bash
echo 2
echo "backup" > /home/mysql/state
M_File1=$(mysql -e "show master status\G" | awk -F': ' '/File/{print $2}')
M_Position1=$(mysql  -e "show master status\G" | awk -F': ' '/Position/{print $2}')
sleep 1
M_File2=$(mysql -e "show master status\G" | awk -F': ' '/File/{print $2}')
M_Position2=$(mysql -e "show master status\G" | awk -F': ' '/Position/{print $2}')
i=1
while true
do
if [ $M_File1 = $M_File2 ] && [ $M_Position1 -eq $M_Position2 ]
then
   echo "ok"

mysql -e "set global read_only=1;"
mysql -e "CHANGE MASTER TO
MASTER_HOST='10.10.8.62',
MASTER_PORT=3306,
MASTER_USER='repl',
MASTER_PASSWORD='nkm%cF',
MASTER_AUTO_POSITION=1;"
mysql -e "start slave;"

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
