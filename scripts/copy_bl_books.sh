#!/bin/bash

source=$1
target=$2
mkdir -p $target
for i in $source/1*; do
  if [ -d "$i" ]; then
    year=${i##*/}
    source_path=$source'/'$year'/*.zip'
    target_path=$target'/'$year
    mkdir $target_path
    cp $source_path $target_path'/.'
  fi
done
