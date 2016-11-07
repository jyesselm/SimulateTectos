import glob
import os
import random
import pandas as pd
from rnamake import motif, sqlite_library, motif_state_ensemble_tree
from rnamake import resource_manager as rm
from rnamake.submit import qsub_job
from simulate_tectos import settings

def build_extra_me_files():

    path = "/Users/josephyesselman/projects/RNAMake.projects/tecto_ensemble_generation"
    m_files = glob.glob(path+"/test.*.str")

    org_m = rm.manager.get_motif(name="TWOWAY.1DUQ.7")
    org_m.to_pdb("org.pdb")
    for i, m_file in enumerate(m_files):
        m = motif.file_to_motif(m_file)
        if len(m.ends) != 2:
            continue
        m.name = "TWOWAY.1DUQ.7.euler."+str(i)
        m.to_pdb("test."+str(i)+".pdb")
        rm.manager.add_motif(motif=m)

        motif_state_ensemble_tree.build_me_sub(org_m, [m], "extra_me_files/"+str(i)+".dat")

def run_single_state():
    i = 0
    run_dir = "runs"
    if not os.path.isdir(run_dir):
        os.mkdir("runs")

    csv_path  = os.path.abspath("TWOWAY.1DUQ.7.csv")
    exec_path = settings.LIB_PATH + "simulate_tectos/simulate_set.py"
    pos = 0

    extra_me_files = glob.glob("extra_me_files/*")

    for me_file in extra_me_files:
        if not os.path.isdir(run_dir+"/"+str(pos)):
            os.mkdir(run_dir+"/"+str(pos))

        full_path = os.path.abspath(run_dir+"/"+str(pos)+"/qsub.sh")
        full_me_file = os.path.abspath(me_file)

        cmd  = "python2.7 " + exec_path + " -csv " + csv_path + " -extra_me "
        cmd += full_me_file + " -n 3"
        job = qsub_job.QSUBJob(full_path, cmd, walltime="24:00:00")
        job.submit()
        pos += 1


def build_2_state_extra_me_files():
    if not os.path.isdir("me_round_2"):
        os.mkdir("me_round_2")


    org_m = rm.manager.get_motif(name="TWOWAY.1DUQ.7")
    motifs = []
    f = open("all_motifs.str")
    lines = f.readlines()
    f.close()
    for l in lines:
        motifs.append(motif.str_to_motif(l))
    for m in motifs:
        rm.manager.add_motif(motif=m)

    combos = []

    for i in range(10000):
        m1 = random.choice(motifs)
        m2 = random.choice(motifs)
        mems = [m1, m2]
        motif_state_ensemble_tree.build_me_sub(org_m, mems, "me_round_2/"+str(i)+".dat")




build_2_state_extra_me_files()

i = 0
run_dir = "runs_2_state"
if not os.path.isdir(run_dir):
    os.mkdir("runs_2_state")

csv_path  = os.path.abspath("TWOWAY.1DUQ.7.csv")
exec_path = settings.LIB_PATH + "simulate_tectos/simulate_set.py"
pos = 0

extra_me_files = glob.glob("me_round_2/*")

for me_file in extra_me_files:
    if not os.path.isdir(run_dir+"/"+str(pos)):
        os.mkdir(run_dir+"/"+str(pos))

    full_path = os.path.abspath(run_dir+"/"+str(pos)+"/qsub.sh")
    full_me_file = os.path.abspath(me_file)

    cmd  = "python2.7 " + exec_path + " -csv " + csv_path + " -extra_me "
    cmd += full_me_file + " -n 3"
    job = qsub_job.QSUBJob(full_path, cmd, walltime="24:00:00")
    #job.submit()
    pos += 1
