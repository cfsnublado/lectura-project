import argparse
import json
import os
import sys

import requests

from base import get_user_auth_token, print_color


def export_readings(token, output_path):
    file_path = os.path.join(output_path, 'readings.json')
    print_color(96, file_path)

    with open(file_path, 'w+') as f:
        headers = {
            'Authorization': 'token {0}'.format(token)
        }
        response = requests.get(export_url, headers=headers)
        json_data = response.json()
        f.write(json.dumps(json_data, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Export reading json data.")
    parser.add_argument("--localhost", help="request from localhost", action="store_true")
    parser.add_argument("output_path", help="output path")
    args = parser.parse_args()
    localhost_base = "http://127.0.0.1:8000"
    host_base = "http://cfslectura.herokuapp.com"
    token_path = "api/api-token-auth/"
    export_path = "api/vocab/readings/export/"

    if args.localhost:
        token_url = "{0}/{1}".format(localhost_base, token_path)
        export_url = "{0}/{1}".format(localhost_base, export_path)
    else:
        token_url = "{0}/{1}".format(host_base, token_path)
        export_url = "{0}/{1}".format(host_base, export_path)

    token = get_user_auth_token(token_url)

    if token:
        export_entries(token, args.output_path)
    else:
        sys.exit("Invalid login.")