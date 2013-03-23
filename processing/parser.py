import json
from collections import defaultdict

year = 2012
csv_file = 'csv/{0}.csv'.format(year)
json_file = 'json/{0}.json'.format(year)

main_json = {"nodes": [], "links": []}
section_json = defaultdict(lambda: {"nodes": [], "links": []})

container = {}
section_dict = {
    'left': {},
    'right': {}
}
municipality_dict = {
    'left': {},
    'right': {}
}
section_value = {
    'left': defaultdict(lambda: defaultdict(lambda: 0)),
    'right': defaultdict(lambda: defaultdict(lambda: 0))
}

node_counter = 0
section_node_counter = defaultdict(lambda: 0)

with open(csv_file, 'r') as f:
    lines = f.readlines()

header = lines[0].rstrip().split(',')
for i in range(2, len(header)):
    main_json["nodes"].append({"node": node_counter, "name": header[i], "side": "container"})
    container[header[i]] = node_counter
    node_counter += 1

for line in lines[1:]:
    parts =  line.rstrip().split(',')
    municipality = parts[0]
    section = parts[1]

    # if municipality not in [v["name"] for v in main_json["nodes"]] or municipality == section:
    #     has_left = has_right = False
    #     for _line in lines[1:]:
    #         _line = _line.rstrip().split(',')
    #         if section == _line[0]:
    #             numbers = [float(v) for v in _line[2:]]
    #             if min(numbers) < 0:
    #                 has_left = True
    #             if max(numbers) > 0:
    #                 has_right = True
    #             if has_left and has_right:
    #                 break
    #     if has_left:
    #         main_json["nodes"].append({"node": node_counter, "name": municipality})
    #         left_municipality[municipality] = node_counter
    #         node_counter += 1
    #     if has_right:
    #         main_json["nodes"].append({"node": node_counter, "name": municipality})
    #         right_municipality[municipality] = node_counter
    #         node_counter += 1

    if section not in [v["name"] for v in main_json["nodes"]]: # or municipality == section:
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
            main_json["nodes"].append({"node": node_counter, "name": section, "side": "left"})
            section_dict['left'][section] = node_counter
            node_counter += 1
        if has_right:
            main_json["nodes"].append({"node": node_counter, "name": section, "side": "right"})
            section_dict['right'][section] = node_counter
            node_counter += 1

for line in lines[1:]:
    parts =  line.rstrip().split(',')
    municipality = parts[0]
    section = parts[1]
    nodes = section_json[section]["nodes"]

    # if section not in [v["name"] for v in nodes]:
    #     nodes.append({"node": section_node_counter[section], "name":})

    if municipality not in [v["name"] for v in nodes]: # or municipality == section:
        has_left = has_right = False
        for _line in lines[1:]:
            _line = _line.rstrip().split(',')
            if municipality == _line[0]:
                numbers = [float(v) for v in _line[2:]]
                if min(numbers) < 0:
                    has_left = True
                if max(numbers) > 0:
                    has_right = True
                if has_left and has_right:
                    break
        if has_left:
            nodes.append({"node": section_node_counter[section], "name": municipality, "side": "left"})
            municipality_dict['left'][municipality] = section_node_counter[section]
            section_node_counter[section] += 1
        if has_right:
            nodes.append({"node": section_node_counter[section], "name": municipality, "side": "right"})
            municipality_dict['right'][municipality] = section_node_counter[section]
            section_node_counter[section] += 1

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
            main_json["links"].append({
                "source": section_dict['left'][section],
                "target": container[header[i]],
                "value": -section_value['left'][section][i]
            })
        if section_value['right'][section][i] != 0:
            main_json["links"].append({
                "source": container[header[i]],
                "target": section_dict['right'][section],
                "value": section_value['right'][section][i]
            })

for line in lines[1:]:
    parts =  line.rstrip().split(',')
    municipality = parts[0]
    section = parts[1]
    links = section_json[section]["links"]

    for i in range(2, len(header)):
        value = round(float(parts[i]), 2)
        # Left side, donator
        if value < 0:
            links.append({
                "source": municipality_dict['left'][municipality],
                "target": section_dict['left'][section],
                "value": -value
            })

        # Right side, receiver
        if value > 0:
            links.append({
                "source": section_dict['right'][section],
                "target": municipality_dict['right'][municipality],
                "value": value
            })
        # 0 values are getting ignored

json.dump(main_json, open(json_file, 'w'))
for side in section_dict.values():
    for name, node in side.items():
        json.dump(section_json[name], open('json/{0}_{1}.json'.format(year, node), 'w'))

