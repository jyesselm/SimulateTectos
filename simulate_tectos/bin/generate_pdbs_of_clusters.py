from rnamake import resource_manager as rm
from rnamake import motif_tree, util, basic_io, motif
import argparse
import os
import numpy as np
import pandas as pd

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-csv', help='dataframe in csv format', required=True)
    parser.add_argument('-cluster_dir', default="clusters", help='location of output pdbs')

    args = parser.parse_args()

    f_extension = args.csv[-4:]
    if f_extension != ".csv":
        raise ValueError("file supplied with -csv does not have a .csv extension")

    return args


def is_valid_table(df):
    cols = "pdb_id side1 side2 cluster flank1_5prime flank1_3prime flank2_5prime flank2_3prime side1_all side2_all".split()
    for col in cols:
        if col not in df:
            return 0
    return 1


def get_motif_from_row(r):
    m = None
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
    return rs


def get_motif_from_seq(r):
    bp_step_names = get_bp_steps_from_seqs(r.side1, r.side2)
    motifs = []
    for bp_step_name in bp_step_names:
        motifs.append(rm.manager.get_bp_step(bp_step_name))

    mt = motif_tree.MotifTree()
    for m in motifs:
        mt.add_motif(m)

    rs = mt.get_structure()
    rs.name = r.side1+"="+r.side2
    if motifs[0].ends[0].name() != rs.ends[0].name():
       rs.ends = rs.ends[::-1]


    m = motif.Motif(r_struct=rs)
    m.name = r.side1+"="+r.side2
    return m

args = parse_args()
df = pd.read_csv(args.csv)
r = is_valid_table(df)
if r == 0:
    cols = "pdb_id side1 side2 cluster flank1_5prime flank1_3prime flank2_5prime flank2_3prime side1_all side2_all"
    raise ValueError(args.csv + " table is not valid required columns are: " + cols)

motifs = {}
diff = []
rot_diff = []
origin = np.array([0, 0, 0])
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
    #print rs.name + "." + r.side1_all + "." + r.side2_all
    motifs[rs.name + "." + r.side1_all + "." + r.side2_all] = rs

    dist_1 = util.distance(origin, rs.ends[0].d())
    dist_2 = util.distance(origin, rs.ends[1].d())

    if dist_1 > dist_2:
        diff.append(basic_io.point_to_str(rs.ends[0].d()))
        rot_diff.append(basic_io.matrix_to_str(rs.ends[0].r()))
    else:
        diff.append(basic_io.point_to_str(rs.ends[1].d()))
        rot_diff.append(basic_io.matrix_to_str(rs.ends[1].r()))


#df['translation'] = diff
#df['rotation'] = rot_diff

#fname = util.filename(args.csv)
#df.to_csv(fname[:-4]+"_diff.csv", index=False)

groups = df.groupby(['cluster'])
if not os.path.isdir(args.cluster_dir):
    os.mkdir(args.cluster_dir)

for g in groups:
    d =args.cluster_dir + '/' + str(int(g[0]))
    print d
    try:
        os.mkdir(d)
    except:
        pass

    for i, r in g[1].iterrows():
        name = r.side1 + "=" + r.side2
        try:
            m = motifs[name+"."+r.side1_all+"."+r.side2_all]
        except:
            continue
        m.to_pdb(d+"/"+name+"."+r.side1_all+"."+r.side2_all+".pdb", renumber=1, close_chain=1)


