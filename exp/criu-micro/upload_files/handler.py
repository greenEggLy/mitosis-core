import pandas as pd
import pyarrow as pa
import pyarrow.feather as feather


def warm_start_handler(params):
    file_name = params["file_name"]
    df_arrow = feather.read_feather(file_name)
    return df_arrow


def lambda_handler(params,data):
    return data


def get_input():
    params = {
        "file_name": "/tmp/data.arrow"
    }
    return params