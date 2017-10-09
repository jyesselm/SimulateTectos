import pandas as pd
import sys
import argparse

from rnamake import resource_manager as rm
from rnamake import motif_ensemble, vienna, util, motif_tree, motif, motif_factory


flow_seqs = {"WC9bp": 'CUAGGAAUCUGGAAGACCGAGGAAACUCGGUCUUCCUGUGUCCUAG',
             "WC10bp": 'CUAGGAAUCUGGAAGUACCGAGGAAACUCGGUACUUCCUGUGUCCUAG',
             "WC11bp": 'CUAGGAAUCUGGAAGUACACGAGGAAACUCGUGUACUUCCUGUGUCCUAG'}

flow_ss =   {'WC9bp': "((((((....(((((((((((....)))))))))))....))))))",
             'WC10bp': "((((((....((((((((((((....))))))))))))....))))))",
             'WC11bp': "((((((....(((((((((((((....)))))))))))))....))))))"}


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-csv', help='dataframe in csv format', required=True)
    parser.add_argument('-me_outfile', default='test.dat', help='name of motif ensemble file')

    args = parser.parse_args()

    f_extension = args.csv[-4:]
    if f_extension != ".csv":
        raise ValueError("file supplied with -csv does not have a .csv extension")

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


def is_valid_table(df):
    cols = "pdb_id side1 side2".split()
    for col in cols:
        if col not in df:
            return 0
    return 1


def get_motif_from_row(r):
    try:
        m = rm.manager.get_motif(name=r.pdb_id)
    except:
        return None

    seqs = m.sequence().split("&")
    if seqs[0] == r.side1 and seqs[1] == r.side2:
        return m
    elif seqs[1] == r.side1 and seqs[0] == r.side2:
        m = rm.manager.get_motif(name=r.pdb_id, end_name=m.ends[1].name())
        return m


def get_final_flank_sequences(flank_5p, flank_3p, m_seq):
    if not pd.isnull(flank_5p):
        flank_5p_final = flank_5p+m_seq[0]
    else:
        flank_5p_final = ''

    if not pd.isnull(flank_3p):
        flank_3p_final = m_seq[-1] + flank_3p
    else:
        flank_3p_final = ''

    return flank_5p_final, flank_3p_final


def get_bp_steps_from_seqs(prime5, prime3):
    bp_steps = []
    j = len(prime5) - 1
    for i in range(len(prime5) - 1):
        bp_step = prime5[i] + prime5[i + 1] + "_" + "LL" + "_" + prime3[j - 1] + prime3[j] + "_RR"
        j -= 1
        bp_steps.append(bp_step)

    return bp_steps


def get_combined_structure(front_bps, end_bps, m):
    mt = motif_tree.MotifTree()
    for bp_step_name in front_bps:
        mt.add_motif(rm.manager.get_bp_step(bp_step_name))
    mt.add_motif(m)
    for bp_step_name in end_bps:
        mt.add_motif(rm.manager.get_bp_step(bp_step_name))
    rs = mt.get_structure()
    rs.name = m.name
    motif_factory.factory._setup_secondary_structure(rs)
    return rs

args = parse_args()
motifs = []

df = pd.read_csv(args.csv)
if not is_valid_table(df):
    cols = "pdb_id side1 side2"
    raise ValueError("not valid pandas table supplied as csv. required columns are " + cols)

for i, r in df.iterrows():
    if pd.notnull(r.pdb_id):
        m = get_motif_from_row(r)
    else:
        m = get_motif_from_seq(r)

    if m is None or pd.isnull(r.side1_all):
        rot_diff.append(-1)
        diff.append(-1)
        continue
    m.name = r.side1+"="+r.side2

    seqs = m.sequence().split("&")
    flank1_5prime, flank1_3prime = get_final_flank_sequences(r.flank1_5prime, r.flank1_3prime, seqs[0])
    flank2_5prime, flank2_3prime = get_final_flank_sequences(r.flank2_5prime, r.flank2_3prime, seqs[1])
    front_bps = get_bp_steps_from_seqs(flank1_5prime, flank2_3prime)
    end_bps = get_bp_steps_from_seqs(flank1_3prime, flank2_5prime)
    rs = get_combined_structure(front_bps, end_bps, m)
    n_motif = motif.Motif(r_struct=rs)
    if i != 0:
        rm.manager.add_motif(motif=n_motif)
    motifs.append(n_motif)

start_m = motifs.pop(0)
fname = util.filename(args.csv)

print "# of ensemble members:", len(motifs)
build_me_sub(start_m, motifs, [1 for x in range(len(motifs))], args.me_outfile)
































