#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from collections import defaultdict

year = 2012
csv_file = 'csv/{0}.csv'.format(year)
json_file = 'json/{0}/main.json'.format(year)
json_format = 'json/{0}/{1}.json'

main_json = {'nodes': [], 'links': []}
nodes = main_json['nodes']
links = main_json['links']
node_counter = 0
lines = []
collection = {
    'left': defaultdict(lambda: {
        'municipalities': defaultdict(lambda: {}),
        'values': defaultdict(lambda: 0)
    }),
    'right':  defaultdict(lambda: {
        'municipalities': defaultdict(lambda: {}),
        'values': defaultdict(lambda: 0)
    }),
    'container': {}
}

with open(csv_file, 'r') as f:
    # 0 -> Disparitätenabbau
    # 1 -> Mindestausstattung
    # 2 -> Pauschale Abgeltung
    # 3 -> Geo-topo Zuschuss
    # 4 -> Sozio-demo Zuschuss
    container = f.readline().rstrip().split(',')[2:]

    for line in f.readlines():
        lines.append(line.rstrip().split(','))

### Containers to sections
# Containers
for i in range(len(container)):
    nodes.append({
        'node': node_counter,
        'name': container[i],
        'side': 'container',
        'type': 'container'
    })
    collection['container'][i] = node_counter
    node_counter += 1


# Sections
sections = set([v[1] for v in lines])
for section in sections:
    has_left = has_right = False

    for line in lines:
        if section == line[1]:
            numbers = [float(v) for v in line[2:]]
            if min(numbers) < 0:
                has_left = True
            if max(numbers) > 0:
                has_right = True

            for i in range(len(container)):
                value = round(float(line[i + 2]), 2)
                if value < 0:
                    collection['left'][section]['values'][i] += value
                if value > 0:
                    collection['right'][section]['values'][i] += value

    if has_left:
        collection['left'][section]['obj'] = {
            'node': 0,
            'name': section,
            'side': 'left',
            'type': 'section'
        }
    if has_right:
        collection['right'][section]['obj'] = {
            'node': 0,
            'name': section,
            'side': 'right',
            'type': 'section'
        }

# Add node values to the sections
for side in (collection['left'], collection['right']):
    for section in side.values():
        section['obj']['node'] = node_counter
        nodes.append(section['obj'])
        node_counter += 1

# Sections
for section in sections:
    for i in range(len(container)):
        if section in collection['left'] and \
                collection['left'][section]['values'][i] != 0:
            links.append({
                'source': collection['left'][section]['obj']['node'],
                'target': collection['container'][i],
                'value': -collection['left'][section]['values'][i]
            })

        if section in collection['right'] and \
                collection['right'][section]['values'][i] != 0:
            links.append({
                'source': collection['container'][i],
                'target': collection['right'][section]['obj']['node'],
                'value': collection['right'][section]['values'][i]
            })

json.dump(main_json, open(json_file, 'w'))

### Section to municipalities
# Municipalities
for line in lines:
    municipality = line[0]
    section = line[1]
    has_left = has_right = False

    for line in lines:
        if municipality == line[0]:
            numbers = [float(v) for v in line[2:]]
            if min(numbers) < 0:
                has_left = True
            if max(numbers) > 0:
                has_right = True
            break

    if has_left:
        collection['left'][section]['municipalities'][municipality]['values'] = numbers
        collection['left'][section]['municipalities'][municipality]['obj'] = {
            'node': 0,
            'name': municipality,
            'side': 'left',
            'type': 'municipality'
        }

    if has_right:
        collection['right'][section]['municipalities'][municipality]['values'] = numbers
        collection['right'][section]['municipalities'][municipality]['obj'] = {
            'node': 0,
            'name': municipality,
            'side': 'right',
            'type': 'municipality'
        }

# Sections and municipalities
for section in sections:
    section_json = {'nodes': [], 'links': []}
    nodes = section_json['nodes']
    links = section_json['links']
    node_counter = 0

    if not section in collection['right']:
        continue

    # Containers
    # for i in range(len(container)):
    #     nodes.append({
    #         'node': node_counter,
    #         'name': container[i],
    #         'side': 'container',
    #         'type': 'container'
    #     })
    #     collection['container'][i] = node_counter
    #     node_counter += 1

    # Section
    nodes.append({
        'node': node_counter,
        'name': collection['right'][section]['obj']['name'],
        'side': 'right',
        'type': 'section'
    })
    node_counter += 1

    # Municipalities
    for municipality in collection['right'][section]['municipalities'].values():
        nodes.append({
            'node': node_counter,
            'name': municipality['obj']['name'],
            'side': 'right',
            'type': 'municipality'
        })

        value = sum([v for v in municipality['values'] if v > 0])
        if value > 0:
            links.append({
                'source': 0,
                'target': node_counter,
                'value': value
            })
        node_counter += 1

    # Links between containers and sections
    # for i in range(len(container)):
    #     if collection['right'][section]['values'][i] != 0 and \
    #             municipality['values'][i] != 0:
    #         links.append({
    #             'source': collection['container'][i],
    #             'target': collection['right'][section]['obj']['node'],
    #             'value': collection['right'][section]['values'][i]
    #         })

    json.dump(section_json, open(json_format.format(year,
        collection['right'][section]['obj']['node']), 'w'))
