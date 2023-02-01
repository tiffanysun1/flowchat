import cohere
import json
from dotenv import load_dotenv
import os
import requests

load_dotenv()

BING_API_KEY = os.getenv("BING_API_KEY")
BING_API_ENDPOINT = os.getenv("BING_API_ENDPOINT")
COHERE_API_KEY = os.getenv('COHERE_API_KEY')

if not COHERE_API_KEY:
    raise Exception('COHERE_API_KEY not set')


def pprint(obj):
    print(json.dumps(obj, indent=2))


co = cohere.Client(COHERE_API_KEY, '2022-12-06')

""""
> User: where is my package?
> Bot: Could you tell me your order number?

> Bot: Your package is on its way. It should arrive in 2 days.
"""


def bing_search(search_term: str):
    headers = {"Ocp-Apim-Subscription-Key": BING_API_KEY}
    params = {"q": search_term, }
    response = requests.get(BING_API_ENDPOINT, headers=headers, params=params)
    response.raise_for_status()
    search_results = response.json()
    return search_results


results = bing_search(
    "site:https://help.doordash.com my food isn't here yet")
web_pages = results["webPages"]["value"]
pprint(web_pages)


def on_chat_message(chat_history: list[str], helpdesk_url: str):
    search_str = f"site:{helpdesk_url} {chat_history[-1]}"
    search_query = bing_search(search_str)

    return {
        "response": ""
    }
