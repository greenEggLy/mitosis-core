echo -n 0 > lock
echo -n 0 > time
# setsid python3 test_.py < /dev/null > execution.log 2>&1 &
# setsid /home/ly/miniconda3/bin/python3 test_.py < /dev/null > execution.log 2>&1 &

setsid /home/ly/miniconda3/bin/python3 main.py < /dev/null > execution.log 2>&1 &
export TARGET_PID=$(pgrep python3)
echo "TARGET_PID=${TARGET_PID}"
rm -rf imgs && mkdir imgs
sleep 3
~/mitosis/criu/criu/criu dump --images-dir=./imgs -t ${TARGET_PID} -vvvv -o dump.log
# criu dump --images-dir=./imgs -t ${TARGET_PID} -vvvv -o dump.log
tail -n 1 imgs/dump.log
echo -n 1 > lock
