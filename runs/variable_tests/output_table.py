import pandas as pd
import numpy as np
import subprocess

df = pd.DataFrame({'d': [1., 1., 1., 2., 2., 2.],
                   'c': np.tile(['a', 'b', 'c'], 2),
                   'v': np.arange(1., 7.)})
filename = 'out.tex'
pdffile = 'out.pdf'
outname = 'out.png'

template = r'''\documentclass[preview]{{standalone}}
\usepackage{{booktabs}}
\begin{{document}}
{}
\end{{document}}
'''

with open(filename, 'wb') as f:
    f.write(template.format(df.to_latex()))

#subprocess.call(['pdflatex', filename], shell=True)
subprocess.call(['convert', '-density', '300', pdffile, '-quality', '90', outname], shell=True)
