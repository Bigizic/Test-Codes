#!/bin/bash
# bash scripts that run mongodb locally on this old macos catalina

./Downloads/mongodb/bin/mongod --dbpath ~/Downloads/mongodb/data/db > ~/Downloads/mongodb/logs/mongodb.log 2>&1 &
