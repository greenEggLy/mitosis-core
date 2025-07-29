# START=$(date +%s.%N)
# echo "before start lean container: $START"
#!/bin/bash

# $1: case: 1/2/3/4/5/6
# $2: container number
# $3: sequencial(0)/parallel(1)
# $4: namespace
# $5 ROOTFS_ABS_PATH

#clear build cache
START=$(date +%s.%N)
bash host_dump.sh $1
bash copy_env.sh $5
echo -n 1 > lock
END=$(date +%s.%N)
start_file=$5$(realpath .)/time
end_file=$5$(realpath .)/time2
LD_LIBRARY_PATH=/home/ly/miniconda3/lib:$LD_LIBRARY_PATH ../../mitosis-user-libs/mitosis-lean-container/lib/build/start_lean_container $2 $3 $4 $start_file $5 /bin/bash ./restore.sh

# difference=$(awk "BEGIN {print $END - $START}")

# if [ "$3" == '0' ]; then
#     awk 'NR==1 {for(i=1;i<=NF;i++) a[i]=$i; next} NR==2 {sum=0; for(i=1;i<=NF;i++) sum+=(a[i]-$i); print sum; exit}' "$end_file" "$start_file"
# elif [ "$3" == '1' ]; then
#     awk 'NR==1 {first=$NF; next} NR==2 {last=$1; print first-last; exit}' "$end_file" "$start_file"
# fi

awk '{print $(NF-1)-$1}' "$start_file"