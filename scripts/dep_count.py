import os

from statistics import median

data = {}
with open(os.path.dirname(__file__) + "/../output/parsed_repos_v2.csv", "r") as file:
    for line in file:
        parts = line.split(",")
        data[parts[1]] = parts[3].replace("\n", "").split("|") or []

# Most used dependencies
dependency_count = {}
for _, v in data.items():
    for dep in v:
        if dep in dependency_count:
            dependency_count[dep] += 1
        else:
            dependency_count[dep] = 0


# returns 21 packages
sorted_set = {k: v for k, v in sorted(dependency_count.items(), key=lambda x: x[1], reverse=True) if v > 197}
for val in [(k, v) for k, v in sorted_set.items()]:
    print(f"{val[0]}, {val[1]}")

# mean and median counts
counts = {}
for k, v in data.items():
    if v == [""]:
        counts[k] = 0
    else:
        counts[k] = len(v)

counts = {k: v for k, v in counts.items() if k and v > 0}

print(f"MEAN: {sum(counts.values())/len(counts.values())}")
print(f"MEDIAN: {median(counts.values())}")