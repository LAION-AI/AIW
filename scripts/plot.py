import pandas as pd
import numpy as np
from scipy import stats
import glob
import json
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import argparse
from scipy.optimize import minimize
from scipy import optimize
from adjustText import adjust_text
import re



plt.style.use("ggplot")



MODEL_SHORT_NAMES = {
    'mistral-large-latest': 'Mistral-L',
    'gpt-4-turbo-2024-04-09': 'GPT-4-T',
    'claude-3-opus-20240229': 'Claude-3-O',
    'llama-3-70b-chat': 'LLama-3-70b',
    'claude-3-sonnet-20240229': 'Claude-3-S',
    'open-mixtral-8x22b': 'Mixtral-8x22b',
    'qwen1.5-72b-chat': 'Qwen1.5-72b',
    'command-r-plus': 'Command-R+',
    'claude-3-haiku-20240307': 'Claude-3-H',
    'qwen1.5-32b-chat': 'Qwen1.5-32b',
    'mistral-small-latest': 'Mistral-S',
    'open-mixtral-8x7b': 'Mixtral-8x7b',
    'gpt-3.5-turbo-0125': 'GPT-3.5-T',
    'qwen1.5-14b-chat': 'Qwen1.5-14b',
    'gemini-pro': 'Gemini-Pro',
    'open-mistral-7b': 'Mistral-7b',
    'qwen1.5-7b-chat': 'Qwen1.5-7b', 
    'gemma-7b-it': 'Gemma-7b',
    'llama-3-8b-chat': 'Llama-3-8b',
    'qwen1.5-4b-chat': 'Qwen1.5-4b',
    'gpt-4-0613': 'GPT-4',
    'qwen1.5-1.8b-chat': 'Qwen1.5-1.8b',
    'gemma-2b-it': 'Gemma-2b',
    'gpt-4-turbo-preview': 'GPT-4-T-Preview',
    'gpt-4o-2024-05-13': 'GPT-4-O',
    'mistral-large-2402': 'Mistral-L',
    'llama-2-7b-chat': 'LLama-2-7b',
    'llama-2-70b-chat': 'LLama-2-70b',
    'llama-2-13b-chat': 'LLama-2-13b',
    'dbrx-instruct': 'DBRX-Instruct',
}

PROMPT_TYPES = {
    "STANDARD": "55 56 63 69 91".split(),
    "THINKING": "57 58 64 70 92".split(),
    "RESTRICTED": "53 54 65 71 93".split()
}

PARAMS_PROMPTS = {
    '100,101,102': re.compile(r'M(?:\s*\+|\s+\s*)1'),
    '103,104,105': re.compile(r'X(?:\s*\+|\s+\s*)1'),
    '106,107,108': re.compile(r'Y(?:\s*\+|\s+\s*)1')
}

PARAMS_PROMPTS_2 = {}

for k,v in PARAMS_PROMPTS.items():

    for p in k.split(','):
        PARAMS_PROMPTS_2[p] = v




PROMPT_TYPES = {
    k: list(map(int, v)) for k,v in PROMPT_TYPES.items()
}

MODEL_MAPPINGS = {
    "mistral-large": "mistral-large-2402",
    "mistral-large-latest": "mistral-large-2402",
    "gpt-4-turbo-preview": "gpt-4-0125-preview",
    "mistral-small-latest": "mistral-small",
    "mistral-large-2402": "mistral-large-2402"
}

def find_alpha_beta_for_mean_variance(mu, var):
    """
    Find alpha and beta parameters for Beta distribution given mean and variance.
    Args:
        mu (float): Mean of the distribution.
        var (float): Variance of the distribution.
    """
    def objective_function(alpha):
        beta = alpha * (1 / mu - 1)
        mean_diff = alpha / (alpha + beta) - mu
        var_diff = (alpha * beta) / ((alpha + beta) ** 2 * (alpha + beta + 1)) - var

        return mean_diff ** 2 + var_diff ** 2

    initial_guess = mu * (1 - mu) / var - 1
    result = minimize(objective_function, initial_guess, method='Nelder-Mead')
    alpha = result.x
    beta = alpha * (1 / mu - 1)

    return alpha[0], beta[0]

