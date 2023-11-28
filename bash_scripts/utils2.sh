#!/bin/bash

echo -n "Enter Commit Message: "; read commit
git add .
git commit -m "$commit"
git push
