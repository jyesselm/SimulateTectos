SimulateTectos package:
=======================

---

tools for working with RNAMake's simulate_tectos tool for simulating the tecto RNA system.


simulate_set.py
---------------
accepts a whole set of constructs to run where each line in a csv file is a construct.

```
simulate_set.py -csv CSV 
				[-s S] 
				[-out_file OUT_FILE]
				[-new_ggaa_model]
				[-ggaa_model GGAA_MODEL]
				[-extra_me EXTRA_ME]
				[-extra_motifs EXTRA_MOTIFS]
				[-print_command]
				[-n N]
				[-v]
				[-max MAX]
				[-simulation.temperature SIMULATION.TEMPERATURE]
				[-simulation.steric_radius SIMULATION.STERIC_RADIUS]
				[-simulation.cutoff SIMULATION.CUTOFF]
```

### examples:
```
simulate_set.py -csv examples/0/test_set.csv -out_file examples/0/results.csv
```

where:
test_set.csv

![test_set.csv](resources/imgs/test_set.png)

possible columns for csv file:

Column  | Description
------------- | -------------
fseq		    | sequence of flow peice 
fss			    | secondary structure of the flow peice in dot bracket notation
cseq			 |	sequence of the chip peice 
css			    | secondary structure of the flow peice in dot bracket notation
s				 | number of steps in the monte carlo
n				 | number of independent monte carlo runs, will return the averaged hit_count of all the runs (default: 1,000,000)
extra_me		 | extra motif ensemble file, allows for user supplied motif ensemble for a given a motif sequence/secondary structure
simulation.temperature | the temperature for the monte carlo simulation (default: 298K)
simulation.steric_radius | the radius between each steric bead that defines a steric clash (default: 2.2)
simulation.cutoff | the cutoff between the target and current basepair that defines a hit (default: 4.5)

For each row in the csv file a value MUST be defined, pd.nan is not a viable option.

Values can be overrided at command line, if number of steps is specified at command line and is in the csv, the command line will override the csv value. command line options are options that you want to be included for all rows.


generate_pdbs_of_clusters.py
---------------





