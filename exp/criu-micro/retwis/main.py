import sys

sys.path.append("../common")  # include outer path
from criu_wrapper import *

from handler import lambda_handler, get_input

import sys


@criu_bench_v2
def bench(params):
    ret = lambda_handler(params)
    print(ret)


def main():
    input = get_input()
    bench(input)


if __name__ == "__main__":
    main()
