#!/bin/bash
. ./ymltojson.sh

objects=$(cat merged.yml | ymltojson | jq -c '.courses[]')

OLDIFS=$IFS; IFS=$'\n'
for obj in $objects; do
  (echo "obj=$obj"; cat fillform.js) | xclip -selection clipboard
  echo "$(echo $obj | jq -r '.title')"
  read -p "[Enter]"
  echo -en "\e[1A\033[0K" # Erase last line
done
IFS=$OLDIFS
