#!/bin/bash

N_TRIALS=$1
RUN_ID=$2
MODELS_SET=$3
ID_SET=$4
EXP_NAME=$5

echo $ID_SET
echo $EXP_NAME

# for run_idx in ${ID_SET}
# do

#    echo "python examples/example_litellm_test.py --prompt_id=${run_idx} --n_trials=${N_TRIALS} --n_sessions=1 --prompts_json=lmsys_tools/prompts.json --models_json=lmsys_tools/${MODELS_SET} --exp_name=${EXP_NAME}_run-${RUN_ID} &&"

# done

# a=($(echo "$t" | tr ',' '\n'))

array_id_set=($(echo "$ID_SET" | tr ' ' '\n'))
array_exp_name=($(echo "$EXP_NAME" | tr ' ' '\n'))


n_ids=${#array_id_set[@]}


# for ((idx=0;idx<$n_ids;idx++))
# do
#    echo "python examples/example_litellm_test.py --prompt_id=${array_id_set[$idx]} --n_trials=${N_TRIALS} --n_sessions=1 --prompts_json=lmsys_tools/prompts.json --models_json=lmsys_tools/${MODELS_SET} --exp_name=${array_exp_name[$idx]}_run-${RUN_ID} &&"
# done

for ((idx=0;idx<$n_ids;idx++))
do
    python examples/example_litellm_test.py --prompt_id=${array_id_set[$idx]} --n_trials=${N_TRIALS} --n_sessions=1 --prompts_json=lmsys_tools/prompts.json --models_json=lmsys_tools/${MODELS_SET} --exp_name=${array_exp_name[$idx]}_run-${RUN_ID}
done


# python examples/example_litellm_test.py --prompt_id=33 --n_trials=${N_TRIALS} --n_sessions=1 --prompts_json=lmsys_tools/prompts.json --models_json=lmsys_tools/${MODELS_SET} --exp_name=model_set_STANDARD_run-${RUN_ID} &&

# python examples/example_litellm_test.py --prompt_id=43 --n_trials=${N_TRIALS} --n_sessions=1 --prompts_json=lmsys_tools/prompts.json --models_json=lmsys_tools/${MODELS_SET} --exp_name=model_set_THINKING_run-${RUN_ID} &&

# python examples/example_litellm_test.py --prompt_id=44 --n_trials=${N_TRIALS} --n_sessions=1 --prompts_json=lmsys_tools/prompts.json --models_json=lmsys_tools/${MODELS_SET} --exp_name=model_set_THINKING_run-${RUN_ID} &&

# python examples/example_litellm_test.py --prompt_id=19 --n_trials=${N_TRIALS} --n_sessions=1 --prompts_json=lmsys_tools/prompts.json --models_json=lmsys_tools/${MODELS_SET} --exp_name=model_set_RESTRICTED_run-${RUN_ID} &&

# python examples/example_litellm_test.py --prompt_id=20 --n_trials=${N_TRIALS} --n_sessions=1 --prompts_json=lmsys_tools/prompts.json --models_json=lmsys_tools/${MODELS_SET} --exp_name=model_set_RESTRICTED_run-${RUN_ID}
