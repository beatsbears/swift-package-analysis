import os

import requests
from requests.auth import HTTPBasicAuth

GITHUB_USER = os.environ['GITHUB_USER']
GITHUB_API_KEY = os.environ['GITHUB_API_KEY']

def get_top(sort_type):
    url = f"https://api.github.com/search/repositories?q=swift+language:swift&sort={sort_type}&order=desc"
    resp = requests.get(url=url, 
        auth=HTTPBasicAuth(GITHUB_USER, GITHUB_API_KEY)
    )
    return resp.json()

if __name__ == "__main__":
    top_stars = get_top("stars").get("items", [])
    for repo in top_stars[:20]:
        print(f"{repo['name']},{repo['html_url']},{repo['stargazers_count']}")

    print("\n\n")
    top_stars = get_top("forks").get("items", [])
    for repo in top_stars[:20]:
        print(f"{repo['name']},{repo['html_url']},{repo['forks_count']}")