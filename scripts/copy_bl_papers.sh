#!/bin/bash

source=$1
target=$2
mkdir -p $target
for i in $source/*; do
  if [ -d "$i" ]; then
    newspaper=${i##*/}
    source_path=$source'/'$newspaper
    target_path=$target'/'$newspaper
    echo $source_path $target_path
    mkdir "$target_path"
    cp "$source_path"/* "$target_path"'/.'
  fi
done
