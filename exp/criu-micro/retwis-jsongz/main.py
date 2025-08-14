import sys

sys.path.append("../common")  # include outer path
from criu_wrapper import *

from handler import *

import sys


# @criu_bench_warm_start
def bench_0(params):
    return warm_start_handler(params)

# @criu_bench_v2
def bench(params, data):
    ret = lambda_handler(params, data)
    print(f"user data len: {len(ret)}")


def main():
    input = get_input()
    data = bench_0(input)
    bench(input, data)


if __name__ == "__main__":
    main()
