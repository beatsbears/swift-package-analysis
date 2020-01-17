# Swift package usage analysis

This is a hodge-podge of scripts written to collect an analyze swift package use in public github projects.

Code is NOT production ready by any means, this was just an experiment that required tweaking along the way. i.e. Don't judge me ;)

The analysis code leverages graph theory to analyze the relationships between different packages.


## Data Collection
1. The first step is to search github for all repos that contain a `package.swift` file - this indicates they may be using outside dependencies. Run `python search_code.py` using various parameters for the file size in order to avoid github's code search API restrictions on the number of items that can be returned (limit 1000 per search, paged by 100). I needed to run this many times, using a size range of 1 byte in the most populated ranges, and then by larger ranges where hitting the 1000 item limit was not a concern. Results are output to `found_repos.csv`. I scanned from 1 byte to 200 kb.

2. If you do this right, you can ignore this step. I accidenlty ran the script for awhile with overlapping values, meaning I pulled duplicate items. Run `python dedupe.py`. Results are output to `clean_found_repos.csv`.

3. Step 3 is to fetch all package.swift files for the found repos and to extract their dependencies. In this early draft I'm ignoring all other metadata and version details. Run `python fetch_dependencies` which will output to `parsed_repos.csv`.

4. Next we will attempt to move these repos into a Graph form where packages are nodes and connections to dependencies are edges.

