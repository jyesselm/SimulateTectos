import glob
import os
from rnamake import motif, sqlite_library, motif_state_ensemble_tree
from rnamake import resource_manager as rm
from rnamake.submit import qsub_job
from simulate_tectos import settings

def build_extra_me_files():

    path = "/Users/josephyesselman/projects/RNAMake.projects/tecto_ensemble_generation"
    m_files = glob.glob(path+"/test.*.str")

    mlib = sqlite_library.MotifSqliteLibrary("twoway")
    org_m = rm.manager.get_motif(name="TWOWAY.1DUQ.7")
    org_m.to_pdb("org.pdb")
    for i, m_file in enumerate(m_files):
        m = motif.file_to_motif(m_file)
        if len(m.ends) != 2:
            continue
        m.name = "TWOWAY.1DUQ.7.euler."+str(i)
        rm.manager.add_motif(motif=m)

        motif_state_ensemble_tree.build_me_sub(org_m, [m], "extra_me_files/"+str(i)+".dat")

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
