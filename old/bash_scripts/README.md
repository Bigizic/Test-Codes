## This repo contains useful bash scripts mainly for git

### All scripts are to be used on a personal pc

#### you can execute shell scripts with
		chmod +x {filename}

## m:

This script imports the subprocess module to run some git commands.
It trunicates through your filename and check if your filename has
a digit or hypen if yes it skips that character and takes the remaning
file name and update it in a variable, it proceeds to add Update + the
trunicated filename if the first digit of the filename is a number
otherwise it puts the file name and include Add to it

## This python script generates a commit message for you 

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
