* Note

* The following public GPG build key is for MySQL 5.7.37 packages and higher. For the public GPG build key for earlier MySQL release packages (keyID 5072E1F5), see Section 2.1.4.5, “GPG Public Build Key for Archived Packages”.

`copy public key`
<a href="https://dev.mysql.com/doc/refman/5.7/en/checking-gpg-signature.html"> Here </a>

Save it in a file in home dir

	sudo apt-key add {path to key}

add the apt repo

	sudo sh -c 'echo "deb http://repo.mysql.com/apt/ubuntu bionic mysql-5.7" >> /etc/apt/sources.list.d/mysql.list'

update apt

	sudo apt-get update

check available version

	sudo apt-cache policy mysql-server

Now install mysql 5.7

	sudo apt install -f mysql-client=5.7* mysql-community-server=5.7* mysql-server=5.7*

Now install mysql alchemy

    pip install mysqlclient

Install mysql alchmey dependencies

    sudo apt-get install libmysqlclient-dev

    sudo apt-get install libmariadbclient-dev


Then update mysql to version 8

	sudo apt-get update
	sudo apt-get install wget
	wget https://dev.mysql.com/get/mysql-apt-config_0.8.23-1_all.deb
	sudo dpkg -i mysql-apt-config_0.8.23-1_all.deb


Update package list

	sudo apt-get update


Update mysql server

	sudo apt-get upgrade mysql-server
 	sudo service mysql restart

If this error presist update libmariab3
error:  NameError: name '_mysql' is not defined

	sudo apt-get install libmariadb3 libmariadb-dev

    


## READ
* <a href="https://www.digitalocean.com/community/tutorials/how-to-choose-a-redundancy-plan-to-ensure-high-availability#sql-replication"> SQL REPLICATION </a>
* <a href="https://www.digitalocean.com/community/tutorials/how-to-set-up-replication-in-mysql"> How To Set Up Replication in MySQL</a>
