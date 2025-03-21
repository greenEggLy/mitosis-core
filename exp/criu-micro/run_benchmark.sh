# START=$(date +%s.%N)
# echo "before start lean container: $START"
#!/bin/bash

# $1: case: 1/2/3/4/5
# $2: container number
# $3: sequencial(0)/parallel(1)
# $4: namespace
# $5: time file path
# $6: ROOTFS_ABS_PATH

#clear build cache
START=$(date +%s.%N)
bash host_dump.sh $1
bash copy_env.sh $6
echo -n 1 > lock
END=$(date +%s.%N)
../../mitosis-user-libs/mitosis-lean-container/lib/build/start_lean_container $2 $3 $4 $5 $6 /bin/bash ./restore.sh
# END=$(date +%s.%N)
# TOTAL_TIME=$(echo "($END-$START)*1000" | bc) # uncomment this to calculate the full end-to-end time
# tail -n 2 $2/$(pwd)/execution.log
difference=$(awk "BEGIN {print $END - $START}")
echo $difference
awk '{print $NF-$1}' $5