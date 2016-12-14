
import pandas as pd
from pandas.tools.plotting import table
import matplotlib.pyplot as plt

from simulate_tectos import analysis, stats, plot

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import subprocess

sns.set(style="white", context="talk", font_scale=1.5)

def plot_org():
    df = analysis.get_summary_df("results.csv")
    df = df[(df.eminus < 0.5) & (df.eplus < 0.5)]
    print stats.r2(df.dG_predicted, df.dG_normalized)
    print stats.get_avg_diff(df.dG_predicted, df.dG_normalized)
    plot.plot_dG_correlation(df)
    plot.show_plots()


def get_scatters(df, name):
    params = "s,simulation.temperature,simulation.steric_radius,simulation.cutoff,n".split(",")
    depend = "r2,avg_diff".split(",")

    for x in params:
        for y in depend:
            sns.regplot(x=x, y=y, data=df)
            plt.savefig("plots/scatter."+name+"."+x+"."+y+".png")
            compare_name = name+"."+x+"."+y
            print compare_name, stats.r2(df[x], df[y])
            plt.clf()


def generate_best_table(df, size, path):
    df = df.sort(["r2", "avg_diff"], ascending=[0, 1])
    df = df.drop('csv', axis=1)
    plot.generate_table(df[:size], path)


def get_heatmaps(df, name):
    df_new = pd.DataFrame(columns="simulation.cutoff n r2".split())
    pos = 0

    groups = df.groupby(['simulation.cutoff', 'n'])
    for name, group in groups:
        df_new.loc[pos] = [group["simulation.cutoff"].unique()[0], group.n.unique()[0], group.r2.mean()]
        pos += 1

    df_new = df_new.pivot("simulation.cutoff", "n", "r2")

    sns.heatmap(df_new, cmap="jet")
    plt.show()

#plot.plot_dG_correlation(df_sum)
#print stats.r2(df_sum.dG_predicted, df_sum.dG_normalized)
#print stats.get_avg_diff(df_sum.dG_predicted, df_sum.dG_normalized)
#plot.show_plots()

#df = pd.read_csv("output_csvs/1850.csv")
#plot.plot_dG_correlation_by_topology(df)
#plot.show_plots()


df = pd.read_csv("results_sorted.csv")
df_al = df[df.csv == "/home/jyesselm/projects/RNAMake.projects/SimulateTectos/data/all_lengths.csv"]
df_hv = df[df.csv == "/home/jyesselm/projects/RNAMake.projects/SimulateTectos/data/helical_variation_subset.csv"]


#get_scatters(df, "helical_variation")
#get_scatters(df, "all_lengths")

#generate_best_table(df_al, 10, "plots/all_lengths_top.png")
#generate_best_table(df_hv, 10, "plots/helical_variation_top.png")


