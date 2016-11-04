import argparse
import pandas as pd

import simulate_tectos_run

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-csv', help='dataframe in csv format')
    parser.add_argument('-s', type=int, help='steps in each simulation')
    parser.add_argument('-new_ggaa_model', action="store_true",
                        help='use different model for ggaa_contact')
    parser.add_argument('-ggaa_model', help='path to motif file for new model ')
    parser.add_argument('-n', type=int, help='number of runs per construct')
    parser.add_argument('-v', action="store_true",
                        help='verbose print out')
    args = parser.parse_args()

    f_extension = args.csv[-4:]
    if f_extension != ".csv":
        raise ValueError("file supplied with -csv does not have a .csv extension")

    return args

args = parse_args()

try:
    df = pd.read_csv(args.csv)
except:
    raise ValueError(
        "cannot load csv file: " + args.csv + " either it doesnt exist or " +
        "it is not a pandas dataframe formmated in csv format")

run_dict = {}
opts = vars(args)
del opts['csv']

for name,val in opts.iteritems():
    if val is None:
        continue
    run_dict[name] = val

st_run = simulate_tectos_run.SimulateTectosRun()
st_run.run(df, **run_dict)
