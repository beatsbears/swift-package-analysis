'''
Andrew Scott - Ochrona Security
1/8/2020
'''
import os
import re

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
    except Exception as ex:
        print(ex)
        return ""

def parse_dependencies(file_contents):
    '''
    Return pattern matches
    '''
    PATTERN = r'url: \"(https\://\S+)\"'
    return re.findall(PATTERN, file_contents)

if __name__ == "__main__":
    with open(os.path.dirname(__file__) + '/../output/found_repos.csv','r') as in_file, open(os.path.dirname(__file__) + '/../output/parsed_repos.csv','w') as out_file:
        for line in in_file:
            parts = line.rstrip("\n\r").split(',')
            print(f"Handing - {parts[1]}")
            spd = SwiftPkgDependencies(parts[0], parts[1], parts[3], parse_dependencies(fetch_file(parts[3])))
            out_file.write(str(spd))
