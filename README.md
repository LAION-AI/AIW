<h1 align="center">
        🎩🐇 Alice in Wonderland: Simple Tasks Showing Complete Reasoning Breakdown in State-Of-the-Art Large Language Models
    </h1>
 <p align="center">Alice in Wonderland code base for experiments and raw experiments data</p>
<h4 align="center"><a href="https://marianna13.github.io/aiw/" target="_blank">Homepage</a> | <a href="https://arxiv.org/pdf/2406.02061" target="_blank"> Paper</a> | <a href="https://arxiv.org/abs/2406.02061"target="_blank">arXiv:2506.04598</a> | <a href="https://huggingface.co/spaces/marianna13/AIW-responses"target="_blank">Dataset explorer</a></h4>


## Usage

Install requirements:
`pip install requirements.txt`

### Collect experiments data

**Collect using [LiteLLM](https://github.com/BerriAI/litellm):**
Refer to the [LiteLLM Docs](https://docs.litellm.ai/docs/) on how to setup your account and API keys.

Workflow init:

```bash
export SHARED_MINICONDA=/path/to/miniconda_install
export CONDA_ENV=/path/to/conda_env
export AIW_REPO_PATH=/path/to_local_cloned_AIW_repo

source ${SHARED_MINICONDA}/bin/activate ${CONDA_ENV}
export PYTHONPATH=$PYTHONPATH:$AIW_REPO_PATH

# export your API keys
export TOGETHERAI_API_KEY=
export OPENAI_API_KEY=
export ANTHROPIC_API_KEY=
export MISTRAL_API_KEY=
export GEMINI_API_KEY=
export COHERE_API_KEY=

cd $AIW_REPO_PATH

```


### Execution example for a single selected prompt ID:

```bash

# LiteLLM based experiments; 30 trials for STANDARD prompt type, AIW Variation 1 (Prompt ID 55 in prompts.json)
python examples/example_litellm.py --prompt_id=55 --n_trials=30 --n_sessions=1 --prompts_json=lmsys_tools/prompts.json --models_json=lmsys_tools/models_plot_set.json --exp_name=model_set_STANDARD_run-1

# 30 trials for THINKING prompt type, AIW Variation 2 (Prompt ID 58 in prompts.json)
python examples/example_litellm.py --prompt_id=58 --n_trials=30 --n_sessions=1 --prompts_json=lmsys_tools/prompts.json --models_json=lmsys_tools/models_plot_set.json --exp_name=model_set_THINKING_run-1

# 30 trials for RESTRICTED prompt type, AIW Variation 2 (Prompt ID 58 in prompts.json)
python examples/example_litellm.py --prompt_id=53 --n_trials=30 --n_sessions=1 --prompts_json=lmsys_tools/prompts.json --models_json=lmsys_tools/models_plot_set.json --exp_name=model_set_RESTRICTED_run-1

# Same for LMSys based experiments
python examples/example_lmsys.py --prompt_id=53 --n_trials=30 --n_sessions=1 --prompts_json=lmsys_tools/prompts.json --models_json=lmsys_tools/models_plot_set.json --exp_name=model_set_RESTRICTED_run-1


```

Hint: n_sessions is now purely a dummy, and can be set to 1; the only thing that matters is number of trials

**Execution example for a whole range of ID:**

Hint: rename script file names inside the script files, they have to be adapted, as those are using local own naming)


```bash

# Execute experiments over LiteLLM: 30 trials, start with run counter set to 1, perform 2 rounds; for AIW Variations 1-2, prompt types STANDARD, THINKING, RESTRICTED (as defined in prompt ID)
source execute_litellm_data_gathering.sh 30 1 2 models_plot_set.json "55 56 57 58 53 54" "model_set_STANDARD model_set_STANDARD model_set_THINKING model_set_THINKING model_set_RESTRICTED model_set_RESTRICTED"

# Do the same for AIW Variation 3, prompt types STANDARD, THINKING, RESTRICTED (as defined in prompt ID)
source execute_litellm_data_gathering.sh 30 1 2 models_plot_set.json "63 64 65" "model_set_AIW-VAR-3_STANDARD model_set_AIW-VAR-3_THINKING model_set_AIW-VAR-3_RESTRICTED"

# Execute experiments over lmsys: 7 trials, start with run counter set to 1, perform 2 rounds
source execute_lmsys_data_gathering.sh 7 1 2 models_plot_set.json "55 56 57 58 53 54" "model_set_STANDARD model_set_STANDARD model_set_THINKING model_set_THINKING model_set_RESTRICTED model_set_RESTRICTED"

source execute_lmsys_data_gathering.sh 7 1 2 models_plot_set.json "63 64 65" "model_set_EASY_STANDARD model_set_EASY_THINKING model_set_EASY_RESTRICTED"
```

- Usage for the script call:

```bash
source execute_litellm_data_gathering.sh NUM_TRIALS RUN_ID_START NUM_ROUNDS models_plot_set.json "PROMPT_ID_1 PROMPT_ID_2 PROMPT_ID_3" "EXP_NAME_1 EXP_NAME_2 EXP_NAME_3"

source execute_lmsys_data_gathering.sh NUM_TRIALS RUN_ID_START NUM_ROUNDS models_plot_set.json "PROMPT_ID_1 PROMPT_ID_2 PROMPT_ID_3" "EXP_NAME_1 EXP_NAME_2 EXP_NAME_3"
```

where 

- NUM_TRIALS: trials to conduct in each round
- START_RUN_ID: starting from run id (will apply to file name run-ID)
- NUM_ROUNDS: how many rounds to go, each round will have NUM_TRIALS trials and own incremental run id
- "PROMPT_ID_X ..." : list of IDs pointing to corresponding entries defined in prompt.json file
- "EXP_NAME_X ..." : list of experiment names that can be chosed freely for each corresponding prompt ID to be appended to the filename with saved data

- Example for a collecting data for a full plot (Fig. 1) in the paper

```bash

# Reading models from models_plot_set_reference.json and prompt IDs from prompt.json; full experiment set over all main AIW variations 1-4 and prompt types STANDARD, THINKING, RESTRICTED; doing 30 trials starting with run counter 1, for 2 rounds, aiming ot 60 trials in total per each model and prompt ID (that is a given combination of a prompt type and AIW variation)
source execute_litellm_data_gathering.sh 30 1 2 models_plot_set_reference.json "55 56 57 58 53 54 63 64 65 69 70 71" "model_set_reference_AIW-VAR-1_STANDARD model_set_reference_AIW-VAR-2_STANDARD model_set_reference_AIW-VAR-1_THINKING model_set_reference_AIW-VAR-2_THINKING model_set_reference_AIW-VAR-1_RESTRICTED model_set_reference_AIW-VAR-2_RESTRICTED model_set_reference_AIW-VAR-3_STANDARD model_set_reference_AIW-VAR-3_THINKING model_set_reference_AIW-VAR-3_RESTRICTED model_set_reference_AIW-VAR-4_STANDARD model_set_reference_AIW-VAR-4_THINKING model_set_reference_AIW-VAR-4_RESTRICTED"

```


Refer to [this bash script](scripts/execute_litellm_data_gathering.sh) to see how to use litellm to gather model responses.

**Collect using [TogetherAI](https://www.together.ai/):**

Refer to the [TogetherAI Docs](https://docs.together.ai/docs/quickstart) on how to setup your account and API keys.

Refer to [this Python script](data_collection/examples/example_together.py) to see how to use togetherAI to gather model responses.

**Collect by scraping [LMSYS Chatbot Arena](https://chat.lmsys.org/):**

*Note* This method is not recommended since it's limited for purpose of automated model evaluation. The platform is gated by cloudflare.

Refer to [this bash script](scripts/execute_lmsys_data_gathering.sh) to see how to use litellm to gather model responses.


## Plot the data

Run script to generate plots from the paper (by default plots will be saved in the working directory):
`bash scripts/plot.sh`

## Acknowledgments

We would like to express gratitude to all the people who are working on making code, models and data publicly available, advancing community based research and making research more reproducible. Specifically, we would like to thank all the members of the [LAION Discord server](https://discord.gg/BZqhreFazY) community and [Open-Ψ (Open-Sci) Collective](https://discord.gg/GsKh4mBVcv) for providing fruitful ground for scientific exchange and open-source development.

Marianna Nezhurina acknowledges funding by the Federal Ministry of Education and Research of Germany under grant no. 01IS22094B WestAI - AI Service Center West.

Lucia Cipolina-Kun acknowledges the Helmholtz Information & Data Science Academy (HIDA) for providing financial support enabling a short-term research stay at Juelich Supercomputing Center (JSC), Research Center Juelich (FZJ) to conduct research on foundation models.

## Citation
If you like this work, please cite:

```
@article{nezhurina2024alice,
        title={Alice in Wonderland: Simple Tasks Showing Complete Reasoning Breakdown in State-Of-the-Art Large Language Models},
        author={Marianna Nezhurina and Lucia Cipolina-Kun and Mehdi Cherti and Jenia Jitsev},
        year={2024},
        journal={arXiv preprint arXiv:2406.02061},
        eprint={2406.02061},
        archivePrefix={arXiv},
        primaryClass={cs.LG}
}
```

License
=======
    Copyright 2024 Marianna Nezhurina, Lucia Cipolina-Kun, Mehdi Cherti, Jenia Jitsev

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
