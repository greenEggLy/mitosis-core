#!/bin/bash

image="criu:v2.0"
count=$1
mode=$2

start_container() {
    docker run --rm -d criu:v2.0
}

export -f start_container

START=$(date +%s.%N)

if [ "$mode" -eq 0 ]; then # sequential
    for ((i=0; i<count; i++)); do
        docker run --rm -d criu:v2.0
    done
elif [ "$mode" -eq 1 ]; then #parallel
    seq "$count" | parallel -n0 start_container
fi
END=$(date +%s.%N)
difference=$(awk "BEGIN {print $END - $START}")
echo $difference