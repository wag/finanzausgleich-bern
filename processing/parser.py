#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from collections import defaultdict

year = 2012
csv_file = 'csv/{0}.csv'.format(year)
json_file = 'json/{0}.json'.format(year)

main_json = {"nodes": [], "links": []}
nodes = main_json["nodes"]
links = main_json["links"]
node_counter = 0

values = []
container_dict = {}
section_dict = {
    'left': {},
    'right': {}
}
section_amount = {
    'left': defaultdict(lambda: defaultdict(lambda: 0)),
    'right': defaultdict(lambda: defaultdict(lambda: 0))
}

with open(csv_file, 'r') as f:
    # 0 -> Disparitätenabbau
    # 1 -> Mindestausstattung
    # 2 -> Pauschale Abgeltung
    # 3 -> Geo-topo Zuschuss
    # 4 -> Sozio-demo Zuschuss
    container = f.readline().rstrip().split(',')[2:]

    for line in f.readlines():
        values.append(line.rstrip().split(','))

# Add the containers to the nodes
for i in range(len(container)):
    nodes.append({
        "node": node_counter,
        "name": container[i],
        "side": "container"
    })
    container_dict[container[i]] = node_counter
    node_counter += 1

# Add the sections to the nodes, make a distinction between
# donators (left side) and receivers (right side).
# Omit them, if the don't donate or receive any money.
sections = set([v[1] for v in values])
for section in sections:
    has_left = has_right = False
    for line in values:
        if section == line[1]:
            numbers = [float(v) for v in line[2:]]
            if min(numbers) < 0:
                has_left = True
            if max(numbers) > 0:
                has_right = True

            for i in range(len(container)):
                value = round(float(line[i + 2]), 2)
                if value < 0:
                    section_amount['left'][section][i] += value
                if value > 0:
                    section_amount['right'][section][i] += value

    if has_left:
        nodes.append({
            "node": node_counter,
            "name": section,
            "side": "left"
        })
        section_dict['left'][section] = node_counter
        node_counter += 1
    if has_right:
        nodes.append({
            "node": node_counter,
            "name": section,
            "side": "right"
        })
        section_dict['right'][section] = node_counter
        node_counter += 1

# Add the municipalities to the nodes, make a distinction between
# donators (left side) and receivers (right side).
# Omit them, if the don't donate or receive any money.

# Add the links between the containers, the left and right sections
# Omit them, if the don't donate or receive any money.
for section in sections:
    for i in range(len(container)):
        if section in section_dict['left'] and \
                section_amount['left'][section][i] != 0:
            links.append({
                "source": section_dict['left'][section],
                "target": container_dict[container[i]],
                "value": -section_amount['left'][section][i]
            })

        if section in section_dict['right'] and \
                section_amount['right'][section][i] != 0:
            links.append({
                "source": container_dict[container[i]],
                "target": section_dict['right'][section],
                "value": section_amount['right'][section][i]
            })

json.dump(main_json, open(json_file, 'w'))
