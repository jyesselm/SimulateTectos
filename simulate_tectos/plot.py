import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("white")
sns.set_context("talk")

def plot_dG_correlation(df):
    plt.figure()
    sns.regplot(x="dG_normalized", y="dG_predicted", data=df,
                scatter_kws={"s": 100})

def show_plots():
    plt.show()