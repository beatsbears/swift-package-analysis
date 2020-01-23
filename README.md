# Swift package usage analysis

This is a hodge-podge of scripts written to collect an analyze swift package use in public github projects.

Code is NOT production ready by any means, this was an experiment that required no small amount of tweaking along the way. i.e. Don't judge me ;)

## Data Collection
1. The first step is to search github for all repos that contain a `package.swift` file - this indicates they may be using outside dependencies. Run `python scripts/search_code.py` using various parameters for the file size in order to avoid github's code search API restrictions on the number of items that can be returned (limit 1000 per search, paged by 100). I needed to run this many times, using a size range of 1 byte in the most populated ranges, and then by larger ranges where hitting the 1000 item limit was not a concern. Results are output to `output/found_repos.csv`. I scanned from 1 byte to 200 kb.

2. If you do the first step correctly, you can ignore this step. I accidenlty ran the script for awhile with overlapping values, meaning I pulled duplicate items. Run `python scripts/dedupe.py`. Results are output to `output/clean_found_repos.csv`.

3. Step 3 is to fetch all package.swift files for the found repos and to extract their dependencies. In this early draft I'm ignoring all other metadata and version details. Run `python scripts/fetch_dependencies.py` which will output to `output/parsed_repos.csv`. This will take about 9 hours.

4. Next we will attempt to move these repos into a Graph form where packages are nodes and connections to dependencies are edges. Run `python scripts/to_graph.py` which will output a gml file to `output/package_dependencies.gml`

5. Now we'll need to use [Gephi](https://gephi.org/) to visualize our graph data and do some analysis. I imported the data in a new project and positioned the data using the ... algorithm.

6. Finally we can export a `.gexf` file named `Swift_Packages.gexf` from Gephi and place it in the `visualize/data/` directory. You can then open the `index.html` in your browser. It will take a second to render. If you see any console errors it is likely due to a CORS error from your browser. You may be able to temporarily adjust your browser settings to allow the local file access. 

The visualization code was found [here](https://victorwiard.wordpress.com/2015/01/29/using-sigma-js-to-put-gephi-graphs-and-visualizations-online/) and adjusted to fit my needs, but I can't take credit for any of the Javascript and Sigma.js configuration. 


## Result (January 2020)


