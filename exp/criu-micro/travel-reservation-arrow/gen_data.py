
import random
max_request_cnt = 800000
oa_reserve_loc="aaa"
oa_reserve_date="2025-10-10"
reserve_loc = []
reserve_date = []

def get_random_day(month: int, start: int):
    if month in [1, 3, 5, 7, 8, 10, 12]:
        day = random.randint(start, 31)
    elif month in [4, 6, 9, 11]:
        day = random.randint(start, 30)
    else:
        day = random.randint(start, 28)
    return day

def get_random_date():
    in_month = random.randint(1, 12)
    out_month = random.randint(in_month, 12)
    in_day, out_day = 0, 0

    if in_month == out_month:
        in_day = get_random_day(in_month, 1)
        out_day = get_random_day(out_month, in_day)
    else:
        in_day = get_random_day(in_month, 1)
        out_day = get_random_day(out_month, 1)
    return [in_month, in_day], [out_month, out_day]

reserve_cnt = 0
for _ in range(max_request_cnt):

    Lat = 38.0235 + (random.randint(0, 481) - 240.5) / 1000.0
    Lon = -122.095 + (random.randint(0, 325) - 157.0) / 1000.0
    # Loc = [Lat, Lon]
    Date = get_random_date()
    [in_month, in_day], [out_month, out_day] = Date
    
    reserve_loc_cnt = f'{oa_reserve_loc}-{reserve_cnt}'
    reserve_date_cnt = f'{oa_reserve_date}-{reserve_cnt}'
    reserve_loc.append({"Date": reserve_loc_cnt, "Lat": Lat, "Lon": Lon})
    reserve_date.append({"Date": reserve_date_cnt, "InMonth" : in_month, "InDay": in_day, "OutMonth": out_month, "OutDay": out_day})
    # reserve_loc[reserve_loc_cnt] = Loc
    # reserve_date[reserve_date_cnt] = Date
    reserve_cnt += 1

import json

with open('./travel_loc.json', 'w') as f:
    json.dump(reserve_loc, f, indent=4)
with open('./travel_date.json', 'w') as f:
    json.dump(reserve_date, f, indent=4)


import pandas as pd
import pyarrow as pa
import pyarrow.feather as feather

df = pd.DataFrame(reserve_loc)
table = pa.Table.from_pandas(df)
feather.write_feather(table, './travel_loc.arrow')

df = pd.DataFrame(reserve_date)
table = pa.Table.from_pandas(df)
feather.write_feather(table, './travel_date.arrow')

