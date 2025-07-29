import sys

sys.path.append("../common")  # include outer path
from criu_wrapper import *

from handler import warm_start_handler, get_input, lambda_handler

import sys

@criu_bench_warm_start
def warm_bench(params):
    data =  warm_start_handler(params)
    return data

@criu_bench_v2
def bench(params,data):
    ret = lambda_handler(params, data)
    print(ret)

def main():
    in_put = get_input()
    data = warm_bench(in_put)
    
    
if __name__ == "__main__":
    import time
    main()