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


def build_2_state_next_round():
    org_m = rm.manager.get_motif(name="TWOWAY.1DUQ.7")
    motifs = {}
    f = open("all_motifs.str")
    lines = f.readlines()
    f.close()
    for l in lines:
        m = motif.str_to_motif(l)
        motifs[m.name] = m
        rm.manager.add_motif(motif=m)

    round = 1
    me_dir = "me_round_2_"+str(round)
    if not os.path.isdir(me_dir):
        os.mkdir(me_dir)


    df = pd.read_csv("next_round.csv")
    for i, r in df.iterrows():
        mem_names = r.members.split(',')
        m1 = motifs[mem_names[0]]
        m2 = motifs[mem_names[1]]
        mems = [m1, m2]
        motif_state_ensemble_tree.build_me_sub(org_m, mems, me_dir+"/"+str(i)+".dat")
        if i > 10:
            break



#build_2_state_next_round()
#build_extra_me_files()

i = 0
run_dir = "runs_2_state_1"
if not os.path.isdir(run_dir):
    os.mkdir("runs_2_state_1")

csv_path  = os.path.abspath("TWOWAY.1DUQ.7.csv")
exec_path = settings.LIB_PATH + "simulate_tectos/simulate_set.py"
pos = 0

extra_me_files = glob.glob("me_round_2_1/*")

cmd = ""
for me_file in extra_me_files:
    if not os.path.isdir(run_dir+"/"+str(pos)):
        os.mkdir(run_dir+"/"+str(pos))


    full_me_file = os.path.abspath(me_file)
    full_exec_path = os.path.abspath(run_dir+"/"+str(pos))

    cmd += "cd " + full_exec_path + "\n"
    cmd += "python2.7 " + exec_path + " -csv " + csv_path + " -extra_me "
    cmd += full_me_file + " -n 3\n\n"
    if pos % 5 == 0 and pos != 0:
        full_path = os.path.abspath(run_dir+"/qsub."+str(pos)+".sh")
        print full_path
        job = qsub_job.QSUBJob(full_path, cmd, walltime="24:00:00")
        #job.submit()
        cmd = ""
    pos += 1
