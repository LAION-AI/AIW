# We will use the LMSYSChatScraper class to interact with the LMSYS API and generate responses to a prompt.
from lmsys_tools.utils import parse_model_response, get_server_id, get_cookies
from lmsys_tools.lmsys_scraper import LMSYSChatScraper
from lmsys_tools.cookies_utils import obtain_cookies
from ploting_tools.plot import plot_results
import re
import pandas as pd
import json
import os



output_dir = 'output'
os.makedirs(output_dir, exist_ok=True)


# session_hash = 'bf892vc43ca'

cookies_path = 'cookies.json'
# user_agent = obtain_cookies(file_path=cookies_path)

# with open(cookies_path, 'r') as f:
#     cookies = json.load(f)


# scraper = LMSYSChatScraper(session_hash=session_hash, cookies=cookies, user_agent=user_agent)
# set_prompt = scraper.set_prompt
# generate = scraper.generate
# reset = scraper.reset
# setup = scraper.setup


# Original problem
# prompt ='Alice has 4 brothers and she also has 1 sister. How many sisters does Alice\'s brother have? Think step by step and provide expert response. Then output your answer with following format: ### Answer:.'


# Original problem, GOLDEN PROMPT
# prompt ='Alice has 4 brothers and she also has 1 sister. How many sisters does Alice\'s brother have? To answer the question, DO NOT OUTPUT ANY TEXT EXCEPT following:  ### Answer:'

# Original problem, GOLDEN PROMPT, expert
# prompt ='Alice has 4 brothers and she also has 1 sister. How many sisters does Alice\'s brother have? To answer the question, provide expert response, thinking step by step, DO NOT OUTPUT ANY TEXT EXCEPT following:  ### Answer:'

# Original problem, REFERENCE PROMPT, PLAIN
# prompt ='Alice has 4 brothers and she also has 1 sister. How many sisters does Alice\'s brother have? To answer the question, DO NOT OUTPUT ANY TEXT EXCEPT following format that contains final answer:  ### Answer:'

# Easier problem
# prompt ='Alice has 4 sisters and she also has 1 brother. How many sisters does Alice\'s brother have? Think step by step and provide expert response. Then output your answer with following format: ### Answer:.'

# Simple version, produces sometimes text that is too long.
# prompt ='Alice has 4 sisters and she also has 1 brother. How many sisters does Alice\'s brother have? Output your answer with following format: ### Answer:.'
# EASIER VERSION: Alice has four sisters and she also has a brother. How many sisters does Alice's brother have?

# Mod 0.a, removing unnecessary . 
# prompt ='Alice has 4 sisters and she also has 1 brother. How many sisters does Alice\'s brother have? Output your answer with following format: ### Answer:'

# MOD 1
# prompt ='Alice has 4 sisters and she also has 1 brother. How many sisters does Alice\'s brother have? Output your answer strictly with following format WITHOUT ANY FURTHER TEXT: ### Answer:.'

# MOD 2 GOLDEN PROMPT (llama 2 70B chat )
# prompt ='Alice has 4 sisters and she also has 1 brother. How many sisters does Alice\'s brother have? To answer the question, DO NOT OUTPUT ANY TEXT EXCEPT following:  ### Answer:.'

# WITH DOT (GOOD WITH LLAMA 2)
# prompt ='Alice has 4 sisters and she also has 1 brother. How many sisters does Alice\'s brother have? To answer the question, DO NOT OUTPUT ANY TEXT EXCEPT following format that contains final answer:  ### Answer:.'

# *** CURRENT PROMPT ***
# WITHOUT DOT (ALSO GOOD WITH LLAMA 2)
prompt ='Alice has 4 sisters and she also has 1 brother. How many sisters does Alice\'s brother have? To answer the question, DO NOT OUTPUT ANY TEXT EXCEPT following format that contains final answer:  ### Answer:'

# MOD 3 GOLDEN PROMPT expert
# prompt ='Alice has 4 sisters and she also has 1 brother. How many sisters does Alice\'s brother have? To answer the question, provide expert response, thinking step by step, then DO NOT OUTPUT ANY TEXT EXCEPT following:  ### Answer:'

# MOD 2.A GOLDEN PROMPT EXPERT (llama 2 70B chat ). Restrinction on no more text, but expert quality (works with LLaMA 2)
# Was good for LLaMA 2 70B (20 right)
# prompt ='Alice has 4 sisters and she also has 1 brother. How many sisters does Alice\'s brother have? To answer the question, consider correct and sound expert solution, DO NOT OUTPUT ANY TEXT EXCEPT following:  ### Answer:.'

