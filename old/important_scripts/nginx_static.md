## If issue presists when Nginx server block is correct but static files are not displayed

#### enter:

	sudo -u www-data stat ~/path_to_static_files

www-data user is used by Nginx worker process and it needs permissions to read files just like the normal user would read files

#### if error:
	stat: cannot statx '~/path_to_static_files/': Permission denied

give www-data user same privileges like the ubuntu(default) user or specific user on your machine with read privilages to the static files

#### to check privilages enter:

	sudo -u ubuntu stat ~/path_to_static_files

#### or:
	sudo -u a_user stat ~/path_to_static_files

#### lets give privileges:

	sudo gpasswd -a www-data ubuntu

#### or:

	sudo gpasswd -a www-data a_user

make sure a_user or ubuntu can enter and read all directories

now relaod nginx

	sudo nginx -s reload

restart nginx

	sudo systemctl restart nginx.service
