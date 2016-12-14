import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import subprocess
import os

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
    colors = ["#9F8CA6", "#67E568","#257F27","#08420D","#FFF000",
              "#FFB62B","#E56124","#E53E30","#7F2353","#F911FF"]
    markers = ['o', 'v', 's', '^']


    df = _assign_topology_tags(df)

    fig = plt.figure(figsize=(8.5, 6))
    ax = plt.subplot(111)
    topologies = df.topology.unique()


    color_pos = 0
    mark_pos = 0
    for i, top in enumerate(topologies):
        df_sub = df[df.topology == top]
        sns.regplot(x=df_sub.dG_normalized, y=df_sub.dG_predicted, fit_reg=False,
                    scatter_kws={"s": 75}, label=top, color=colors[color_pos],
                    marker=markers[mark_pos])

        color_pos += 1
        if color_pos >= len(colors):
            color_pos = 0
            mark_pos += 1

    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.7, box.height])
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

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
