from rnamake.submit import qsub_job
from simulate_tectos import settings
import glob
import os

data_path = settings.DATA_PATH
length_csv_files = glob.glob(data_path+"WC*")
ggaa_motifs = glob.glob(data_path+"/ggaa_models/*")

i = 0
run_dir = "runs"
if not os.path.isdir(run_dir):
    os.mkdir("runs")

exec_path = settings.LIB_PATH + "simulate_tectos/simulate_set.py"
pos = 0
for m_path in ggaa_motifs:
    for csv in length_csv_files:
        if not os.path.isdir(run_dir+"/"+str(pos)):
            os.mkdir(run_dir+"/"+str(pos))
        full_path = os.path.abspath(run_dir+"/"+str(pos)+"/qsub.sh")
        cmd  = "python " + exec_path + " -csv " + csv + " -new_ggaa_model "
        cmd += "-ggaa_model " + m_path
        job = qsub_job.QSUBJob(full_path, cmd, walltime="12:00:00")
