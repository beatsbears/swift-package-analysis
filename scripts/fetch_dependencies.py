'''
Andrew Scott - Ochrona Security
1/8/2020
'''
import os
import re
from time import sleep

import requests

class SwiftPkgDependencies:

    def __init__(self, owner, repo, url, dependencies):
        self.owner = owner
        self.repo = repo
        self.url = url
        self.dependencies = dependencies
    
    def __str__(self):
        '''
        Overloading the str method to get csv format
        '''
        return f"{self.owner},{self.repo},{self.url},{'|'.join(self.dependencies)}\n"

def fetch_file(url):
    '''
    Returns raw file as a string
    '''
    try:
        resp = requests.get(url=url)
        return resp.text
    except:
        return ""

def parse_dependencies(file_contents):
    '''
    Return pattern matches
    '''
    PATTERN = '.Package\(url: "(.*)"'
    return re.findall(PATTERN, file_contents)

if __name__ == "__main__":
    with open(os.path.dirname(__file__) + '/../output/clean_found_repos.csv','r') as in_file, open(os.path.dirname(__file__) + '/../output/parsed_repos.csv','w') as out_file:
        for line in in_file:
            parts = line.rstrip("\n\r").split(',')
            print(f"Handing - {parts[1]}")
            spd = SwiftPkgDependencies(parts[0], parts[1], parts[2], parse_dependencies(fetch_file(parts[2])))
            out_file.write(str(spd))
            sleep(1)