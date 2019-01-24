#!/bin/bash

# Usage:
#    source copy_bl_papers.sh <SOURCE> <TARGET>
#
# where <SOURCE> is a directory, with subdirectories:
#
#    <DIRECTORY>/
#        <FILE>
#        <FILE>
#        <FILE>
#        ...
#    <DIRECTORY>/
#        <FILE>
#        <FILE>
#        <FILE>
#        ...
#    ...
#
# These contents are copied into directory <TARGET>.
#
# All files are copied except for files prefixed by dot ".".

source=$1
target=$2
mkdir -p $target
for i in $source/*; do
  if [ -d "$i" ]; then
    sub_path=${i##*/}
    source_path=$source'/'$sub_path
    target_path=$target'/'$sub_path
    echo $source_path $target_path
    mkdir "$target_path"
    cp "$source_path"/* "$target_path"'/.'
  fi
done
