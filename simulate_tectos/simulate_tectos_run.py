import pandas as pd
from rnamake import base, option, vienna
from rnamake.wrappers import simulate_tectos_wrapper, options



class SimulateTectosRun(object):
    def __init__(self):
        self._stw = simulate_tectos_wrapper.SimulateTectosWrapper()
        self._cmd_options = options.Options()
        self._cmd_option_defaults = {}

        self._options = options.Options()
        self._options.add("n", 1)
        self._options.add('out_file', "results.csv")
        self._options.add('v', 0)

        self._output_columns = []

        for opt_name in self._stw._cmd_options.valid_options():
            self._cmd_options.add(opt_name, self._stw.get_cmd_option(opt_name))
            self._cmd_option_defaults[opt_name] = self._stw.get_cmd_option(opt_name)

    def _setup_output_df(self, df):
        self._output_columns = []

        for name, value in self._cmd_options.get_dict().iteritems():
            if self._cmd_option_defaults[name] == value:
                continue
            self._output_columns.append(name)

        for name in df.columns.values:
            if name in self._output_columns:
                raise ValueError(
                    "input conflict: " + name + " is specified in both options and dataframe!")
            else:
                self._output_columns.append(name)

        self._output_columns.append("avg_hit_count")

        output_df = pd.DataFrame(columns=self._output_columns)
        return output_df

    def _get_run_options(self, df_row):
        run_dict = {}
        for name, value in df_row.to_dict().iteritems():
            if name in self._cmd_options:
                run_dict[name] = value

        for name, value in self._cmd_options.get_dict().iteritems():
            if self._cmd_option_defaults[name] == value:
                continue
            run_dict[name] = value

        return run_dict

    def run(self, df, **options):
        for name, value in options.iteritems():
            if name in self._options:
                self._options[name] = value
            elif name in self._cmd_options:
                self._cmd_options[name] = value
            else:
                raise ValueError("unknown option: " + name)

        output_df = self._setup_output_df(df)
        pos = 0
        n = self._options['n']

        for i,row in df.iterrows():
            run_options = self._get_run_options(row)
            avg_hit_count = 0
            runs = 0

            for i in range(0, n):
                self._stw.run(**run_options)
                hits = self._stw.get_output()
                if hits is not None:
                    runs += 1
                    avg_hit_count += hits
            avg_hit_count /= runs

            new_row = []
            for col in self._output_columns[:-1]:
                try:
                    new_row.append(run_options[col])
                except:
                    new_row.append(row[col])
            new_row.append(avg_hit_count)
            if self._options['v']:
                print new_row
            output_df.loc[pos] = new_row
            pos += 1

        output_df.to_csv(self._options['out_file'], index=False)





