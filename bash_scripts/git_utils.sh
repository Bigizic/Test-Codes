#!/bin/bash

echo "Enter file name: "; read name
echo "Enter commit message: "; read commit
git add $name
git commit -m $commit
git push
