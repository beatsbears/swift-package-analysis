import os
import re

files = ["log_v2_1", "log_v2_2", "log_v2_3", "log_v2"]
size_map = {}
SIZE_PATTERN1 = r'filename:package.swift size:(\d+)'
SIZE_PATTERN2 = r'filename:package.swift size:\d+\.\.(\d+)'
RESULT_PATTERN = r'Found (\d+) results in chunk'

def add_to_size_map(file_, spacing=2):
    with open(os.path.dirname(__file__) + f"/../output/{file_}.txt", "r") as f:
        for i, line in enumerate(f):
            try:
                if "filename:package.swift size" in line:
                    size1 = re.findall(SIZE_PATTERN1, line)[0]
                    size2 = re.findall(SIZE_PATTERN2, line)[0]
                    size = (int(size1) + int(size2))/ 2
                    size_map[i] = [size]
                if "results in chunk" in line:
                    found = re.findall(RESULT_PATTERN, line)[0]
                    size_map[i-spacing].append(found)
            except Exception as ex:
                print(ex)
                print(file_, i, line)

for f in files:
    if f == "log_v2":
        add_to_size_map(f, 3)
    else:
        add_to_size_map(f)

final_size_map = {}
for item in size_map.values():
    if len(item) == 2:
        if item[0] not in final_size_map:
            final_size_map[int(item[0])] = int(item[1])

total_items = sum(final_size_map.values())
print(sum([x*s for x, s in final_size_map.items()])/total_items)