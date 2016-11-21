from simulate_tectos import stats, plot
import pandas as pd

target_fseq = len("CUAGGAAUCUGGAAGUACCGAGGAAACUCGGUACUUCCUGUGUCCUAG")
target_cseq = len("CTAGGATATGGAAGATCCTCGGGAACGAGGATCTTCCTAAGTCCTAG")

df = pd.read_csv("org_wc10bp_results.csv")
df_org = df[(df.cseq.str.len() == target_cseq) | (df.cseq.str.len() == target_cseq+2)]

results_df = pd.read_csv("all_results.csv")
results_df = results_df[results_df.r2 != -1.0]

bp10_results = results_df[results_df.data_set == "WC10bp_all_lengths.csv"]
print bp10_results