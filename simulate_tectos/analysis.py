import math
import pandas as pd
import numpy as np

def get_norm_sequence(df):
    mean = df["avg_hit_count"].mean()
    closest_row = ""
    closest_score = 10000

    for i, row in df.iterrows():
        diff = abs(row['avg_hit_count'] - mean)
        if diff < closest_score:
            closest_score = diff
            closest_row = row

    return closest_row


def get_summary_df(csv_file, norm_seq=None):

    df = pd.read_csv(csv_file)
    df = df[df.apply(lambda x:  x['avg_hit_count'] != -1, axis=1)]

    if not norm_seq:
        norm_row = get_norm_sequence(df)
    else:
        row = None
        if 'sequence' in df:
            row = 'sequence'
        elif 'cseq' in df:
            row = 'cseq'
        else:
            raise ValueError(
                "dont know what column holds sequence! valid ones are sequence and cseq")


        norm_df = df[df[row] == norm_seq]
        norm_row = None
        for i, r in norm_df.iterrows():
            norm_row = r
            break

        if norm_row is None:
            raise ValueError("cannot find norm sequence: " + norm_seq)


    df = df[df.apply(lambda x:  not pd.isnull(x['dG']), axis=1)]

    df['dG_normalized'] = df['dG'] - norm_row['dG']

    dG_predicted = []
    for i, row in df.iterrows():
        try:
            prediction = 1.9872041e-3*298*math.log(float(norm_row['avg_hit_count'])/float(row['avg_hit_count']))
            dG_predicted.append(prediction)
        except:
            dG_predicted.append(np.nan)

    df['dG_predicted'] = dG_predicted
    df = df[df.apply(lambda x:  not pd.isnull(x['dG_predicted']), axis=1)]
    return df