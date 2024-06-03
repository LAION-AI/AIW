# Description: A class to scrape the LMSYS chatbot

import requests
import json
import sys
import os


class LMSYSChatScraper:
    """
    A class to scrape the LMSYS chatbot
    """

    def __init__(self, session_hash, cookies=None, user_agent=None, models_json_path='./models.json'):
        """
        Initialize the LMSYS chat scraper
        Args:
            session_hash (str): The session hash
        """

        self.session_hash = session_hash
        self.cookies = cookies
        self.user_agent = user_agent

        with open(models_json_path, 'r') as f:
            self.models = json.load(f)

    def set_prompt(self, prompt, model):
        """
        Set the prompt for the chatbot
        Args:
            prompt (str): The prompt to set
            model (str): The model to use
        Returns:
            bool: True if the prompt was set successfully, False otherwise
        
        """

        if model not in self.models:
            assert f"Model {model} not found in the list of models" \
                    f"Available models: {self.models}"


        headers = {
            'User-Agent': self.user_agent if self.user_agent else 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.5',
            # 'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://chat.lmsys.org/',
            'Content-Type': 'application/json',
            'Origin': 'https://chat.lmsys.org',
            'Connection': 'keep-alive',
            # 'Cookie': '__cf_bm=JWgdEvavCGDiohv.4agpDtthJyHxEYthta2am4h5RLA-1714122804-1.0.1.1-rI7xsaTGTiNZt1zyagYPy2Ees5_o5hUE4VkAGMvUJvOlJ5qmx.m32JvS9F3uq9YkmXCR7FvhUsnl5OAZNlQ1ew; cf_clearance=Imb_KWLGSx5SqKp2XCKtFtZlwLSOYdO0ZPWqn1pxCt4-1714122858-1.0.1.1-Tr2cn..jnPIcEL2uQke3A_9pPReh0IXd5amq8MY.i6m.ktQyqvwgFoGYnaHuRGdIxg3oKbLYTD1tWqsDJ8aHhA; SERVERID=S2|ZitxH; _ga_K6D24EE9ED=GS1.1.1714122834.1.1.1714122859.0.0.0; _ga=GA1.2.592274911.1714122834; _ga_R1FN4KJKJH=GS1.1.1714122834.1.1.1714122860.0.0.0; _gid=GA1.2.129336038.1714122837',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            # Requests doesn't support trailers
            # 'TE': 'trailers',
        }

        params = ''

        json_data = {
            'data': [
                None,
                model,
                prompt,
                None,
            ],
            'event_data': None,
            'fn_index': 39,
            'trigger_id': 92,
            'session_hash': self.session_hash,
        }

        response = requests.post('https://chat.lmsys.org/queue/join', params=params, cookies=self.cookies, headers=headers, json=json_data)
        if response.status_code != 200:
            print(response.status_code)
        return response.status_code == 200


    def generate(self):
        """
        Generate a response from the chatbot
        Returns:
            requests.Response: The response from the chatbot
        """

        headers = {
            'User-Agent': self.user_agent if self.user_agent else 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/',
            'Accept': 'text/event-stream',
            'Accept-Language': 'en-US,en;q=0.5',
            # 'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Referer': 'https://chat.lmsys.org/',
            # 'Cookie': '__cf_bm=JWgdEvavCGDiohv.4agpDtthJyHxEYthta2am4h5RLA-1714122804-1.0.1.1-rI7xsaTGTiNZt1zyagYPy2Ees5_o5hUE4VkAGMvUJvOlJ5qmx.m32JvS9F3uq9YkmXCR7FvhUsnl5OAZNlQ1ew; cf_clearance=Imb_KWLGSx5SqKp2XCKtFtZlwLSOYdO0ZPWqn1pxCt4-1714122858-1.0.1.1-Tr2cn..jnPIcEL2uQke3A_9pPReh0IXd5amq8MY.i6m.ktQyqvwgFoGYnaHuRGdIxg3oKbLYTD1tWqsDJ8aHhA; SERVERID=S2|ZitxH; _ga_K6D24EE9ED=GS1.1.1714122834.1.1.1714122859.0.0.0; _ga=GA1.2.592274911.1714122834; _ga_R1FN4KJKJH=GS1.1.1714122834.1.1.1714122860.0.0.0; _gid=GA1.2.129336038.1714122837',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            # Requests doesn't support trailers
            # 'TE': 'trailers',
        }
        params = {
            'session_hash': self.session_hash,
        }

        response = requests.get('https://chat.lmsys.org/queue/data', params=params, cookies=self.cookies, headers=headers)
        return response

    def reset(self, trigger_id, fn_index=35):
        """
        Reset the chatbot
        Args:
            trigger_id (int): The trigger ID
            fn_index (int): The function index
        Returns:
            bool: True if the chatbot was reset successfully, False otherwise
        """

        headers = {
            'User-Agent': self.user_agent if self.user_agent else 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.5',
            # 'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://chat.lmsys.org/',
            'Content-Type': 'application/json',
            'Origin': 'https://chat.lmsys.org',
            'Connection': 'keep-alive',
            # 'Cookie': '__cf_bm=JWgdEvavCGDiohv.4agpDtthJyHxEYthta2am4h5RLA-1714122804-1.0.1.1-rI7xsaTGTiNZt1zyagYPy2Ees5_o5hUE4VkAGMvUJvOlJ5qmx.m32JvS9F3uq9YkmXCR7FvhUsnl5OAZNlQ1ew; cf_clearance=Imb_KWLGSx5SqKp2XCKtFtZlwLSOYdO0ZPWqn1pxCt4-1714122858-1.0.1.1-Tr2cn..jnPIcEL2uQke3A_9pPReh0IXd5amq8MY.i6m.ktQyqvwgFoGYnaHuRGdIxg3oKbLYTD1tWqsDJ8aHhA; SERVERID=S2|ZitxH; _ga_K6D24EE9ED=GS1.1.1714122834.1.1.1714122859.0.0.0; _ga=GA1.2.592274911.1714122834; _ga_R1FN4KJKJH=GS1.1.1714122834.1.1.1714122860.0.0.0; _gid=GA1.2.129336038.1714122837',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            # Requests doesn't support trailers
            # 'TE': 'trailers',
        }

        params = ''

        json_data = {
            'data': [
                None,
            ],
            'event_data': None,
            'fn_index': fn_index,
            'trigger_id': trigger_id,
            'session_hash': self.session_hash,
        }

        response = requests.post('https://chat.lmsys.org/queue/join', params=params, cookies=self.cookies, headers=headers, json=json_data)
        if response.status_code != 200:
            print(response.status_code)
            print(response.text)
            # print(response.text)
        return response.status_code == 200
    
    def setup(self, temperature=0.7, top_p=1, max_output_tokens=1024):
        """
        Setup the chatbot
        Args:
            temperature (float): The temperature
            top_p (float): The top p
            max_output_tokens (int): The maximum output tokens
        Returns:
            bool: True if the chatbot was setup successfully, False otherwise
        """
        headers = {
            'User-Agent': self.user_agent if self.user_agent else 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.5',
            # 'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://chat.lmsys.org/',
            'Content-Type': 'application/json',
            'Origin': 'https://chat.lmsys.org',
            'Connection': 'keep-alive',
            # 'Cookie': '__cf_bm=JWgdEvavCGDiohv.4agpDtthJyHxEYthta2am4h5RLA-1714122804-1.0.1.1-rI7xsaTGTiNZt1zyagYPy2Ees5_o5hUE4VkAGMvUJvOlJ5qmx.m32JvS9F3uq9YkmXCR7FvhUsnl5OAZNlQ1ew; cf_clearance=Imb_KWLGSx5SqKp2XCKtFtZlwLSOYdO0ZPWqn1pxCt4-1714122858-1.0.1.1-Tr2cn..jnPIcEL2uQke3A_9pPReh0IXd5amq8MY.i6m.ktQyqvwgFoGYnaHuRGdIxg3oKbLYTD1tWqsDJ8aHhA; SERVERID=S2|ZitxH; _ga_K6D24EE9ED=GS1.1.1714122834.1.1.1714122859.0.0.0; _ga=GA1.2.592274911.1714122834; _ga_R1FN4KJKJH=GS1.1.1714122834.1.1.1714122860.0.0.0; _gid=GA1.2.129336038.1714122837',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            # Requests doesn't support trailers
            # 'TE': 'trailers',
        }

        params = ''

        json_data = {
            'data': [
                None,
                temperature,
                top_p,
                max_output_tokens,
            ],
            'event_data': None,
            'fn_index': 42,
            'trigger_id': 93,
            'session_hash': self.session_hash,
        }

        response = requests.post('https://chat.lmsys.org/queue/join', params=params, cookies=self.cookies, headers=headers, json=json_data)
        if response.status_code != 200:
            print(response.status_code)
        return response.status_code == 200

