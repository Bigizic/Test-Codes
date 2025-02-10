The error "Failed to unlink socket file /tmp/mongodb-27017.sock" suggests that MongoDB does not have permission to access or remove the socket file. This is causing MongoDB to crash.

Fix: --

sudo chmod 777 /tmp
