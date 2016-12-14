
import pandas as pd
from simulate_tectos import stats, analysis, plot
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_style("white")
sns.set_context("talk")
#sns.set(style="ticks", color_codes=True) # change style

def get_all_wc_data():
    df1 = pd.read_csv("results/org_wc10bp.csv")
    df2 = pd.read_csv("results/org_wc11bp.csv")
    df3 = pd.read_csv("results/org_wc9bp.csv")
    frames = [df1, df2, df3]
    df = pd.concat(frames)
    df.to_csv("results/org_wcall.csv",index=False)
    df_sum = analysis.get_summary_df("results/org_wcall.csv")
    df_sum.to_csv("results/org_wcall_results.csv")



df = pd.read_csv("results/org_wcall_results.csv")
#print stats.r2(df.dG_predicted, df.dG_normalized), stats.get_avg_diff(df.dG_predicted, df.dG_normalized)
#fig = plot.plot_dG_correlation_by_topology(df)

#plot.show_plots()


#df_sum = analysis.get_summary_df("results/org_wcall.csv")
#plot.plot_dG_correlation(df_sum)
#plot.show_plots()

