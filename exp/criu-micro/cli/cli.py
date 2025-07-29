import argparse
import os

# when upload a function file, it will call checkpoint function
def checkpoint(rootfs_path, function_name="lambda_handler", payload=None, function_file = "handler.py"):
    # default function file is ./handler.py, 
    # it should contains lambda_handler(or function_name) and get_input(if payload provided, we will use payload as input)function 
    # We will generate a main.py based on the function file and payload
    gen_main_py(function_name, payload, function_file)
    os.system("sudo bash host_dump.sh")
    os.system(f"sudo bash copy_env.sh {rootfs_path}")

def restore(parallel, number, name, rootfs_path):
    print(f"Restore {number} containers in {'parallel' if parallel else 'sequential'} mode")
    os.system(f"sudo bash run_benchmark.sh {number} {parallel} {name} {rootfs_path}/{os.path.realpath(os.getcwd())}/time {rootfs_path}")



def gen_main_py(function_name = "lambda_handler", payload = None, function_file = "handler.py"):
    file_name = function_file.split('/')[-1].split('.')[0]
    base_main_py = f"""
import sys

from criu_wrapper import *

from {file_name} import {function_name}

import sys


@criu_bench_v2
def bench(params):
    ret = {function_name}(params)
    print(ret)


def main():
    input = get_input()
    bench(input)


if __name__ == "__main__":
    main()
"""
    if function_file != "handler.py" or function_name != "lambda_handler":
        base_main_py = base_main_py.replace("from handler import lambda_handler, get_input", f"from {function_file.split('/')[-1].split('.')[0]} import {function_name}, get_input")
    if payload:
        base_main_py = base_main_py.replace("get_input()", payload)
    else:
        # insert one line to the first line: from {file_name} import get_input
        base_main_py = f"from {file_name} import get_input\n" + base_main_py
    with open("main.py", "w") as f:
        f.write(base_main_py)



if __name__ == "__main__":
    # usage: python cli.py --action checkpoint --rootfs_path <rootfs_path> [--function <function_name>] [--payload <payload>] [--function-file <function_file>]
    # usage: python cli.py --action restore --number <number> --rootfs_path <rootfs_path> [--parallel] [--name <name>] 
    parser = argparse.ArgumentParser()
    parser.add_argument("--action", type=str, choices=["checkpoint", "restore"], help="action")
    parser.add_argument("--rootfs_path", type=str, required=True, help="rootfs path")

    parser.add_argument("--function", type=str, default="lambda_handler", help="function name")
    parser.add_argument("--payload", type=str, default=None, help="payload")
    parser.add_argument("--function-file", type=str, default="handler.py", help="function file")

    parser.add_argument("--parallel", action='store_true', help="parallel")
    parser.add_argument("--number", type=int, default=1, help="number")
    parser.add_argument("--name", type=str, default="my_container", help="name")
    args = parser.parse_args()

    rootfs = args.rootfs_path
    parallel = 1 if args.parallel else 0
    if rootfs[-1] == "/":
        rootfs = rootfs[:-1]
    if args.action == "checkpoint":
        checkpoint(rootfs, args.function, args.payload, args.function_file)
    elif args.action == "restore":
        restore(parallel, args.number, args.name, rootfs)

