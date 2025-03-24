import sys
# import argparse

# parser = argparse.ArgumentParser()
# parser.add_argument("--handler-path", type=str, default=".")
# args = parser.parse_args()

sys.path.append("../common")  # include outer path
from criu_wrapper import *

from handler import lambda_handler, get_input

import sys
import json
import urllib.request
import time
import threading
import os

# make it True when you want to use redis between remote machines instead of our own library.
# make sure all /etc/hosts on host machine are configured correctly.
# like "10.244.1.2 redis-service"
# get this ip via "kubectl describe service redis-service | grep Endpoints"
use_redis_when_remote = False


# the port of each stage

def stage0(schedule = None, request_id = "000000"):
    # arguments = [[{
    #     'dummy': 0,
    #     'input': 'ML_Pipeline/Digits_Train.txt',
    #     'output': {
    #         'vectors_pca': f"{request_id}-ML_Pipeline/stage0/vectors_pca", 
    #         'train_pca_transform': f"{request_id}-ML_Pipeline/stage0/train_pca_transform"
    #     },
    #     'use_redis_when_remote': use_redis_when_remote,
    #     'schedule': schedule
    # }, None]]

    # for argument in arguments:
    input = get_input()
    # print(f"input:{input}")
    result = lambda_handler(input)

    if result is not None:
        return result
    else:
        print("stage0 timeout")
        return None

# def stage1(schedule, request_id = "000000"):
#     stage1_loc = {
#         'input': {
#             'train_pca_transform': f'{request_id}-ML_Pipeline/stage0/train_pca_transform'
#         },
#         'output': {
#             'model_prefix': f'{request_id}-ML_Pipeline/stage1/model'
#         },
#         'use_redis_when_remote': use_redis_when_remote,
#         'schedule': schedule
#     }

#     # two tasks, each task run 2 (the second argument) times.
#     # parallelism = vcpucnt = 1 (the third arg)

#     # TODO: to parellelize them. Use async.
#     # arguments = [[0, 2, 1, stage1_loc], [1, 2, 1, stage1_loc]]

#     arguments = [[0, 1, 1, stage1_loc]]
    
#     for argument in arguments:
#         result = fw.send_lambda_call(schedule['stage1'][0], schedule['stage1'][1], argument)

#         if result is not None:
#             return result
#         else:
#             print("stage1 timeout")
#             return None

# def stage2(schedule, request_id = "000000"):
#     stage2_key = {
#         'input': {
#             'train_pca_transform': f'{request_id}-ML_Pipeline/stage0/train_pca_transform', 
#             'model_prefix': f'{request_id}-ML_Pipeline/stage1/model'
#         },
#         'output': {
#             'forest_prefix': f'{request_id}-ML_Pipeline/stage2/forest', 
#             'predict_prefix': f'{request_id}-ML_Pipeline/stage2/predict'
#         },
#         'use_redis_when_remote': use_redis_when_remote,
#         'schedule': schedule
#     }
#     # arguments = [[2, 0, stage2_key], [2, 1, stage2_key]]
#     # TODO: to parellelize them. Use async.

#     arguments = [[1, 0, stage2_key]]

#     for argument in arguments:

#         result = fw.send_lambda_call(schedule['stage2'][0], schedule['stage2'][1], argument)

#         if result is not None:
#             return result
#         else:
#             print("stage2 timeout")
#             return None


# def stage3(schedule, request_id = "000000"):
#     arguments = [[{
#         'input':{
#             'train_pca_transform': f'{request_id}-ML_Pipeline/stage0/train_pca_transform', 
#             'predict_prefix': f'{request_id}-ML_Pipeline/stage2/predict'
#         },
#         'use_redis_when_remote': use_redis_when_remote,
#         'schedule': schedule
#     }], ]

#     for argument in arguments:
#         result = fw.send_lambda_call(schedule['stage3'][0], schedule['stage3'][1], argument)

#         if result is not None:
#             return result
#         else:
#             print("stage3 timeout")
#             return None



@criu_bench_v2
def pipe_go(): 

    # get accurate time in microseconds
    start_time = int(round(time.time() * 1000)) / 1000.0

    print("stage0 going...")
    print(stage0())
    # print("stage1 going...")
    # print(stage1(schedule))
    # print("stage2 going...")
    # print(stage2(schedule))
    # print("stage3 going...")
    # print(stage3(schedule))


    # get time
    end_time = int(round(time.time() * 1000)) / 1000.0

    # get time elapsed
    elapsed_time = end_time - start_time

    return elapsed_time

        
if __name__ == "__main__":
    # Check if enough command line arguments are provided
    # if len(sys.argv) < 3:
    #     print("Usage: python client.py <IP> <port>")
    #     sys.exit(1)

    pipe_go()
