import json

data_file = 'csv/2012.csv'

output_json = {
    "nodes": [],
    "links": []
}

left_municipality = {}
left_section = {}
container = {}
right_section = {}
right_municipality = {}

node_counter = 0

with open(data_file, 'r') as f:
    header = f.readline().rstrip().split(',')
    for i in range(2, len(header)):
        output_json["nodes"].append({"node": node_counter, "name": header[i]})
        container[header[i]] = node_counter
        node_counter += 1

    for line in f.readlines():
        parts =  line.rstrip().split(',')
        municipality = parts[0]
        section = parts[1]
        if section not in [v["name"] for v in output_json["nodes"]]:
            output_json["nodes"].append({"node": node_counter, "name": section})
            left_section[section] = node_counter
            node_counter += 1
            output_json["nodes"].append({"node": node_counter, "name": section})
            right_section[section] = node_counter
            node_counter += 1

        for i in range(2, len(header)):
            value = round(float(parts[i]), 2)
            # Left side, donator
            if value < 0:
                output_json["links"].append({
                    "source": left_section[parts[1]],
                    "target": container[header[i]],
                    "value": -value
                })

            # Right side, receiver
            if value > 0:
                output_json["links"].append({
                    "source": container[header[i]],
                    "target": right_section[parts[1]],
                    "value": value
                })
            # 0 values are getting ignored

json.dump(output_json, open('out.json', 'w'))