def plot_boxplot(data, output_path, prompt_id):
    """
    Plot the results of the models.
    Args:
        data (pd.DataFrame): Dataframe with the results.
        output_path (str): Path to save the plot.
    """
    sns.set_style("whitegrid")
    FIG_WIDTH, FIG_HEIGHT = (6, 4)

    X_LOWER, X_UPPER = 0, 1

    fig, ax = plt.subplots(figsize=(FIG_WIDTH, FIG_HEIGHT))
    # ax = plt.subplot(111)

    meds = data.groupby('model')['correct'].mean()
    meds.sort_values(ascending=False, inplace=True)
    data = data.set_index('model').join(meds, rsuffix='_mean')

    data = data.reset_index()
    data = data.rename(columns={'correct_mean': 'mean'})
    # data = data[data['mean'] > 0]
    data = data.sort_values(by='mean', ascending=False)

    ax = sns.boxplot(
        data=data,
        x='correct',
        y='model',
        # orient='h',
        showmeans=False,
        shownotches=False,
        showbox=True,
        showcaps=True,
        showfliers=False,
        meanprops={"marker":"o",
                   "markerfacecolor":"white", 
                   "markeredgecolor":"black",
                   "markersize":"10"},
        palette='light:#5A9',
        hue='model',
        hue_order=meds.index,
        order=meds.index,
        linewidth=0.3 # make opacity of the boxplot lower if it's zero
    )


    prompt_ids_str = ', '.join([f'#{p}' for p in prompt_id])

    ax.xaxis.set_label_position('top') 
    ax.xaxis.tick_top()

    family = 'sans-serif'

    font = FontProperties()
    font.set_family(family)

    xlabel = '+' if 91 in prompt_id or  92 in prompt_id  or 93 in prompt_id else ''

    plt.xlabel(f'AIW{xlabel} Correct response rate', fontweight='bold', fontdict={ 'size': 6})

    plt.ylabel('')
    plt.xticks(fontsize=4)
    plt.yticks(fontsize=4)
    plt.locator_params(nbins=20)
    plt.xlim(X_LOWER, X_UPPER)
    plt.grid( linestyle='--', alpha=0.5, linewidth=0.1, color='grey')

    plt.tight_layout()
    prompt_ids_str = '_'.join([f'{p}' for p in prompt_id])

    ax.tick_params(width=0.2)
    ax.figure.savefig(output_path.format(prompt_ids_str), dpi=300, transparent=True)





def plot_heatmap_prompttypes(data, output_path, prompt_id):
    """
    Plot the heatmap of the prompt types.
    Args:
        data (pd.DataFrame): Dataframe with the results.
        output_path (str): Path to save the plot.
        prompt_id (list): List of prompt ids.
    """
    fig = plt.figure(figsize=(10, 20))

    data = data.dropna(subset=['model_response'])
    
    data['len_model_response'] = data.model_response.apply(lambda x: len(list(x)) if isinstance(x, str) else 0)
    data["prompt_type"] = data.prompt_id.apply(lambda x: 'STANDARD' if x in PROMPT_TYPES['STANDARD'] else 'THINKING' if x in PROMPT_TYPES['THINKING'] else 'RESTRICTED')
    data_pivot = data.groupby(['model', 'prompt_type'])[['correct']].count().reset_index()
    data_pivot = data_pivot.pivot(index='model', columns='prompt_type', values='correct')
    xlabel = '+' if 91 in prompt_id or  92 in prompt_id  or 93 in prompt_id else ''


    data_pivot = data_pivot.sort_values(by='STANDARD', ascending=False)
    ax = sns.heatmap(
        data_pivot,
        annot=True,
        cmap='viridis',
        linewidths=0.5,
        linecolor='black'
    )
    plt.title(f'AIW{xlabel} Number of responses per model', fontweight='bold')


    ax.xaxis.set_label_position('top') 
    ax.xaxis.tick_top()
    # plt.tight_layout()
    prompt_ids_str = '_'.join([f'{p}' for p in prompt_id]) + '_heatmap'
    plt.savefig(output_path.format(prompt_ids_str), dpi=300, transparent=True, bbox_inches='tight')
    fig = plt.figure(figsize=(10, 20))

    data_pivot = data.groupby(['model', 'prompt_type'])[['len_model_response']].mean().reset_index()
    data_pivot = data_pivot.pivot(index='model', columns='prompt_type', values='len_model_response')
    data_pivot = data_pivot.sort_values(by='STANDARD', ascending=False)
    ax = sns.heatmap(
        data_pivot,
        annot=True,
        cmap='viridis',
        linewidths=0.5,
        linecolor='black'
    )

    plt.title(f'AIW{xlabel} Average length of responses', fontweight='bold')
    plt.xticks()
    plt.yticks()

    ax.xaxis.set_label_position('top') 
    ax.xaxis.tick_top()
    # plt.tight_layout()
    prompt_ids_str = '_'.join([f'{p}' for p in prompt_id]) + '_heatmap_len_model_response'
    plt.savefig(output_path.format(prompt_ids_str), dpi=300, transparent=True, bbox_inches='tight')



