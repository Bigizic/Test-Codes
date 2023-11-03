#!/bin/bash

gpg_output=$(gpg --list-secret-keys --keyid-format=long)

ed=$(echo "$gpg_output" | grep "sec   ed" | awk '{print $2}')

key_id=$(echo "$ed" | awk -F/ '{print $2}')

echo -n "Enter user name: "; read input_name
echo -n "Enter user email: "; read input_email

git config --local user.name "$input_name"
git config --local user.email "$input_email"

git config --local commit.gpgsign true
git config --local user.signingkey $key_id

#  echo $key_id