# *** EXPERT VARIANT ***
# BEST SO FAR (23 right)
# prompt ='Alice has 4 sisters and she also has 1 brother. How many sisters does Alice\'s brother have? To answer the question, consider correct and sound expert solution, DO NOT OUTPUT ANY TEXT EXCEPT following format that contains final answer:  ### Answer:.'

# SAME WITHOUT DOT
# prompt ='Alice has 4 sisters and she also has 1 brother. How many sisters does Alice\'s brother have? To answer the question, consider correct and sound expert solution, DO NOT OUTPUT ANY TEXT EXCEPT following format that contains final answer:  ### Answer:'


# prompt ='Alice has 4 sisters and she also has 1 brother. How many sisters does Alice\'s brother have? Consider correct and sound expert solution. DO NOT OUTPUT ANY TEXT EXCEPT following format that contains final answer:  ### Answer:.'

# THIS GETS WORSE FOR LLAMA-2 (removing DO NOT OUTPUT ANY OTHER TEXT restriction)
# prompt ='Alice has 4 sisters and she also has 1 brother. How many sisters does Alice\'s brother have? After considering correct and sound expert solution. provide final answer in the following format:  ### Answer:.'

# TRIED FOR LLAMA 3, FAILS 
# Alice has 4 sisters and she also has 1 brother. How many sisters does Alice's brother have? Produce correct and sound expert solution. Provide final answer in the following format:  ### Answer:

# MOD 2.B GOLDEN PROMPT EXPERT (llama 2 70B chat ). Removing demand for no text except final answer
# prompt ='Alice has 4 sisters and she also has 1 brother. How many sisters does Alice\'s brother have? To answer the question, consider correct and sound expert solution. Output your final answer with following format:  ### Answer:.'

model_type = "llama-3-8b-70b-instruct"
# model_type = "llama-3-70b-instruct"
# model_type = "llama-2-70b-chat"
# model_type = "llama-2-7b-chat"
# model_type = "llama-2-13b-chat"
# model_type = "command-r-plus"
# exp_type = "WITH_DOT_PLAIN"
# exp_type = "WITHOUT_DOT_PLAIN"
# exp_type = "WITHOUT_DOT_PLAIN_RUN-2"
# exp_type = "ORIGINAL_PLAIN_RUN-1"
exp_type = "PLAIN_RUN-1"
# exp_type = "ORIGINAL_PLAIN_RUN-2"
# exp_type = "WITHOUT_DOT_EXPERT"

models = [
    "llama-3-70b-instruct",
    "llama-3-8b-instruct"
    # "llama-2-70b-chat"
    # "llama-2-13b-chat"
    # "llama-2-7b-chat"
    # "claude-3-opus-20240229",
    # "command-r-plus"
    # "mixtral-8x7b-instruct-v0.1",
    # "mistral-large-2402",
    # "qwen1.5-72b-chat",
    # "dbrx-instruct"
    ]

# Original problem
# right_answer = '2'

# Easier problem
right_answer = '5'

n_trials = 10

# n_sessions = 2
n_sessions = 3


cookies_path = 'cookies.json'
session_hash = '3m46r1tvrm8'
# session_hash = 'bf892vc43ca'


data = []
for session in range(n_sessions): 
    user_agent = obtain_cookies(file_path=cookies_path)

    with open(cookies_path, 'r') as f:
        cookies = json.load(f)
    scraper = LMSYSChatScraper(session_hash=session_hash, cookies=cookies, user_agent=user_agent)
    set_prompt = scraper.set_prompt
    generate = scraper.generate
    reset = scraper.reset
    setup = scraper.setup
    for model in models:
        
    
        for trial in range(n_trials):
            print(f'Model: {model}, Trial: {trial+1}, session: {session+1}')
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
                parsed_answer = re.findall(r'Answer:.*?(\d+)', model_response)[0]
            except:
                print(f'Error parsing model response for model {model}')
                print(f'Output: {output}. Skipping...')
                continue
            
            
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

            data.append(output_dict)


            reset(trigger_id=100, fn_index=37)


df = pd.DataFrame(data)
print(df)
output_path = f'{output_dir}/{n_trials}_{n_sessions}_{model_type}_{exp_type}.json'
df.to_json(output_path, orient='records')