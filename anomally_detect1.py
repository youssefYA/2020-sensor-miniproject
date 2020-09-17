import pandas
from pathlib import Path
import argparse
import json
from datetime import datetime
import typing as T
import matplotlib.pyplot as plt
import numpy as np

def load_data(file: Path) -> T.Dict[str, pandas.DataFrame]:

    temperature = {}
    occupancy = {}
    co2 = {}
    time = []
    with open(file, "r") as f:
        for line in f:

            r = json.loads(line)
            room = list(r.keys())[0]
            currtime = datetime.fromisoformat(r[room]["time"])

            temperature[currtime] = {room: r[room]["temperature"][0]}
            occupancy[currtime] = {room: r[room]["occupancy"][0]}
            co2[currtime] = {room: r[room]["co2"][0]}
            time += [currtime]
    data = {
        "temperature": pandas.DataFrame.from_dict(temperature, "index").sort_index(),
        "occupancy": pandas.DataFrame.from_dict(occupancy, "index").sort_index(),
        "co2": pandas.DataFrame.from_dict(co2, "index").sort_index(),
    }


    return data, time


file = '/Users/youssefYA/2020-sensor-miniproject/data.txt'

data,_ = load_data(file)
temp = data['temperature'].class1
temp.dropna()
temp_sdev = (temp.var())**0.5
print(temp_sdev)
temp_mean = temp.mean()
print(temp_mean)

# Anomally condition
ubound = temp_mean + 1.5*temp_sdev
lbound = temp_mean - 1.5*temp_sdev
filtered_temps = []

for i in temp:
    if (i <= lbound or i >= ubound):
        print("bad data")
    else:
        filtered_temps += [i]


print('new size is ' +str(len(filtered_temps)) + '\n')
print('old size is ' +str(temp.size) + '\n')

anom_perc = (1-len(filtered_temps)/temp.size)*100

print('the percentage of bad data is: ' + str(anom_perc))
