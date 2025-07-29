import sys

sys.path.append("../common")  # include outer path
from criu_wrapper import *

from handler import lambda_handler, get_input, warm_start_handler

import sys


@criu_bench_warm_start
def bench_0(params):
    return warm_start_handler(params)

def bench(params, data):
    ret = lambda_handler(params, data)
    print(ret)


def main():
    input = get_input()
    bench(input)


if __name__ == "__main__":
    main()
