'''
Andrew Scott - Ochrona Security
1/3/2020
'''
import os
import csv
from time import sleep

import requests
from requests.auth import HTTPBasicAuth

GITHUB_USER = os.environ['GITHUB_USER']
GITHUB_API_KEY = os.environ['GITHUB_API_KEY']

def get_page(page_num, base_size, range_size):
    url = "https://api.github.com/search/code"

    querystring = {"q":f"package filename:package.swift size:{base_size}..{(base_size+999)}", 
                   "page": page_num, 
                   "per_page": 100}
    resp = requests.get(url=url, 
        params=querystring, 
        auth=HTTPBasicAuth(GITHUB_USER, GITHUB_API_KEY)
    )
    print(f"Query - {querystring}")
    return resp.json()

def parse_item(item):
    '''
    Interesting fields:
        owner.login - This is the repo owner
        html_url - browser friendly repo name
        raw_file_url - self-generated, so we can pull raw text later
    '''
    resp = {}
    resp["owner"] = item.get("repository", {}).get("owner", {}).get("login", "unknown")
    resp["repo"] = item.get("repository", {}).get("html_url", "unknown")
    resp["file_link"] = item.get("html_url")
    resp["raw_link"] = create_raw_link(item.get("html_url"))
    return resp

def create_raw_link(url):
    '''
    html_url to raw url transformer

    ex.
        https://github.com/MaherKSantina/MSAutoView/blob/1bf6891b4681f74c6bb7ea8a03056456fa9ea830/Package.swift
        ...
        https://raw.githubusercontent.com/MaherKSantina/MSAutoView/1bf6891b4681f74c6bb7ea8a03056456fa9ea830/Package.swift
    '''
    if url is not None:
        parts = url.split('/')
        return f"https://raw.githubusercontent.com/{parts[3]}/{parts[4]}/{parts[6]}/{'/'.join(parts[7:])}"
    else:
        return "NA"

def write_to_file(item):
    with open(os.path.dirname(__file__) + '/../output/found_repos.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow(item.values())

if __name__ == "__main__":
    # Start file size at
    _start_size = 20001

    # Stop running the script once you hit this file size
    _max_size = 200000

    # How large of a range to search each time
    _file_size_range = 1000

    for _run_size in range(_start_size, _max_size, _file_size_range):
        _full_results = False
        _page = 1
        _total_pages = 0

        while not _full_results:
            try:
                page = get_page(_page, _run_size, _file_size_range)
                # if we don't know how many total pages to fetch, calculate it
                if _total_pages == 0:
                    _total_pages = int(int(page["total_count"]) / 100) + 1
                    if _total_pages > 10:
                        print("Overriding to only collect 10 pages from chunk")
                        _total_pages = 10
                
                # notify
                print(f"Processing page {_page} of {_total_pages}")
                print(f"Found {page['total_count']} results in chunk")
                _page += 1

                # handle results
                if "items" in page:
                    for item in page["items"]:
                        write_to_file(parse_item(item))
                else:
                    print(page)
                
                # see if we're done
                if _page > _total_pages:
                    _full_results = True
            except Exception as ex:
                print(f"EXCEPTION: {ex}")

            sleep(6) # avoid rate limiting

