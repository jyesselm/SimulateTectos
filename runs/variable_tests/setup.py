import itertools
import os
import pandas as pd
import numpy as np
from rnamake.submit import qsub_job

from simulate_tectos import settings


f = open("variables.dat")
lines = f.readlines()
f.close()
lines.pop(0)

variables = []
all_values = []
for l in lines:
    spl = l.rstrip().split(",")
    variables.append(spl[1])
    try:
        values = [float(x) for x in spl[2].split(";")]
    except:
        values = spl[2].split(";")
    all_values.append(values)

combos = itertools.product(*all_values)

exec_path = settings.LIB_PATH + "simulate_tectos/simulate_set.py"

run_dir = "runs"
if not os.path.isdir(run_dir):
    os.mkdir("runs")

df = pd.DataFrame(columns=variables)
df["run"] = np.nan

pos = 0
for c in combos:
    if not os.path.isdir(run_dir+"/"+str(pos)):
        os.mkdir(run_dir+"/"+str(pos))

    cmd = "python2.7 " + exec_path + " "

    for i, v in enumerate(c):
        if variables[i] == "s" or variables[i] == "n":
            cmd += "-" + variables[i] + " " +  str(int(v)) + " "
        else:
            cmd += "-" + variables[i] + " " +  str(v) + " "

    full_path = os.path.abspath(run_dir+"/"+str(pos)+"/qsub.sh")
    job = qsub_job.QSUBJob(full_path, cmd, walltime="24:00:00")

    values=[]
    values.extend(c)
    values.append(pos)
    df.loc[pos] = values
    pos += 1

df.to_csv("summary.csv", index=False)

