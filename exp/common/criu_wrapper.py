import argparse
import os
import time
from functools import wraps
import sys
import mmap
sys.stdout.reconfigure(line_buffering=True)

parser = argparse.ArgumentParser()
parser.add_argument("-profile", type=int, default=1, help="whether print out the profile data")
parser.add_argument("-app_name", type=str, default="micro", help="application name")
parser.add_argument("-lock_file", type=str, default="lock", help="lock file")
parser.add_argument("-lock_string", type=str, default="0", help="check the lock file and compare with the first byte of lock string")
parser.add_argument("-exclude_execution", type=int, default=0,
                    help="Whether exclude the resume stage")
parser.add_argument("-time_file", type=str, default="time2", help="record start and end time")
args, _ = parser.parse_known_args()

profile = args.profile
app_name = args.app_name
lock_file = args.lock_file
time_file = args.time_file
lock_string = args.lock_string
ret_imm = args.exclude_execution != 0

mm_lock = None

def criu_bench(handler):
    def wait():
        with open(lock_file, 'rb') as f:
            fd = f.fileno()
            mm_lock = mmap.mmap(fd, 0, flags=mmap.MAP_SHARED, prot=mmap.PROT_READ)
        while chr(mm_lock[0]) == lock_string:
            pass

    @wraps(handler)
    def wrapper(*args, **kwargs):
        # handler(*args, **kwargs)
        wait()
        if not ret_imm:
            handler(*args, **kwargs)
        os._exit(0)

    return wrapper

def safe_write_atomic(path: str, data: str):
    b = data.encode("utf-8", errors="replace")
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o644)
    try:
        os.write(fd, b)
        os.fsync(fd)
    finally:
        os.close(fd)

    
def criu_bench_v2(handler):
    def wait():
        with open(lock_file, 'rb') as f:
            fd = f.fileno()
            mm_lock = mmap.mmap(fd, 0, flags=mmap.MAP_SHARED, prot=mmap.PROT_READ)
        while chr(mm_lock[0]) == lock_string:
            pass

    @wraps(handler)
    def wrapper(*args, **kwargs):
        wait()
        
        with open(time_file, 'a') as f:
            f.write(str(time.time()))
            f.write(" ")
            f.close()
        #safe_write_atomic(time_file, str(time.time()))
            
        if not ret_imm:
            handler(*args, **kwargs)
        
        os._exit(0)

    return wrapper

    
def criu_bench_warm_start(deserialize_handler):
    def wait():
        with open(lock_file, 'rb') as f:
            fd = f.fileno()
            mm_lock = mmap.mmap(fd, 0, flags=mmap.MAP_SHARED, prot=mmap.PROT_READ)
        while chr(mm_lock[0]) == lock_string:
            pass

    @wraps(deserialize_handler)
    def wrapper(*args, **kwargs):
        wait()
        if not ret_imm:
            deserialize_handler(*args, **kwargs)
        
        with open(time_file, 'a') as f:
            f.write(str(time.time()))
            f.write(" ")
            f.close()
        
        os._exit(0)

    return wrapper


def tick_execution_time(handler):
    """

    """
    @wraps(handler)
    def wrapper(*args, **kwargs):
        # start = time.time()
        result = handler(*args, **kwargs)
        # end = time.time()
        # if profile == 1:
        #     print("before start python handler: %f" % (start))
        #     bench.report("%s-execution" % app_name, start, end)
        return result

    return wrapper

