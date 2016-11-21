from simulate_tectos import analysis, stats, plot


df = analysis.get_summary_df("org_wc11bp.csv")
df.to_csv("org_wc11bp_results.csv")
r2 = stats.r2(df["dG_normalized"], df["dG_predicted"])
print r2
plot.plot_dG_correlation(df)
plot.show_plots()