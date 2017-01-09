import argparse
import pandas as pd
from pandas.tools.plotting import table
import matplotlib.pyplot as plt

from simulate_tectos import analysis, stats, plot

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import subprocess

sns.set(style="white", context="talk", font_scale=1.5)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-dir', help='sweep directory')
    args = parser.parse_args()

    return args


def get_results(dir):
    spl = dir.split(",")
    df = pd.read_csv(spl[0]+"/results/results_sorted.csv")
    return df


def split_results(df):
    df_al = df[df.csv == "/home/jyesselm/projects/RNAMake.projects/SimulateTectos/data/all_lengths.csv"]
    df_hv = df[df.csv == "/home/jyesselm/projects/RNAMake.projects/SimulateTectos/data/helical_variation_subset.csv"]

    return df_al, df_hv


def plot_org():
    df = analysis.get_summary_df("results.csv")
    df = df[(df.eminus < 0.5) & (df.eplus < 0.5)]
    print stats.r2(df.dG_predicted, df.dG_normalized)
    print stats.get_avg_diff(df.dG_predicted, df.dG_normalized)
    plot.plot_dG_correlation(df)
    plot.show_plots()


def get_scatters(df, name):
    #params = "s,simulation.temperature,simulation.steric_radius,simulation.cutoff,n".split(",")
    params = "s,simulation.steric_radius,simulation.cutoff,n".split(",")

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


def get_heatmap(df, x, y, z, name):
    df_new = pd.DataFrame(columns=(x, y, z))
    pos = 0

    groups = df.groupby([x, y])
    for gname, group in groups:
        df_new.loc[pos] = [group[x].unique()[0], group[y].unique()[0], group[z].mean()]
        pos += 1

    df_new = df_new.pivot(x, y, z)

    sns.heatmap(df_new, cmap="jet")
    plt.savefig("plots/heatmap."+name+"_"+x+"_"+y+"_"+z+".png")
    plt.clf()


def get_heatmaps(df, name):
    #params = "s,simulation.temperature,simulation.steric_radius,simulation.cutoff,n".split(",")
    params = "s,simulation.steric_radius,simulation.cutoff,n".split(",")

    depend = "r2,avg_diff".split(",")

    for i in range(0, len(params)):
        for j in range(i+1, len(params)):
            for d in depend:
                get_heatmap(df, params[i], params[j], d, name)


if __name__ == "__main__":
    args = parse_args()
    df = get_results(args.dir)
    df_al, df_hv = split_results(df)

    df_hv = df_hv[df_hv.apply(lambda x : (x["simulation.cutoff"] > 4) & \
                                         (x["simulation.temperature"] == 250) & \
                                         (x["s"] == 1000000), axis=1)]
    df_hv = df_hv.sort(["r2"], ascending=[0])
    top_row = df_hv.iloc[0]

    df_run = pd.read_csv("sweep_1/results/output_csvs/"+str(int(top_row.run))+".csv")
    sns.regplot(x="avg_hit_count", y="dG", data=df_run, fit_reg=False, scatter_kws={'s' : 100})

    print top_row

    plt.figure()
    new_row = df_hv.iloc[10]
    df_run = pd.read_csv("sweep_1/results/output_csvs/"+str(int(new_row.run))+".csv")
    sns.regplot(x="avg_hit_count", y="dG", data=df_run, fit_reg=False, scatter_kws={'s' : 100})

    print new_row

    plt.show()


    #df = pd.read_csv(args.dir + "/results/results_sorted.csv")


#plot.plot_dG_correlation(df_sum)
#print stats.   r2(df_sum.dG_predicted, df_sum.dG_normalized)
#print stats.get_avg_diff(df_sum.dG_predicted, df_sum.dG_normalized)
#plot.show_plots()

#df = pd.read_csv("output_csvs/1850.csv")
#plot.plot_dG_correlation_by_topology(df)
#plot.show_plots()


exit()



get_scatters(df, "helical_variation")
get_scatters(df, "all_lengths")

generate_best_table(df_al, 10, "plots/all_lengths_top.png")
generate_best_table(df_hv, 10, "plots/helical_variation_top.png")

get_heatmaps(df_al, "all_lengths")
get_heatmaps(df_hv, "helical_variation")
