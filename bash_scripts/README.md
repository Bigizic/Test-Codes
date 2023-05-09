## This repo contains useful bash scripts mainly for git

### All scripts are to be used on a personal pc

#### you can execute shell scripts with
		chmod +x {filename}

## 1:
Display a prompt, asks you to enter a filename, trunicate through the name you give it and check if the first digit of your file name is a number if so it removes it and input *update + the name of your file* if the first digit is not a digit it commit with *add + name of your file*. 

## This bash script generates a commit message for you 

----------------------------------------------------------------------------------------------------------------------------------------------------


## 1: set_origin.sh: 
This script allows you to set access token, username and repo while you're in the repo. With this script you don't have to enter username and password whenever you git push.

-----------------------------------------------------------------------------------------------------------------

## 2: git_utils.sh: 
This script mimick the
		git add {filename}
		git commit -m ''
		git push
Commands. The commit message does not allow spaces

-----------------------------------------------------------------------------------------------------------------

## 3: utils2.sh:
This script adds all changes at once and writes a commit message for files that have been added

-----------------------------------------------------------------------------------------------------------------
