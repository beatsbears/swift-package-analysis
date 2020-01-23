'''
Andrew Scott - Ochrona Security
1/6/2020
'''
if __name__ == "__main__":
    with open('found_repos.csv','r') as in_file, open('clean_found_repos.csv','w') as out_file:
        seen = set()
        for line in in_file:
            if line in seen: 
                continue

            seen.add(line)
            out_file.write(line)