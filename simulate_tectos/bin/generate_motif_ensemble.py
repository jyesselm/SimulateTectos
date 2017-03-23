import pandas as pd
import sys
import argparse

from rnamake import resource_manager as rm
from rnamake import motif_ensemble, vienna, util


flow_seqs = {"WC9bp": 'CUAGGAAUCUGGAAGACCGAGGAAACUCGGUCUUCCUGUGUCCUAG',
             "WC10bp": 'CUAGGAAUCUGGAAGUACCGAGGAAACUCGGUACUUCCUGUGUCCUAG',
             "WC11bp": 'CUAGGAAUCUGGAAGUACACGAGGAAACUCGUGUACUUCCUGUGUCCUAG'}

flow_ss =   {'WC9bp': "((((((....(((((((((((....)))))))))))....))))))",
             'WC10bp': "((((((....((((((((((((....))))))))))))....))))))",
             'WC11bp': "((((((....(((((((((((((....)))))))))))))....))))))"}


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-csv', help='dataframe in csv format', required=True)
    parser.add_argument('-sequences', help='sequences to be ran as ensemble test')
    parser.add_argument('-me_outfile', default='test.dat', help='name of motif ensemble file')
    parser.add_argument('-run_outfile', default='run.csv', help='csv file to be used in simulate_set.py')

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


args = parse_args()
motifs = []

df = pd.read_csv(args.csv)
if not is_valid_table(df):
    cols = "pdb_id side1 side2"
    raise ValueError("not valid pandas table supplied as csv. required columns are " + cols)


for i, r in df.iterrows():
    m = get_motif_from_row(r)
    if m is not None:
        motifs.append(m)

start_m = motifs[0]
fname = util.filename(args.csv)

print "# of ensemble members:", len(motifs)
build_me_sub(start_m, motifs, [1 for x in range(len(motifs))], args.me_outfile)

if not args.sequences:
    exit(0)

f = open(args.sequences)
lines = f.readlines()
f.close()

rep_seqs = start_m.sequence().split("&")
rep_ss = start_m.dot_bracket().split("&")
length = len(rep_seqs[0])
if len(rep_seqs[1]) < length:
    length = len(rep_seqs[1])


df_run = pd.DataFrame(columns="cseq css fseq fss fname extra_me type".split())
loc_pos = 0
v = vienna.Vienna()
for l in lines:
    spl = l.rstrip().split("N")
    peices = []
    for e in spl:
        if len(e) > 1:
            peices.append(e)

    first = "".join(["G" for x in range(length)])
    second = "".join(["C" for x in range(length)])
    seq = peices[0] + first + peices[1] + second + peices[2]
    ss = v.fold(seq).structure

    for flow_name, flow_seq in flow_seqs.iteritems():
        df_run.loc[loc_pos] = [seq, ss, flow_seq, flow_ss[flow_name], flow_name, args.me_outfile, "HELIX"]
        loc_pos += 1

    pos2 =  seq.find(peices[1])
    pos3 =  seq.find(peices[2])

    m_seq =  peices[0] + rep_seqs[0] + peices[1] + rep_seqs[1] + peices[2]
    m_ss  =  ss[0:len(peices[0])] + rep_ss[0] + ss[pos2:pos2+len(peices[1])] + rep_ss[1] + ss[pos3:]

    for flow_name, flow_seq in flow_seqs.iteritems():
        df_run.loc[loc_pos] = [m_seq, m_ss, flow_seq, flow_ss[flow_name], flow_name, args.me_outfile, "MOTIF"]
        loc_pos += 1


df_run.to_csv(args.run_outfile, index=False)
print "done!, run:"
print "python simulate_set.py -csv " + args.run_outfile































