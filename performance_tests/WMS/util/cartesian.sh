#!/bin/bash

delim="," # CSV by default

# Parse flagged arguments:
while getopts "td:" flag
do
  case $flag in
    d) delim=$OPTARG;;
    t) delim="\t";;
    ?) exit;;
  esac
done

# Delete the flagged arguments:
shift $(($OPTIND -1))

# Remaining args now in $*

# Now join $1 and $2
while read a; 
 do while read b; 
      do echo "$a${delim}$b"; 
      done < $2;
 done < $1 
