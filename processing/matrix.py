# -*- coding: utf-8 -*-

import json, csv
from collections import defaultdict

year = 2012
csv_file = 'csv/{0}.csv'.format(year)
json_file = 'json/matrix_{0}.json'.format(year)
csv_file_sections = 'json/sections_{0}.csv'.format(year)

matrix = []
sections = {}
pots = []
totals = None

with open(csv_file, 'r') as f:
    lines = f.readlines()

headers = lines[0].rstrip().split(',')
for header in headers[2:]:
    pots.append(header)

for line in lines[1:]:
    parts =  line.rstrip().split(',')
    municipality = parts[0]
    section = parts[1]
    
    if section not in sections:
        sections[section] = [0 for part in parts[2:]]
    
    if totals == None:
        totals = [0 for part in parts[2:]]
    
    i = 0
    for part in parts[2:]:
        
        value = float(part)
        
        sections[section][i] += value
        
        if value > 0:
            totals[i] += value
        
        i = i + 1

print pots
print sections

i = 0
for pot in pots:
    
    row = []
    
    for pot in pots:
        row.append(0)
    
    for section, data in sections.items():
        
        if data[i] > 0:
            row.append(data[i])
        else:
            row.append(0)
    
    matrix.append(row)
    
    i = i + 1

for section, data in sections.items():
    
    row = []
    
    sum = 0
    i = 0
    for part in data:
        if data[i] < 0:
            row.append(-data[i])
        else:
            row.append(0)
        i = i + 1
    
    for sub_section, sub_data in sections.items():
        
        row.append(0)
    
    matrix.append(row)

json.dump(matrix, open(json_file, 'w'))

out = csv.writer(open(csv_file_sections, 'w'), delimiter=',', quoting=csv.QUOTE_ALL)
out.writerow(['name', 'type'])
for pot in pots:
    out.writerow([pot, "pot"])
for section in sections.keys():
    out.writerow([section, "section"])
