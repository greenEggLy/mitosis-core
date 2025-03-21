#!/bin/bash

# $1: container number
# $2: sequencial(0)/parallel(1)
# $3: namespace
# $4: time file path
# $5: ROOTFS_ABS_PATH

#clear build cache
echo -n 1 > lock
../../../mitosis-user-libs/mitosis-lean-container/lib/build/start_lean_container $1 $2 $3 $4 $5 /bin/bash ./restore.sh
awk '{print $NF-$1}' $4