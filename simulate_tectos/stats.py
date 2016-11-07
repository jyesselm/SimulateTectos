from scipy import stats

def r2(x, y):
    return stats.pearsonr(x, y)[0] ** 2