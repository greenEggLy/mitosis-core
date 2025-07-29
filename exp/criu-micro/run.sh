# START=$(date +%s.%N)
# echo "before start lean container: $START"
#!/bin/bash

# $1: container number
# $2: sequencial(0)/parallel(1)
# $3: namespace
# $4 ROOTFS_ABS_PATH

start_file=$4$(realpath .)/time
end_file=$4$(realpath .)/time2
../../mitosis-user-libs/mitosis-lean-container/lib/build/start_lean_container $1 $2 $3 $start_file $4 /bin/bash ./restore.sh

if [ "$2" == '0' ]; then
    awk 'NR==1 {for(i=1;i<=NF;i++) a[i]=$i; next} NR==2 {sum=0; for(i=1;i<=NF;i++) sum+=(a[i]-$i); print sum; exit}' "$end_file" "$start_file"
elif [ "$2" == '1' ]; then
    awk 'NR==1 {first=$NF; next} NR==2 {last=$1; print first-last; exit}' "$end_file" "$start_file"
fi
