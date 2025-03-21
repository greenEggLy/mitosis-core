#!/bin/bash

rootfs=$1
realpath=$2
docker=$3

apps=(1 2 3 4 5)
modes=(0 1)
number_parallel=(1 10 50 100)
number_seq=(1 10 20)

for app in "${apps[@]}"; do
    for mode in "${modes[@]}"; do
        if [ "$mode" -eq 0 ]; then
            for seq in "${number_seq[@]}"; do
                echo "Running app $app in sequential mode with $seq tasks"
                if [ "$docker" -eq 0 ]; then
                    bash ./run_benchmark.sh $app $seq $mode my_container $rootfs/$realpath/time $rootfs
                elif [ "$docker" -eq 1 ]; then
                    bash ./run_benchmark_docker.sh $seq $mode
                fi 
            done
        elif [ "$mode" -eq 1 ]; then
            for parallel in "${number_parallel[@]}"; do
                echo "Running app $app in parallel mode with $parallel tasks"
                if [ "$docker" -eq 0 ]; then
                    bash ./run_benchmark.sh $app $parallel $mode my_container $rootfs/$realpath/time $rootfs
                elif [ "$docker" -eq 1 ]; then
                    bash ./run_benchmark_docker.sh $parallel $mode
                fi
            done
        fi
    done
done