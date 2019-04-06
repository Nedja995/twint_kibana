import sys
import argparse
import datetime
from string import Template
import uuid
import json

# Template file
tweets_visualizations = "elasticsearch/visualizations_tweets.json"
# Template ids
id_kibana_index_pattern = "17423e10-356f-11e9-8683-53ee6dcae892"
id_dashboard = "65ce205a-3566-11e9-9d70-681729ad18c6"
dashboard_title = "<DASBOARD TITLE>"
index_name = "<INDEX NAME>"
#visualization
visualizations_id = [
    "65ce2055-3566-11e9-9d70-681729ad18c6",
    "f270ccf0-3a0f-11e9-a646-5f29877560c2",
    "65ce2056-3566-11e9-9d70-681729ad18c6",
    "65ce2059-3566-11e9-9d70-681729ad18c6",
    "f0a7edd0-356f-11e9-8683-53ee6dcae892",
    "65ce2052-3566-11e9-9d70-681729ad18c6",
    "52ab0430-4abb-11e9-b349-33592a2dd62f",
    "65ce2053-3566-11e9-9d70-681729ad18c6",
    "65ce2057-3566-11e9-9d70-681729ad18c6",
    "65ce2058-3566-11e9-9d70-681729ad18c6",
    "65ce2054-3566-11e9-9d70-681729ad18c6"
]


def main(name, kibana_index):
    print("\nGenerate Kibana visualizations.")
    print("ES index: {}".format(kibana_index))

    new_visualizations_id = [str(uuid.uuid1()) for x in range(len(visualizations_id))]
    dict_final = dict(zip(visualizations_id, new_visualizations_id))

    new_dashboard_id = str(uuid.uuid1())
    dict_final[id_kibana_index_pattern] = kibana_index
    dict_final[id_dashboard] = new_dashboard_id
    dict_final[dashboard_title] = name
    dict_final[index_name] = name

    filein = open(tweets_visualizations)

    template = filein.read()
    result = template
    for k,v in dict_final.items():
        result = result.replace(k, v)

    #print(result)

    outfile = 'visualizations_' + name + '.json'
    print("Output file: " + outfile)
    with open(outfile, 'w') as outfile:
        outfile.write(result)
    print("Generating finished.")


def lsplit(str, prefix):
    if str.startswith(prefix):
        return str[len(prefix)+1:]
    return str


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Generate visualization for Kibana",
        epilog="As an alternative to the commandline, params can be placed in a file, one per line, and specified on the commandline like '%(prog)s @params.conf'.",
        fromfile_prefix_chars='@')
    parser.add_argument(
        "index",
        help="pass Kibana Index Pattern to the program")
    parser.add_argument(
        "-n",
        "--name",
        help="pass name of Kibana Index Pattern to the program")
    parser.add_argument(
        "-v",
        "--verbose",
        help="increase output verbosity",
        action="store_true")
    args = parser.parse_args()

    # args.index = args.index.split()[1]
    kibana_index = lsplit(args.index, 'index')
    
    if args.name != None:
        name = lsplit(args.name, 'name')
    else:
        name = args.index

    main(name, kibana_index)

    

