import sys

sys.path.append("../common")  # include outer path
from criu_wrapper import *

from handler import *

import time


@criu_bench_warm_start
def bench_0(params):
    start = time.time()
    ret =  warm_start_handler(params)
    end = time.time()
    print(end-start)
    return ret

@criu_bench_v2
def bench(params, data):
    ret = lambda_handler(params, data)
    print(ret)


def main():
    input = get_input()
    data = bench_0(input)
    bench(input, data)


if __name__ == "__main__":
    main()
