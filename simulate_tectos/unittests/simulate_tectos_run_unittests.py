import unittest
import os
import pandas as pd

from simulate_tectos import simulate_tectos_run

class SimulateTectosRunUnittest(unittest.TestCase):

    def test_creation(self):
        str = simulate_tectos_run.SimulateTectosRun()

    def test_run(self):
        df = pd.read_csv("resources/test_set.csv")
        str = simulate_tectos_run.SimulateTectosRun()
        str.run(df)




def main():
    unittest.main()

if __name__ == '__main__':
    main()