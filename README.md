<h1 align="center">
        🎩🐇 Alice in Wonderland: Simple Tasks Showing Complete Reasoning Breakdown in State-Of-the-Art Large Language Models
    </h1>
 <p align="center">Alice in Wonderland code base for experiments and raw experiments data</p>
<h4 align="center"><a href="https://marianna13.github.io/aiw/" target="_blank">Homepage</a> | <a href="https://docs.litellm.ai/docs/hosted" target="_blank"> Paper</a> | <a href="https://docs.litellm.ai/docs/enterprise"target="_blank">Arxiv</a></h4>


## Usage

Install requirements:
`pip install requirements.txt`

### Collect experiments data

#### Collect using [LiteLLM](https://github.com/BerriAI/litellm)
Refer to the [LiteLLM Docs](https://docs.litellm.ai/docs/) on how to setup your account and API keys.

Refer to [this bash script](scripts/execute_litellm_data_gathering.sh) to see how to use litellm to gather model responses.

#### Collect using [TogetherAI](https://www.together.ai/)

Refer to the [TogetherAI Docs](https://docs.together.ai/docs/quickstart) on how to setup your account and API keys.

Refer to [this Python script](data_collection/examples/example_together.py) to see how to use togetherAI to gather model responses.

#### Colect by scraping [LMSYS Chatbot Arena](https://chat.lmsys.org/) 
**Important note** This method is not recommended since it's limited and can violate LMSYS' ToS.

Refer to [this bash script](scripts/execute_lmsys_data_gathering.sh) to see how to use litellm to gather model responses.


## Plot the data

Run script to generate plots from the paper (by deafault plots will be saved in the working directory):
`bash scripts/plot.sh`
