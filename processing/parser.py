import json

data_file = 'csv/2012.csv'

output_json = {
    "nodes": [],
    "links": []
}

header_labels = {}  # middle
in_labels = {}  # left side
out_labels = {}  # right side

nr_of_buckets = 5
node_counter = 0

with open(data_file, 'r') as f:
    header = f.readline().rstrip().split(',')[2:]
    for i in range(0, len(header)):
        output_json["nodes"].append({"node": node_counter, "name": header[i]})
        header_labels[header[i]] = node_counter
        node_counter += 1

    for line in f.readlines():
        line = line.rstrip()
        parts = line.split(',')
        region = parts[0]  # Verwaltungskreis
        # section = parts[1]  # Gemeinde
        if region not in [v["name"] for v in output_json["nodes"]]:
            output_json["nodes"].append({"node": node_counter, "name": region})
            in_labels[region] = node_counter
            node_counter += 1
            output_json["nodes"].append({"node": node_counter, "name": region})
            out_labels[region] = node_counter
            node_counter += 1

        for i in range(2,7):
            value = float(parts[i])
            if value < 0:  # Left side, donator
                output_json["links"].append({
                    "source": in_labels[parts[0]],
                    "target": header_labels[header[i-2]],
                    "value": -value
                })

            if value > 0:  # Right side, receiver
                output_json["links"].append({
                    "source": header_labels[header[i-2]],
                    "target": out_labels[parts[0]],
                    "value": value
                })

json.dump(output_json, open('out.json', 'w'))
