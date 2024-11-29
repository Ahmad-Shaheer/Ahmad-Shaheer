#!/bin/bash

# This checks if the number of arguments is correct
# If the number of arguments is incorrect ( $# != 2) print error message and exit
if [[ $# != 2 ]]
then
  echo "backup.sh target_directory_name destination_directory_name"
  exit
fi

# This checks if argument 1 and argument 2 are valid directory paths
if [[ ! -d $1 ]] || [[ ! -d $2 ]]
then
  echo "Invalid directory path provided"
  exit
fi  # this marks the end of the if statement

# [TASK 1]
targetDirectory=$1  # this is the first argument given to the sh file
destinationDirectory=$2 # this is the second argument given to the sh file

# [TASK 2]
echo "The target directory is: $1"
echo "The destination directory is: $2"

# [TASK 3]
currentTS=`$date`  # we use backticks here to for the command next to the $ to be interopreted as a literal.
# we save the currentTS as a substitution command, to call it, we use the $currentTS this is what allows the shell to interpret 
# the self assigned variable to be called

# [TASK 4]
backupFileName="backup-$(date +%Y%m%d-%H%M%S).tar.gz" # calling the currentTS variable inside the file name definition. 
# this is the name of the file created in the target directory


# We're going to:
  # 1: Go into the target directory
  # 2: Create the backup file
  # 3: Move the backup file to the destination directory

# To make things easier, we will define some useful variables...

# [TASK 5]
origAbsPath=$(pwd)  # creating the absolute path for the current directory

# [TASK 6]
cd $destinationDirectory    # moving to the destination directory
destDirAbsPath=`$pwd`       # saving the name of the destinationDirectory's absolute path in a variable of its own

# [TASK 7]
cd $origAbsPath 


# [TASK 8]
yesterdayTS=$(($currentTS - 86500)) # applying arithmatic using the double paranthesis $(())
# recall that calling any variable tht we have defined, we need to add a $ before it


declare -a toBackup #This line declares a variable called toBackup, which is an array.
# -a is used to create an array which is an area of contiguous mmeo

for file in * # [TASK 9]
do
  # [TASK 10]
#   `date -r $file +%s` > $yesterdayTS
  file_last_modified_date=$(date -r "$file" +%s)

  if (($file_last_modified_date > - gt $yesterdayTS))
  then
    # [TASK 11]
    toBackup+=($file)
  fi
done

# [TASK 12]
tar -czvf "$backupFileName" "${toBackup[@]}"
# [TASK 13]
mv "$targetDirectory/$backupFileName" "$destDirAbsPath"
# Congratulations! You completed the final project for this course!

./backup.sh targetdir destdir