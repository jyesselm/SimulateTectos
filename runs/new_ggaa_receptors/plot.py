
import pandas as pd
from simulate_tectos import stats, plot


target_fseq = len("CUAGGAAUCUGGAAGUACCGAGGAAACUCGGUACUUCCUGUGUCCUAG")
target_cseq = len("CTAGGATATGGAAGATCCTCGGGAACGAGGATCTTCCTAAGTCCTAG")

df = pd.read_csv("org_wc10bp_results.csv")
#df = df[(df.cseq.str.len() == target_cseq) | (df.cseq.str.len() == target_cseq+2)]


plot.plot_dG_correlation(df)
plot.plot_dG_correlation(pd.read_csv("output_csvs/130.csv"))
plot.show_plots()