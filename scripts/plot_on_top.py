import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from matplotlib.font_manager import FontProperties


sns.set_theme(style="whitegrid")


def plot_boxplot(data, ax, X_LOWER=0, X_UPPER=1, palette='#5A9', label='AIW', rm_zeros=True):

    

    meds = data.groupby('model')['correct'].mean()
    meds.sort_values(ascending=False, inplace=True)
    if rm_zeros:
        meds = meds[meds > 0]
    sns.boxplot(
        x='correct', 
        y='model', 
        data=data, 
        ax=ax,
        showmeans=False,
        shownotches=False,
        showbox=True,
        showcaps=True,
        showfliers=False,
        meanprops={"marker":"o",
                   "markerfacecolor":"white", 
                   "markeredgecolor":"black",
                   "markersize":"10"},
        # color=palette,
        palette=palette,
        hue='model',
        hue_order=meds.index,
        order=meds.index,
        linewidth=0.3
        )
    
    ax.xaxis.set_label_position('top') 
    ax.xaxis.tick_top()
    ax.tick_params(width=0.2)

    family = 'sans-serif'

    font = FontProperties()
    font.set_family(family)

    plt.xlabel(label, fontweight='bold', fontdict={ 'size': 12})
    plt.ylabel('')

    plt.xticks(fontsize=6)
    plt.yticks(fontsize=8)
    plt.locator_params(nbins=20)
    plt.xlim(X_LOWER, X_UPPER)
    plt.grid( linestyle='--', alpha=0.3, linewidth=0.1, color='grey')



if __name__ == '__main__':

    aiw_plot_df_path = r'AITW\55_56_63_69_57_58_64_70_53_54_65_71_data.pkl'

    aiw_plus_plot_df_path = r'AITW\91_92_data.pkl'


    fig, ax1 = plt.subplots(figsize=(10, 6))
    data_aiw = pd.read_pickle(aiw_plot_df_path)
    data_aiw_plus = pd.read_pickle(aiw_plus_plot_df_path)



    aiw_box_plot = plot_boxplot(data_aiw, ax1,  X_LOWER=-.01, X_UPPER=1.01, palette='light:seagreen', label='AIW Correct response rate')

    ax2 = fig.add_axes([0.4, 0.15, 0.45, 0.5])

    aiw_plus_box_plot =  plot_boxplot(data_aiw_plus, ax2, X_LOWER=-.01, X_UPPER=1.01, palette='light:blue', label='AIW+ Correct response rate')

    figname = 'aiw_vs_aiw_plus.pdf'
    print(figname)
    fig.savefig(figname, bbox_inches='tight', transparent=False)