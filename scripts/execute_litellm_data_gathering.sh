#!/bin/bash

N_TRIALS=$1
START_RUN_ID=$2
SESSIONS=$3


MODELS_SET=$4
ID_SET=$5
EXP_NAME=$6

echo $ID_SET
echo $EXP_NAME

array_id_set=($(echo "$ID_SET" | tr ' ' '\n'))
array_exp_name=($(echo "$EXP_NAME" | tr ' ' '\n'))


n_ids=${#array_id_set[@]}

# adapt data_collection/examples/example_litellm.py to your env and save it as data_collection/examples/example_litellm_test.py  
for ((sess_id=0; sess_id<$SESSIONS;sess_id++))
do

    RUN_ID=$((START_RUN_ID + sess_id))
    echo $RUN_ID

    for ((idx=0;idx<$n_ids;idx++))
    do
        python data_collection/examples/example_litellm_test.py --prompt_id=${array_id_set[$idx]} --n_trials=${N_TRIALS} --n_sessions=1 --prompts_json=lmsys_tools/prompts.json --models_json=lmsys_tools/${MODELS_SET} --exp_name=${array_exp_name[$idx]}_run-${RUN_ID}
    done

done

# python examples/example_litellm_test.py --prompt_id=33 --n_trials=${N_TRIALS} --n_sessions=1 --prompts_json=lmsys_tools/prompts.json --models_json=lmsys_tools/${MODELS_SET} --exp_name=model_set_STANDARD_run-${RUN_ID} &&

# python examples/example_litellm_test.py --prompt_id=43 --n_trials=${N_TRIALS} --n_sessions=1 --prompts_json=lmsys_tools/prompts.json --models_json=lmsys_tools/${MODELS_SET} --exp_name=model_set_THINKING_run-${RUN_ID} &&

# python examples/example_litellm_test.py --prompt_id=44 --n_trials=${N_TRIALS} --n_sessions=1 --prompts_json=lmsys_tools/prompts.json --models_json=lmsys_tools/${MODELS_SET} --exp_name=model_set_THINKING_run-${RUN_ID} &&

# python examples/example_litellm_test.py --prompt_id=19 --n_trials=${N_TRIALS} --n_sessions=1 --prompts_json=lmsys_tools/prompts.json --models_json=lmsys_tools/${MODELS_SET} --exp_name=model_set_RESTRICTED_run-${RUN_ID} &&

# python examples/example_litellm_test.py --prompt_id=20 --n_trials=${N_TRIALS} --n_sessions=1 --prompts_json=lmsys_tools/prompts.json --models_json=lmsys_tools/${MODELS_SET} --exp_name=model_set_RESTRICTED_run-${RUN_ID}
