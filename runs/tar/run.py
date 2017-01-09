import os
import pandas as pd
import numpy as np

from rnamake.submit import qsub_job
from simulate_tectos import settings

exec_path = settings.LIB_PATH + "simulate_tectos/simulate_set.py"
full_me_file = os.path.abspath("tar.dat")
full_motif_paths = os.path.abspath("start_tar.motif")

run_dir = "runs"
if not os.path.isdir(run_dir):
    os.mkdir("runs")

df = pd.read_csv("tar_constructs.csv")

dfs = np.array_split(df, 50)

for i, run_df in enumerate(dfs):
    if not os.path.isdir(run_dir+"/"+str(i)):
        os.mkdir(run_dir+"/"+str(i))

    cmd = "python2.7 " + exec_path + " "
    cmd += "-csv " + " set.csv "
    cmd += "-extra_me " + full_me_file + " -extra_motifs " + full_motif_paths
    run_df.to_csv(run_dir+"/"+str(i)+"/set.csv")

    full_path = os.path.abspath(run_dir+"/"+str(i)+"/qsub.sh")
    job = qsub_job.QSUBJob(full_path, cmd, walltime="10:00:00")