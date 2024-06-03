# We will use the LMSYSChatScraper class to interact with the LMSYS API and generate responses to a prompt.
from lmsys_tools.utils import parse_model_response, get_server_id, get_cookies
from lmsys_tools.lmsys_scraper import LMSYSChatScraper
from lmsys_tools.cookies_utils import obtain_cookies

import re
import pandas as pd
import json
import os
import time
import argparse
import random
import uuid


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Run LMSYS chat scraper')
    parser.add_argument('--prompt_id', type=int, default=1, help='Prompt id')
    parser.add_argument('--n_trials', type=int, default=10, help='Number of trials')
    parser.add_argument('--n_sessions', type=int, default=2, help='Number of sessions')
    parser.add_argument('--output_dir', type=str, default='output', help='Output directory')
    parser.add_argument('--prompts_json', type=str, default='prompts.json', help='Path to prompts json file')
    parser.add_argument('--models_json', type=str, default='models.json', help='Path to models json file')
    parser.add_argument('--exp_name', type=str, default='aiw', help='Experiment Name')
    args = parser.parse_args()
    output_dir = args.output_dir
    exp_name = args.exp_name
    os.makedirs(output_dir, exist_ok=True)


    session_hash = 'km4n5rqtn9b'

    cookies_path = 'cookies.json'
    prompts_json = args.prompts_json
    prompt_id = args.prompt_id

    with open(prompts_json, 'r') as f:
        prompts = json.load(f)

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


    ookies_path = 'cookies.json'

    data = []
    for session in range(n_sessions): 
        random.shuffle(models)
        # sess_id = str(uuid.uuid4())
        # user_agent = obtain_cookies(file_path=cookies_path)

        # with open(cookies_path, 'r') as f:
        #     cookies = json.load(f)
        # print(cookies)
        # scraper = LMSYSChatScraper(
        #     session_hash=session_hash, 
        #     cookies=cookies,
        #     user_agent=user_agent,
        #     models_json_path=models_json
        #     )
        
        for model in models:

            user_agent = obtain_cookies(file_path=cookies_path)

            with open(cookies_path, 'r') as f:
                cookies = json.load(f)
            print(cookies)
            scraper = LMSYSChatScraper(
                session_hash=session_hash, 
                cookies=cookies,
                user_agent=user_agent,
                models_json_path=models_json
                )
            set_prompt = scraper.set_prompt
            generate = scraper.generate
            reset = scraper.reset
            setup = scraper.setup
            
            
        
            for trial in range(n_trials):
                time.sleep(5)
                print(f'Model: {model}, Trial: {trial+1}, session: {session+1}')
                # if trial > 0:
                #     r = reset(trigger_id=99, fn_index=39)
                #     print(r)
                #     r = set_prompt(prompt, model)
                #     print(r)
                #     r = setup()
                #     print(r)
                # else:
                r = reset(trigger_id=92, fn_index=39) # reset, 99 regenerate
                
                print(r)
                r = reset(trigger_id=100, fn_index=37)
                print(r)

                r = set_prompt(prompt, model)

                if not r:
                    continue

                r = setup()
                if not r:
                    continue

                r = generate()

                try:
            
                    output = parse_model_response(r)['output']['data'][1][0]
                except Exception as e:
                    print(parse_model_response(r))
                    print(f'Error {e} parsing model response for model {model}')
                    continue
                if 'RATE LIMIT OF THIS MODEL IS REACHED' in output:
                    print(f'Rate limit reached for model {model}. Skipping...')
                    continue
                try:
                    prompt, model_response = output
                    model_response = model_response.replace('\n', ' ')
                    parsed_answer = re.findall(r'answer:.*?(\d+)', model_response.lower())[0]
                except:
                    try:
                        parsed_answer = re.findall(r'has.*?(\d+)', model_response.lower())[0]
                    except:
                        print(f'Error parsing model response for model {model}')
                        print(f'Output: {output}. ')
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
                print(output_dict)

                # save output_dict to a file

                with open(output_path, 'a') as f:
                    f.write(json.dumps(output_dict, indent=4)+'\n')
                data.append(output_dict)
            # time.sleep(100)


                reset(trigger_id=100, fn_index=37)



    df = pd.DataFrame(data)
    print(df)
    
    # df.to_json(output_path, orient='records', indent=4)
