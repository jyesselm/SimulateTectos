import math
import pandas as pd
import numpy as np
from scipy.stats import linregress
from rnamake import motif, motif_factory, util, basic_io
from rnamake import transformations as t

def get_norm(df):
    mean = df["avg_hit_count"].mean()
    return mean


def compute_dG_predicted(df):
    pass

def get_summary_df(csv_file, norm_seq=None):

    df = pd.read_csv(csv_file)
    df = df[df.apply(lambda x:  x['avg_hit_count'] != -1, axis=1)]

    df = df[df.apply(lambda x:  not pd.isnull(x['dG']), axis=1)]
    norm = get_norm(df)

    dG_predicted = []
    for i, row in df.iterrows():
        try:
            prediction = 1.9872041e-3*298*math.log(float(norm)/float(row['avg_hit_count']))
            dG_predicted.append(prediction)
        except:
            dG_predicted.append(np.nan)

    df['dG_predicted'] = dG_predicted
    df = df[df.apply(lambda x:  not pd.isnull(x['dG_predicted']), axis=1)]

    # offset data to give lowest RMSD
    lr = linregress(df.dG_predicted, df.dG)
    df['dG_normalized'] = df['dG'] - lr.intercept

    return df

def to_deg(rad):
    return rad*180/math.pi

def compute_6d_params(fname):
    df = pd.DataFrame(columns='x y z a b g'.split())

    f = open(fname)
    lines = f.readlines()
    f.close()
    pos = 0

    ref_r = motif_factory.factory.ref_motif.ends[0].r()

    for i, l in enumerate(lines):
        if i == 0:
            continue
        spl = l.split(",")
        d1 = basic_io.str_to_point(spl[0])
        r1 = basic_io.str_to_matrix(spl[1])
        d2 = basic_io.str_to_point(spl[2])
        r2 = basic_io.str_to_matrix(spl[3])

        rot = util.unitarize(ref_r.T.dot(r1)).T
        r1_trans = np.dot(r1, rot)
        r2_trans = np.dot(r2, rot)

        r = util.unitarize(r1_trans.T.dot(r2_trans))
        d = d2 - d1
        euler = [to_deg(x) for x in t.euler_from_matrix(r, 'rxyz')]
        df.loc[pos] = [d[0], d[1], d[2], euler[0], euler[1], euler[2]]
        pos += 1

    return df
