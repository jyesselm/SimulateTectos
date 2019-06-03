import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import subprocess
import os

import stats

sns.set_style("white")
sns.set_context("talk")

def plot_dG_correlation(df):
    plt.figure()
    return sns.regplot(x="dG_normalized", y="dG_predicted", data=df,
                scatter_kws={"s": 100})


def plot_xy_line(min, max):
    t = np.arange(min, max, 0.01)
    s = t
    return plt.plot(t, s)


# dG correlation by topology plot  ############################################
def _get_toplogy(row, target_fseq_len, target_cseq_len):
    diff_f = (len(row.fss) - target_fseq_len) / 2
    diff_c = (len(row.css) - target_cseq_len) / 2

    return "Flow " + str(10 + diff_f) + " Chip " + str(10 + diff_c)


def _assign_topology_tags(df):
    #length 10 for both fseq and cseq
    target_fseq_len = len("CUAGGAAUCUGGAAGUACCGAGGAAACUCGGUACUUCCUGUGUCCUAG")
    target_cseq_len = len("CTAGGATATGGAAGATCCTCGGGAACGAGGATCTTCCTAAGTCCTAG")

    df_new = df
    df_new["topology"] = df_new.apply(lambda x: _get_toplogy(x, target_fseq_len, target_cseq_len),
                                      axis=1)

    return df_new


def plot_dG_correlation_by_topology(df):
    #colors = ["#9F8CA6", "#67E568","#257F27","#08420D","#FFF000",
    #          "#FFB62B","#E56124","#E53E30","#7F2353","#F911FF"]
    colors = ["#e6194b", "#3cb44b", "#ffe119", "#0082c8", "#f58231", "#911eb4", "#46f0f0"]
    markers = ['o', 'v', 's', '^']


    df = _assign_topology_tags(df)
    df['diff'] = df['dG_normalized'] - df['dG_predicted']

    fig = plt.figure(figsize=(8.5, 6))
    ax = plt.subplot(111)
    topologies = df.topology.unique()

    color_pos = 0
    mark_pos = 0
    topologies = sorted(topologies)
    for i, top in enumerate(topologies):
        df_sub = df[df.topology == top]
        if top == "Flow 10 Chip 12":
            continue

        cat_name = "_".join(top.split())
        df_sub.to_csv(cat_name+".csv")
        print cat_name
        #if top == "Flow 10 Chip 11":
        #    print df_sub.to_csv("flow_10_chip_11.csv")

        print top, stats.get_avg_diff(df_sub.dG_predicted, df_sub.dG_normalized), len(df_sub)
        sns.regplot(x=df_sub.dG, y=df_sub.dG_predicted, fit_reg=False,
                    scatter_kws={"s": 75}, label=top, color=colors[color_pos],
                    marker=markers[mark_pos])
        color_pos += 1
        if color_pos >= len(colors):
            color_pos = 0
            mark_pos += 1

    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.7, box.height])
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    ax.set_aspect('equal', 'datalim')
    x0, x1 = ax.get_xlim()
    #ax.set_ylim(x0, x1)
    y0, y1 = ax.get_ylim()
    ax.plot([x0, x1], [y0, y1], 'k')

    return fig


# tables
###############################################################################

def generate_table(df, fname):
    filename = 'out.tex'
    pdffile = 'out.pdf'

    template = r'''\documentclass[]{{standalone}}
\usepackage{{booktabs}}
\begin{{document}}
{}
\end{{document}}
'''
    with open(filename, 'wb') as f:
        f.write(template.format(df.to_latex()))

    subprocess.call("pdflatex out.tex", shell=True)
    subprocess.call("convert -density 300 out.pdf -quality 90 " + fname, shell=True)
    files = "out.tex out.pdf out.aux out.log".split()
    for f in files:
        os.remove(f)

###############################################################################

def show_plots():
    plt.show()
