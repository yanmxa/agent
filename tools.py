import httpx
import requests
import os
from dotenv import load_dotenv
import json
from datetime import datetime, timedelta

# Load environment variables from .env file
load_dotenv()

def wikipedia(q):
    return httpx.get("https://en.wikipedia.org/w/api.php", params={
        "action": "query",
        "list": "search",
        "srsearch": q,
        "format": "json"
    }).json()["query"]["search"][0]["snippet"]

def calculate(what):
    return eval(what)


def google(query):
    headers = {
        'X-API-KEY': os.environ['SERPER_API_KEY'],
        'Content-Type': 'application/json',
    }
    payload = {
        'q': query,
        'num': 5  # Number of search results to return
    }
    response = requests.post("https://google.serper.dev/search", json=payload, headers=headers)
    if response.status_code == 200:
      # for idx, result in enumerate(results.get('organic', []), start=1):
        rets = []
        for idx, result in enumerate(response.json().get('organic', []), start=1):
          rets.append(result.get('snippet'))
        return "; ".join(rets)
    else:
        response.raise_for_status()

def news(query):
  param = {
    "q": query,
    "size": 5,
    "apikey": os.environ['NEWS_API_KEY']
  }

  response = requests.get("https://newsdata.io/api/1/latest",  params=param)

  if response.status_code == 200:
      rets = []
      for idx, result in enumerate(response.json().get('results', []), start=1):
        rets.append(result.get('description'))
      return "; ".join(rets)
  else:
      return response.raise_for_status()
    
known_actions = {
    "wikipedia": wikipedia,
    "google": google,
    "news": news
}