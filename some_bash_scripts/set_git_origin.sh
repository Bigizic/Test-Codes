#!/bin/bash

echo "Enter access token: "
read access_token
echo "Enter username: "
read username
echo "Enter repository: "
read repo

git remote set-url origin https://$access_token@github.com/$username/$repo.git
