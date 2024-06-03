# Description: This script is used to plot the boxplot of the correct response rate of the AIW and AIW+ models for the given prompt ids.
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from matplotlib.font_manager import FontProperties



def plot_boxplot(data, ax, prompt_id, X_LOWER=0, X_UPPER=1, palette='#5A9'):

    sns.set_theme(style="whitegrid")

    meds = data.groupby('model')['correct'].mean()
    meds.sort_values(ascending=False, inplace=True)
    # meds = meds[meds > 0]
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
        color=palette,
        # hue='model',
        # hue_order=meds.index,
        order=meds.index,
        linewidth=0.3
        )
    
    ax.xaxis.set_label_position('top') 
    ax.xaxis.tick_top()
    ax.tick_params(width=0.2)

    family = 'sans-serif'

    font = FontProperties()
    font.set_family(family)

    plt.ylabel('')

    plt.xticks(fontsize=6)
    plt.yticks(fontsize=8)
    plt.locator_params(nbins=10)
    plt.xlim(X_LOWER, X_UPPER)
    plt.grid( linestyle='--', alpha=0.3, linewidth=0.1, color='grey')

PROMPT_TYPES = {
    "STANDARD": "55 56 63 69 91".split(),
    "THINKING": "57 58 64 70 92".split(),
    "RESTRICTED": "53 54 65 71 93".split(),
}

# nice colors
LEGEND_COLORS = {
    "STANDARD": "#8856a7",
    "THINKING": "#9ebcda",
    "RESTRICTED": "#e0ecf4",
    "THINKING/STANDARD": "#8856a7",
    "STANDARD/THINKING": "#8856a7",
}

if __name__ == '__main__':
    prompts_id_2 = '69'.split('_')
    prompts_id = '63'.split(',')

    if prompts_id_2[0] == '62':
        prompts_id_2 = ['56']
    if prompts_id[0] == '60':
        prompts_id = ['54']
    prompt_type = []
    for p in prompts_id:
        prompt_type.extend([k for k, v in PROMPT_TYPES.items() if p in v])
    prompt_type = list(set(prompt_type))
    if len(prompt_type) > 0:
        prompt_type = '/'.join(prompt_type)
    else:
        prompt_type = prompt_type[0]
    prompt_type_2 = []
    for p in prompts_id_2:
        prompt_type_2.extend([k for k, v in PROMPT_TYPES.items() if p in v])

    prompt_type_2 = list(set(prompt_type_2))
    if len(prompt_type_2) > 0:
        prompt_type_2 = '/'.join(prompt_type_2)
    else:
        prompt_type_2 = prompt_type_2[0]
    color = LEGEND_COLORS[prompt_type]
    color_2 = LEGEND_COLORS[prompt_type_2]

    if prompt_type == prompt_type_2:
        color_2 = '#5A9'


    if len(prompts_id) == 1:
        aiw_plus_plot_df_path = r'AITW' +r'\\'+f'{prompts_id[0]}_data.pkl'
    else:
        aiw_plus_plot_df_path = r'AITW'+r'\\'+f'{"_".join(prompts_id)}_data.pkl'

    if len(prompts_id_2) == 1:
        aiw_plot_df_path = r'AITW' +r'\\'+f'{prompts_id_2[0]}_data.pkl'
    else:
        aiw_plot_df_path = r'AITW'+r'\\'+f'{"_".join(prompts_id_2)}_data.pkl'


    fig, ax1 = plt.subplots(figsize=(10, 8))
    data_aiw = pd.read_pickle(aiw_plot_df_path)
    data_aiw_plus = pd.read_pickle(aiw_plus_plot_df_path)



    aiw_box_plot = plot_boxplot(data_aiw, ax1, prompts_id,  X_LOWER=-.01, X_UPPER=1.01, palette=color)
    # ax1.set_title('AIW Correct response rate', fontweight='bold', fontdict={ 'size': 6})
    # ax2 = fig.add_axes([0.4, 0.15, 0.45, 0.5])

    aiw_plus_box_plot =  plot_boxplot(data_aiw_plus, ax1, prompts_id_2, X_LOWER=-.01, X_UPPER=1.01, palette=color_2)


    custom_lines = [plt.Line2D([0], [0], color=color, lw=4),
                    plt.Line2D([0], [0], color=color_2, lw=4)]

    if len(prompts_id) == 1:

        legend_text = f'{prompts_id_2[0]}, {prompt_type_2}', f'{prompts_id[0]}, {prompt_type}'
    elif len(prompts_id_2) == 1:
        legend_text = f'{prompts_id_2[0]}, {prompt_type_2}', f'{prompts_id[0]}, {prompt_type}'
    else:
        legend_text = f'{prompt_type_2}', f'{prompt_type}'
    plt.legend(custom_lines, legend_text, loc='center right', fontsize=10)

    if len(prompts_id) == 1:
        label = f'Correct response rate {prompts_id[0]} vs {prompts_id_2[0]}'
    elif len(prompts_id_2) == 1:
        label = f'Correct response rate {prompts_id[0]} vs {prompts_id_2[0]}'
    else:    
        label = f'Correct response rate {prompt_type} vs {prompt_type_2}'
    plt.xlabel(label, fontweight='bold', fontdict={ 'size': 12})


    if len(prompts_id) == 1:
        figname = f'{prompts_id[0]}_vs_{prompts_id_2[0]}.pdf'
    elif len(prompts_id_2) == 1:
        figname = f'{prompts_id[0]}_vs_{prompts_id_2[0]}.pdf'
    else:
        figname = f'{"_".join(prompts_id)}_vs_{"_".join(prompts_id_2)}.pdf'
    print(figname)
    fig.savefig(figname, bbox_inches='tight', transparent=False)