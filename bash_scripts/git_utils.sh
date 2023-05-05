#!/bin/bash

echo -n "Enter filename: "; read filename
echo -n "Enter commit message: "; read commit

git add $filename
git commit -m $commit
git push
