import pandas as pd
import numpy as np

df = pd.read_csv("round_2_results.csv")
df = df.dropna()

df['weight'] = df['r2']*3 - df['avg_diff']
df.ix[df.weight < 0, 'weight'] = 0.01
#weights = df['weight']

df_new = pd.DataFrame(
            columns="members p1_members p2_members p1_r2 p2_r2 p1_avg_diff p2_avg_diff".split())

pos = 0
seen = {}
for i in range(2500):
    s = df.sample(n=2, weights=df.weight)
    p1 = s.iloc[0]
    p2 = s.iloc[1]

    p1_members = p1.members.split(",")
    p2_members = p2.members.split(",")

    for j in range(0, 2):
        for k in range(0, 2):
            child_mem = ",".join([p1_members[j], p2_members[k]])
            if child_mem  in seen:
                continue
            seen[child_mem] = 1

            child = [child_mem, p1.members, p2.members, p1.r2, p2.r2, p1.avg_diff, p2.avg_diff]
            df_new.loc[pos] = child
            pos += 1

df_new.to_csv("next_round.csv")



