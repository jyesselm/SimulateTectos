import os
import glob
import itertools
import pandas as pd

from rnamake import motif_factory, motif_state_ensemble_tree
from rnamake import resource_manager as rm


def generate_tar_ensemble():

    pdbs = glob.glob("ensemble/*/*.pdb")

    motifs = []

    for j, pdb in enumerate(pdbs):
        if j == 130:
            continue
        m = motif_factory.factory.motif_from_file(pdb)
        res_nums = [5, 6, 7, 8, 9, 10, 23, 24, 25]
        res = [ m.get_residue(num=i) for i in res_nums]
        bps = []
        for bp in m.basepairs:
            if bp.res1 in res and bp.res2 in res and bp.bp_type == "cW-W":
                bps.append(bp)

        try:
            m_sub = motif_factory.factory.motif_from_res(res, bps)
        except:
            continue
        m_sub.name = m.name
        if len(m_sub.ends) != 2:
            continue
        m_aligned = motif_factory.factory.can_align_motif_to_end(m_sub, 0)
        if m_aligned is None:
            continue
        m_aligned = motif_factory.factory.align_motif_to_common_frame(m_aligned, 0)
        #m_aligned.to_pdb("m."+str(j)+".pdb")
        rm.manager.add_motif(motif=m_aligned)
        motifs.append(m_aligned)

    start_m = motifs[0]
    s = start_m.to_str()
    f = open("start_tar.motif", "w")
    f.write(s)
    f.close()

    #motif_state_ensemble_tree.build_me_sub(start_m, motifs, "tar.dat")

prime5_seq = "CUAGGAUAUGG"
prime5_ss  = "(((((((..(("

prime3_seq = "CCUAAGUCCUAG"
prime3_ss  = "))...)))))))"

mid_seq = "GGGAAC"
mid_ss  = "(....)"

tar_seqs = ["GAUCUG","CUC"]
tar_ss   = ["(....(",").)"]

possibles = [
    [["A", "U"], ["(", ")"]],
    [["U", "A"], ["(", ")"]],
    [["G", "C"], ["(", ")"]],
    [["C", "G"], ["(", ")"]],
    [["GAUCUG","CUC"], ["(....(",").)"]]
]

df = pd.DataFrame(columns="cseq css".split())
pos = 0

combos = itertools.product(possibles, possibles, possibles, possibles, possibles, possibles)
i = 0
for c in combos:
    seq_1 = prime5_seq
    ss_1  = prime5_ss

    seq_2 = prime3_seq
    ss_2  = prime3_ss

    seen_tar = 0
    for e in c:
        if len(e[0][0]) > 1:
            seen_tar += 1

        seq_1 += e[0][0]
        ss_1  += e[1][0]

        seq_2 = e[0][1] + seq_2
        ss_2  = e[1][1] + ss_2

    if seen_tar != 1:
        continue

    seq = seq_1 + mid_seq + seq_2
    ss  = ss_1  + mid_ss  + ss_2

    df.loc[pos] = [seq, ss]
    pos += 1

    i += 1

df.to_csv("tar_constructs.csv", index=False)

