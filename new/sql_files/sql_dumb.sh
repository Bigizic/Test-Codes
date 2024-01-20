#!/bin/bash
# bash script that creates a dumb of an entered database
echo -n "Enter user (Default: Root >>> enter r for default): "; read user
echo -n "Enter database: "; read database

if [ "$user" == 'r' ] || [ "$user" == 'R' ] || [ "$user" == 'Root' ] || [ "$user" == 'root' ]; then
	p_user='root'
else
	p_user="$user"
fi

mysqldump -u"$p_user" -p "$database" > "${database}_dump.sql"
