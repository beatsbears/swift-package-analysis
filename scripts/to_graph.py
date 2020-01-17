import os
import re
import networkx as nx

G = nx.Graph()

def _url_to_name(url):
    return url.replace('https://github.com/', '').replace('.git', '')

data = []
with open(os.path.dirname(__file__) + "/../output/parsed_repos.csv", "r") as file:
    for line in file:
        try:
            owner, url, raw, deps = line.split(",")
            data += [(url, deps.rstrip())]
        except ValueError:
            weird_data = line.split(",")
            owner, url, raw = weird_data[0:3]
            deps = []
            for val in weird_data[3:]:
                for v in val.split("|"):
                    deps = deps + re.findall(r'(https\://\S+)', v.replace("\"", ""))
            data += [(url, "|".join(deps))]

for val in data:
    url, deps = val
    G.add_node(f"{_url_to_name(url)}")

for val in data:
    url, deps = val
    for dep in deps.split('|'):
        if len(dep) > 0:
            G.add_edge(f"{_url_to_name(url)}", f"{_url_to_name(dep)}")

nx.write_gml(G, os.path.dirname(__file__) + "/../output/package_dependencies.gml")