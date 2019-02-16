import pandas as pd
import sys
import argparse
import glob

from rnamake import resource_manager as rm
from rnamake import motif_ensemble, vienna, util

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-pdb_dir', help='directory of pdbs', required=True)
    parser.add_argument('-weights', help='directory of pdbs')

    args = parser.parse_args()

    return args

def build_me_sub(org_m, new_motifs, scores, extra_mse_file="test.dat"):
    f = open(extra_mse_file, "w")

    for i, end in enumerate(org_m.ends):
        all_ms = []
        all_scores = []

        for j, new_m in enumerate(new_motifs):
            try:
                mi = rm.manager.get_motif(name=new_m.name, end_name=new_m.ends[i].name())
            except:
                continue

            try:
                mi.to_str()
            except:
                continue

            all_ms.append(mi)
            all_scores.append(scores[j])

        me = motif_ensemble.MotifEnsemble()
        me.setup(org_m.end_ids[i], all_ms, all_scores)
        org_m_key = org_m.name + "-" + end.name()

        f.write(org_m_key + "!!" + me.to_str() + "\n")


    f.flush()
    f.close()

def parse_weights_file(weights_file):
    f = open(weights_file)
    lines = f.readlines()
    f.close()

    d = {}
    for l in lines:
        spl = l.split()
        if len(spl) < 2:
            continue
        d[spl[0]] = float(spl[1])
    return d


if __name__ == '__main__':
    args = parse_args()

    name = "test_motif"

    pdbs = glob.glob(args.pdb_dir + "/*.pdb")
    motifs = []
    scores = []

    start_m = rm.manager.get_structure(pdbs[0], name)

    # needs a new motif name for RNAMAke to recognize this sequence / secondary structure
    org_m = start_m
    needs_new_motif = False
    try:
        m = rm.manager.get_motif(end_id=start_m.end_ids[0])
        org_m = m
    except:
        needs_new_motif = True

    score_dict = {}
    if args.weights:
        score_dict = parse_weights_file(args.weights)

    for pdb in pdbs:
        pdb_name = util.filename(pdb)
        rm.manager.add_motif(pdb, name=pdb_name, remove_extra_bps=1)

        if pdb_name in score_dict:
            scores.append(score_dict[pdb_name])
        else:
            scores.append(1)

        motifs.append(rm.manager.get_motif(name=pdb_name))

    build_me_sub(org_m, motifs, scores)



























