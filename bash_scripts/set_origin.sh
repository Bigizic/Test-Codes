#!/bin/bash

echo -n "Enter access token: "; read access_token
echo -n "Enter username: "; read username
echo -n "Enter repository: "; read repo

git remote set-url origin https://$access_token@github.com/$username/$repo.git