def get_model_data(df, model_name):
    df = df[df.model == model_name]

    data = df.correct.apply(int).values
   
    n = len(data)
    p = data.sum()/n
    # n = 1
    mean = n*p
    alpha = 0.05
    z = 1 -0.5*alpha
    std = np.sqrt(p*(1-p)/n)

    def f(x, mu, var):
        alpha, beta = x[0], x[1]
        return [alpha/(alpha+beta) - mu, (alpha*beta)/(((alpha+beta)**2)*(alpha+beta+1)) - var]
    rv = optimize.root(f, [1, 1], args=(p, p*(1-p)/n)).x
    alpha, beta = rv[0], rv[1]

    if alpha > 0 and beta > 0:
    # Calculate PDF values
        data = stats.beta.rvs(alpha, beta, size=1000)
    else:
        data = np.random.normal(loc=p, scale=std, size=1000)

    return data

def plot_barplot(df, benchmark, descriptions, output_path, prompt_id):
    """
    Plot the barplot of the results.
    Args:
        df (pd.DataFrame): Dataframe with the results.
        benchmark (str): Benchmark column.
        descriptions (str): Description of the plot.
        output_path (str): Path to save the plot.
        prompt_id (list): List of prompt ids.
    """

    sns.set_style("whitegrid")

    print(df[['model', 'MMLU']])

    df = df[~df[benchmark].isna()]
   
    fig = plt.figure(figsize=(10,8))
    ax = plt.subplot(111)
    df['diff'] = df[benchmark] - df.correct 



    df = df.sort_values(by='diff', ascending=False)
    
    models = df.model.unique()

    df['model_dummy'] = df['model'].map(dict(zip(models, range(len(models)))))

    texts = []


    for i in range(len(df)):
        model_name = df.model.iloc[i]
        correct = df.correct.iloc[i]
        text = MODEL_SHORT_NAMES[model_name]
        if correct == 0:
            text = ''
        texts.append(plt.text(df.correct.iloc[i]+0.02, df[benchmark].iloc[i], text, fontsize=8, color='black'))

    ax = sns.scatterplot(
        data=df,
        x='correct', 
        y=benchmark, 
        palette="Set3", 
        s=300,
        hue='model',
        style='model',
        ax=ax,
        )
    
    
    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height * 0.3,
                    box.width, box.height * 0.7])
    adjust_text(texts, arrowprops=dict(arrowstyle="->", color='black', lw=0.5, alpha=0.5))


    handles, labels = ax.get_legend_handles_labels()
    legend = ax.legend(
        handles, 
        models, 
        loc='lower right',
        fontsize=8, 
        ncol=3, 
        )
    x = np.linspace(0,1, 100)
    plt.plot(
        x,
        x,
        linestyle='--',
        alpha=.5,
        label='y=x',
        color='black'
        )

    xlabel = '+' if 91 in prompt_id or  92 in prompt_id  or 93 in prompt_id else ''
    plt.xlabel(f'AIW{xlabel} Correct response rate', fontweight='bold', fontdict={ 'size': 10})
    plt.ylabel(benchmark, fontweight='bold', fontdict={ 'size': 10})
    plt.xlim(-0.05, 1)
    plt.ylim(0, 1)
    plt.title(f'AIW Correct answers vs {benchmark}', fontsize=10, fontweight='bold')

    plt.grid(alpha=0.5, linestyle='--', linewidth=0.5, color='grey')
    
    ext = output_path.split('.')[-1]
    prompt_ids_str = '_'.join([f'{p}' for p in prompt_id])
    plt.savefig(output_path.replace(f'.{ext}', '').format(prompt_ids_str)+f'_{benchmark}.{ext}'.replace(':', '_'), dpi=400, transparent=True, bbox_inches='tight')



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Plot the results of the models')
    parser.add_argument('--output', type=str, default='boxplot.png', help='Path to the output plot')
    parser.add_argument('--jsons_dir', type=str, default='.', help='Path to the directory with json files')
    parser.add_argument('--prompt_id', type=str, default='1', help='Prompt id')
    parser.add_argument('--prompts_json', type=str, default='prompts.json', help='Path to prompts json file')

    args = parser.parse_args()
    dist = stats.binom


    jsons_dir = args.jsons_dir

    data = []


    prompt_id = args.prompt_id
    prompt_id = prompt_id.split(',')
    prompt_id = [int(p) for p in prompt_id]
    prompts_json = args.prompts_json
    with open(prompts_json, 'r') as f:
        prompts_data = json.load(f)
    prompt_data = [p for p in prompts_data if p['id'] in prompt_id]

    prompts = [p['prompt'] for p in prompt_data]

    for j in glob.glob(f'{jsons_dir}/**/*.json', recursive=True):
        with open(j, 'r') as f:
 
            js = json.load(f)
            if isinstance(js, list):
                data.extend(js)
            else:
                data.append(js)
  



    df = pd.DataFrame(data)

    df.model = df.model.apply(lambda x: x.lower().split('/')[-1])
    df['correct_reasoning'] = True
    df['manual_inspection'] = False
    all_prompts = df.prompt.unique()
    prompts_dict = {}
    for prompt in all_prompts:
        for p_data in prompts_data:
            if p_data['prompt'] == prompt:
                prompts_dict[prompt] = int(p_data['id'])
            else:
                if prompt not in prompts_dict:

                    prompts_dict[prompt] = None
                


    df['prompt_id'] = df.prompt.apply(lambda x: prompts_dict[x])
    df.model = df.model.apply(lambda x: x.replace('-hf', ''))

    df.model = df.model.apply(lambda x: MODEL_MAPPINGS[x] if x in MODEL_MAPPINGS else x)

    

    def get_correct_regex(prompt_id, correct, model_response):
        prompt_id = int(prompt_id)
        if str(prompt_id) in PARAMS_PROMPTS_2:
            return PARAMS_PROMPTS_2[str(prompt_id)].search(model_response) is not None
        return correct
    


    df = df[df.prompt.isin(prompts)]
    

    models = df.model.unique()
    data = []
    for model in models:
        model_data = get_model_data(df, model)
        if model_data is None:
            continue
        
        data.extend([{
            'model': model,
            'correct': sample
        } for sample in model_data])

    data = pd.DataFrame(data)

    plot_boxplot(data, args.output, prompt_id)

    df = df.groupby(['model'])[['correct']].mean().reset_index()

    df_names = pd.read_excel('models_data/models_plot_set_FULL_names.xlsx')

    df_lb = pd.read_excel('models_data/all_models_plot_set_FULL_results.xlsx')
    df_lb.model = df_lb.model.apply(lambda x: x.replace('-hf', ''))
    df_names.model = df_names.model.apply(lambda x: x.replace('-hf', ''))
    df_names.hf_model_name  = df_names.hf_model_name.apply(lambda x: x.replace('-hf', ''))
    columns = ['hf_model_name'] + df_lb.columns[1:].tolist()
    df_lb.columns = columns

    df_lb.hf_model_name = df_lb.hf_model_name.str.lower()
    df_names.hf_model_name = df_names.hf_model_name.str.lower()
    df_lb = df_lb.merge(df_names, left_on='hf_model_name', right_on='hf_model_name', how='right')
    df_lb.model = df_lb.model.apply(lambda x: x.lower().split('/')[-1].split('\/')[-1])
    
    benchmark = 'MMLU'

    df.model = df.model.apply(lambda x: x.lower()).astype(str)
    df = df.set_index('model').join(df_lb.set_index('model'))

    
    df = df[['correct', benchmark]].reset_index()
 
 
    plot_barplot(df, benchmark, '', args.output, prompt_id)


