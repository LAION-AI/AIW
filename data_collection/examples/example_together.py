import re
import pandas as pd
import json
import os
import time
import argparse
import random
import uuid
from lmsys_tools.utils import parse_model_response
from litellm import completion

import os
import together
together.api_key = os.getenv("TOGETHERAI_API_KEY") 

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Run LMSYS chat scraper')
    parser.add_argument('--prompt_id', type=int, nargs='+', default=[1], help='Prompt id')
    parser.add_argument('--n_trials', type=int, default=10, help='Number of trials')
    parser.add_argument('--n_sessions', type=int, default=1, help='Number of sessions')
    parser.add_argument('--output_dir', type=str, default='output', help='Output directory')
    parser.add_argument('--prompts_json', type=str, default='prompts.json', help='Path to prompts json file')
    parser.add_argument('--models_json', type=str, default='models.json', help='Path to models json file')
    parser.add_argument('--exp_name', type=str, default='aiw', help='Experiment Name')

    args = parser.parse_args()
    output_dir = args.output_dir
    exp_name = args.exp_name
    os.makedirs(output_dir, exist_ok=True)
    prompts_json = args.prompts_json
    prompt_id = args.prompt_id
    with open(prompts_json, 'r') as f:
        prompts = json.load(f)
    data = []
    for prompt_id in args.prompt_id:
        prompt_data = [p for p in prompts if p['id'] == prompt_id][0]
        prompt = prompt_data['prompt']
        right_answer = prompt_data['right_answer']
        models_json = args.models_json
        with open(models_json, 'r') as f:
            models = json.load(f)
        n_trials = args.n_trials
        n_sessions = args.n_sessions
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        output_path = f'{output_dir}/{exp_name}_{prompt_id}-promptid_{n_trials}-trials_{n_sessions}-sessions_{timestamp}.json'
        for session in range(n_sessions): 
            random.shuffle(models)
            for model in models:
                for trial in range(n_trials):
                    messages = [{ "content": prompt,"role": "user"}]
                    response = together.Complete.create(
                      prompt = prompt, 
                      model = model, 
                      temperature=0.7,
                      top_p=0.7,    
                      top_k=50,
                      repetition_penalty=1,
                    )
                    model_response = prompt + response['choices'][0]['text']
                    try:
                        model_response = model_response.replace('\n', ' ')
                        parsed_answer = re.findall(r'answer:.*?(\d+)', model_response.lower())[0]
                    except:
                        try:
                            parsed_answer = re.findall(r'has.*?(\d+)', model_response.lower())[0]
                        except:
                            print(f'Error parsing model response for model {model}')
                            parsed_answer = None
                    
                    output_dict = {
                        'model': model,
                        'prompt': prompt,
                        'model_response': model_response,
                        'parsed_answer': parsed_answer,
                        'correct': parsed_answer == right_answer,
                        'trial': trial,
                        'total_trials': n_trials,
                        'right_answer': right_answer,
                        'session': session,
                        'n_sessions': n_sessions,
                    }
                    print(model, "Response:", model_response, "Parsed Response:", parsed_answer, "Correct ? ", parsed_answer == right_answer)
                    data.append(output_dict)
                    #with open(output_path, 'a') as f:
                    #    f.write(json.dumps(output_dict, indent=4))
                    df = pd.DataFrame(data)
                    df.to_json(output_path, orient='records', indent=4)

    df = pd.DataFrame(data)
    df.to_json(output_path, orient='records', indent=4)
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    output_path = f'{output_dir}/{exp_name}_{prompt_id}-promptid_{n_trials}-trials_{n_sessions}-sessions_{timestamp}.json'
