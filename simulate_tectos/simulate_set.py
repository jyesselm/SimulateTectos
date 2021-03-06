import argparse
import pandas as pd

import simulate_tectos_run

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-csv', help='dataframe in csv format', required=True)
    parser.add_argument('-s', type=int, help='steps in each simulation')
    parser.add_argument('-out_file', help='the name of the output csv')
    parser.add_argument('-new_ggaa_model', action="store_true",
                        help='use different model for ggaa_contact')
    parser.add_argument('-ggaa_model', help='path to motif file for new model ')
    parser.add_argument('-extra_me', help='extra me file for swaping ensembles')
    parser.add_argument('-extra_motifs', help='extra motif files')
    parser.add_argument('-print_command', action="store_true", help="see commands that are being excuted")

    parser.add_argument("-scorer", help="select the scoring typpe")
    parser.add_argument("-constraints", help="select contraints for SixD scorer")
    parser.add_argument('-temperature', type=float, help='temperature of simulation')
    parser.add_argument('-cutoff', type=float, help='cutoff of simulation')
    parser.add_argument('-coorigin', action="store_true", help='changes orientation of buildup')
    parser.add_argument('-randomized_start', action='store_true',
                        help='randomizes the start state at beginning of simulation')

    parser.add_argument('-n', type=int, help='number of runs per construct')
    parser.add_argument('-v', action="store_true",
                        help='verbose print out')
    parser.add_argument('-max', type=int, help='for  testing max number of rows')


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

st_run = simulate_tectos_run.SimulateTectosRun()

if opts['print_command']:
    st_run._stw._options['print_command'] = True

del opts['print_command']

for name,val in opts.iteritems():
    if val is None:
        continue
    run_dict[name] = val


st_run.run(df, **run_dict)
