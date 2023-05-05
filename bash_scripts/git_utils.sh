#!/bin/bash

echo -n "Enter file name: "; read name
echo -n "Enter commit message: "; read commit
git add $name
git commit -m $commit
git push
