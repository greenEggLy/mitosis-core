from test import get_input

import sys

from criu_wrapper import *

from test import handler

import sys


@criu_bench_v2
def bench(params):
    ret = handler(params)
    print(ret)


def main():
    input = get_input()
    bench(input)


if __name__ == "__main__":
    main()
