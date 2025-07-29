echo -n 0 > lock
echo -n 0 > time
# setsid python3 test_.py < /dev/null > execution.log 2>&1 &
# setsid /home/ly/miniconda3/bin/python3 test_.py < /dev/null > execution.log 2>&1 &

case $1 in
    retwis|1)
        setsid /home/ly/miniconda3/bin/python3 retwis/main.py < /dev/null > execution.log 2>&1 &
    ;;
    video|2)
        setsid /home/ly/miniconda3/bin/python3 video-classify/main.py < /dev/null > execution.log 2>&1 &
    ;;
    movie|3)
        setsid /home/ly/miniconda3/bin/python3 movie-review/main.py < /dev/null > execution.log 2>&1 &
    ;;
    ml|4)
        setsid /home/ly/miniconda3/bin/python3 ml-pipe/main.py < /dev/null > execution.log 2>&1 &
    ;;
    travel|5)
        setsid /home/ly/miniconda3/bin/python3 travel-reservation/main.py < /dev/null > execution.log 2>&1 &
    ;;
    movie2|6)
        setsid /home/ly/miniconda3/bin/python3 movie-review-arrow/main.py < /dev/null > execution.log 2>&1 & 
    ;;
    travel2|7)
        setsid /home/ly/miniconda3/bin/python3 travel-reservation-arrow/main.py < /dev/null > execution.log 2>&1 & 
esac
export TARGET_PID=$(pgrep python3)
echo "TARGET_PID=${TARGET_PID}"
rm -rf imgs && mkdir imgs
sleep 3
~/mitosis/criu/criu/criu dump --images-dir=./imgs -t ${TARGET_PID} -v -o dump.log
# criu dump --images-dir=./imgs -t ${TARGET_PID} -vvvv -o dump.log
tail -n 1 imgs/dump.log
echo -n 1 > lock
