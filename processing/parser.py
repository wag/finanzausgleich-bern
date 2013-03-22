import json
from collections import defaultdict

year = 2012
csv_file = 'csv/{0}.csv'.format(year)
json_file = 'json/{0}.json'.format(year)

output_json = {
    "nodes": [],
    "links": []
}

left_municipality = {}
left_section = {}
container = {}
right_section = {}
right_municipality = {}

section_value = {
    'left': defaultdict(lambda: defaultdict(lambda: 0)),
    'right': defaultdict(lambda: defaultdict(lambda: 0))
}

node_counter = 0

with open(csv_file, 'r') as f:
    lines = f.readlines()

header = lines[0].rstrip().split(',')
for i in range(2, len(header)):
    output_json["nodes"].append({"node": node_counter, "name": header[i]})
    container[header[i]] = node_counter
    node_counter += 1

for line in lines[1:]:
    parts =  line.rstrip().split(',')
    municipality = parts[0]
    section = parts[1]

    # if municipality not in [v["name"] for v in output_json["nodes"]] or municipality == section:
    #     output_json["nodes"].append({"node": node_counter, "name": municipality})
    #     left_municipality[municipality] = node_counter
    #     node_counter += 1
    #     output_json["nodes"].append({"node": node_counter, "name": municipality})
    #     right_municipality[municipality] = node_counter
    #     node_counter += 1

    if section not in [v["name"] for v in output_json["nodes"]]: # or municipality == section:
        has_left = has_right = False
        for _line in lines[1:]:
            _line = _line.rstrip().split(',')
            if section == _line[1]:
                numbers = [float(v) for v in _line[2:]]
                if min(numbers) < 0:
                    has_left = True
                if max(numbers) > 0:
                    has_right = True
                if has_left and has_right:
                    break
        if has_left:
            output_json["nodes"].append({"node": node_counter, "name": section})
            left_section[section] = node_counter
            node_counter += 1
        if has_right:
            output_json["nodes"].append({"node": node_counter, "name": section})
            right_section[section] = node_counter
            node_counter += 1

for line in lines[1:]:
    parts =  line.rstrip().split(',')
    section = parts[1]

    for i in range(2, len(header)):
        value = round(float(parts[i]), 2)
        # Left side, donator
        if value < 0:
            section_value['left'][section][i] += value
        # Right side, receiver
        if value > 0:
            section_value['right'][section][i] += value

for section in set([v.split(',')[1] for v in lines[1:]]):
    for i in range(2, len(header)):
        if section_value['left'][section][i] != 0:
            output_json["links"].append({
                "source": left_section[section],
                "target": container[header[i]],
                "value": -section_value['left'][section][i]
            })
        if section_value['right'][section][i] != 0:
            output_json["links"].append({
                "source": container[header[i]],
                "target": right_section[section],
                "value": section_value['right'][section][i]
            })

# for line in lines[1:]:
#     parts =  line.rstrip().split(',')
#     municipality = parts[0]
#     section = parts[1]

#     for i in range(2, len(header)):
#         value = round(float(parts[i]), 2)
#         # Left side, donator
#         if value < 0:
#             output_json["links"].append({
#                 "source": left_municipality[municipality],
#                 "target": left_section[section],
#                 "value": -value
#             })

#         # Right side, receiver
#         if value > 0:
#             output_json["links"].append({
#                 "source": right_section[section],
#                 "target": right_municipality[municipality],
#                 "value": value
#             })
#         # 0 values are getting ignored

json.dump(output_json, open(json_file, 'w'))
