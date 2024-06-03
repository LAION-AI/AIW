#!/bin/bash

N_TRIALS=$1
RUN_ID=$2

python examples/example_litellm_test.py --prompt_id=55 --n_trials=${N_TRIALS} --n_sessions=1 --prompts_json=lmsys_tools/prompts.json --models_json=lmsys_tools/models_plot_set.json --exp_name=model_set_STANDARD_run-${RUN_ID}

python examples/example_litellm_test.py --prompt_id=56 --n_trials=${N_TRIALS} --n_sessions=1 --prompts_json=lmsys_tools/prompts.json --models_json=lmsys_tools/models_plot_set.json --exp_name=model_set_STANDARD_run-${RUN_ID}

python examples/example_litellm_test.py --prompt_id=57 --n_trials=${N_TRIALS} --n_sessions=1 --prompts_json=lmsys_tools/prompts.json --models_json=lmsys_tools/models_plot_set.json --exp_name=model_set_THINKING_run-${RUN_ID}

python examples/example_litellm_test.py --prompt_id=58 --n_trials=${N_TRIALS} --n_sessions=1 --prompts_json=lmsys_tools/prompts.json --models_json=lmsys_tools/models_plot_set.json --exp_name=model_set_THINKING_run-${RUN_ID}

python examples/example_litellm_test.py --prompt_id=53 --n_trials=${N_TRIALS} --n_sessions=1 --prompts_json=lmsys_tools/prompts.json --models_json=lmsys_tools/models_plot_set.json --exp_name=model_set_RESTRICTED_run-${RUN_ID}

python examples/example_litellm_test.py --prompt_id=54 --n_trials=${N_TRIALS} --n_sessions=1 --prompts_json=lmsys_tools/prompts.json --models_json=lmsys_tools/models_plot_set.json --exp_name=model_set_RESTRICTED_run-${RUN_ID}
