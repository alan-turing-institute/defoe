#!/bin/bash
#
# Usage: 
#    source copy_bl_books.sh <SOURCE> <TARGET>
# 
# where <SOURCE> is a directory, with subdirectories:
#
#    1<DIRECTORY>/
#        <FILE>.zip
#        <FILE>.zip
#        <FILE>.zip
#        ...
#    1<DIRECTORY>/
#        <FILE>.zip
#        <FILE>.zip
#        <FILE>.zip
#        ...
#    ...
#
# All subdirectories are assumed to be prefixed with the number "1". 
#
# These contents are copied into directory <TARGET>.
#
# Any files not ending in ".zip" are not copied, nor are files
# prefixed by dot ".".

source=$1
target=$2
mkdir -p $target
for i in $source/1*; do
  if [ -d "$i" ]; then
    sub_path=${i##*/}
    source_path=$source'/'$sub_path'/*.zip'
    target_path=$target'/'$sub_path
    mkdir $target_path
    cp $source_path $target_path'/.'
  fi
done
