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


# adapt data_collection/examples/example_lmsys.py to your env and save it as data_collection/examples/example_lmsys_test_trials_mod.py  
for ((sess_id=0; sess_id<$SESSIONS;sess_id++))
do

    RUN_ID=$((START_RUN_ID + sess_id))
    echo $RUN_ID

    for ((idx=0;idx<$n_ids;idx++))
    do
        python data_collection/examples/example_lmsys_test_trials_mod.py --prompt_id=${array_id_set[$idx]} --n_trials=${N_TRIALS} --n_sessions=1 --prompts_json=lmsys_tools/prompts.json --models_json=lmsys_tools/${MODELS_SET} --exp_name=${array_exp_name[$idx]}_run-${RUN_ID}
    done
    
done

