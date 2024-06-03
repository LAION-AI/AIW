OUTPUT_PATTERN="{}_prompt.pdf"

JSONS_DIR="collected_responses"
SCRIPT_PATH="scripts/plot.py"
PROMPT_ID="55,56,63,69,57,58,64,70,53,54,65,71"
PROMPTS_JSON="prompts/prompts.json"


echo "Plotting for prompts $PROMPT_ID"
echo "Output pattern: $OUTPUT_PATTERN"

CMD="python3 $SCRIPT_PATH \
    --output $OUTPUT_PATTERN \
    --jsons_dir $JSONS_DIR \
    --prompt_id $PROMPT_ID \
    --prompts_json $PROMPTS_JSON"

echo $CMD
$CMD


PROMPT_ID="91,92,93"

echo "Plotting for prompts $PROMPT_ID"
echo "Output pattern: $OUTPUT_PATTERN"

CMD="python3 $SCRIPT_PATH \
    --output $OUTPUT_PATTERN \
    --jsons_dir $JSONS_DIR \
    --prompt_id $PROMPT_ID \
    --prompts_json $PROMPTS_JSON"

echo $CMD
$CMD