import unittest
import os
import pandas as pd

from simulate_tectos import analysis, stats

class AnalysisUnittests(unittest.TestCase):

    def test(self):
        df_sum = analysis.get_summary_df("resources/control.csv")
       #print stats.r2(df_sum['dG_predicted'], df_sum['dG_normalized'])



def main():
    unittest.main()

if __name__ == '__main__':
    main()