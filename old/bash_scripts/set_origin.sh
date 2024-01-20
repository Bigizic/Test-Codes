#!/bin/bash
echo -n "Enter Classic Token: "; read token
echo -n "Enter Username: "; read username
echo -n "Enter repository: "; read repo

git remote set-url origin https://$token@github.com/$username/$repo.git
