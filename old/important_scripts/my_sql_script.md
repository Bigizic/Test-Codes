for mysql v8 upwards use:

		ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'password'

If issue presists when the passsword entered in mysql is wrong and i forget password unistal mysql and it's database. Like this:

1. sudo service mysql stop

2. sudo apt-get remove --purge mysql-server mysql-client mysql-common mysql-server-core-* mysql-client-core-*

3. sudo rm -rf /etc/mysql /var/lib/mysql

4. sudo apt-get update

5. sudo apt-get install mysql-server

If no prompt to set password good

6. sudo service mysql start

7. sudo service mysql status

8. sudo service mysql stop

start in safe mode with the skip-grant-table option

9. sudo mysqld_safe --skip-grant-tables &

If error:

	sudo mysqld_safe --skip-grant-tables &
	[1] 19161
	vagrant@ubuntu-xenial:~$ 2023-08-20T13:57:18.583893Z mysqld_safe Logging to syslog.
	2023-08-20T13:57:18.593893Z mysqld_safe Logging to '/var/log/mysql/error.log'.
	2023-08-20T13:57:18.602411Z mysqld_safe Directory '/var/run/mysqld' for UNIX socket file don't exists.

SHOWS UP

	9a. Create missing directory it can't find

	sudo mkdir -p /var/run/mysqld

	Set permission for the directory cuz it needs it

	sudo chown mysql:mysql /var/run/mysqld

	Try restarting in safe mode again, it shouldn't display that error again

	sudo mysqld_safe --skip-grant-tables &

open new terminal

connect to ssh session

10. mysql -u root

11. USE mysql;
UPDATE user SET plugin='mysql_native_password', authentication_string=PASSWORD('newpassword') WHERE User='root';

new password should be enclosed in single quotes, it's required

12. exit;

13. sudo service mysql stop

14. sudo service mysql start

15. Go to other terminal and click enter to exit
