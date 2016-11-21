import numpy as np
from scipy import stats

def r2(x, y):
    return stats.pearsonr(x, y)[0] ** 2

def get_avg_diff(x, y):
    diff = abs(x - y)
    sum = np.sum(diff)
    return sum / len(diff)