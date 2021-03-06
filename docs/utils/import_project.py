import argparse
import json
import os
import sys

import requests

from base import get_mimetype, get_user_auth_token, print_color


'''
Usage: import_project.py [-h] [--localhost] source

Required:
    source: path to project file(s). If it's a directory, the files in its top level are processed.

Options:
    --localhost: if provided, the localhost api is called. Otherwise, the production api is called.
'''

LOCALHOST = 'http://127.0.0.1:8000'
PRODUCTION_HOST = 'https://cfslectura.herokuapp.com'
TOKEN_PATH = 'api/api-token-auth/'
IMPORT_PATH = 'api/reading/project/import/'


def import_project(token, filename):
    with open(filename, 'r') as file:
        mimetype = get_mimetype(filename)

        if mimetype == 'application/json':
            data = json.load(file)
        else:
            sys.exit('File must be json.')

    headers = {'Authorization': 'token {0}'.format(token)}

    requests.post(import_url, headers=headers, json=data)
    print_color(96, filename)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Import project json data.')
    parser.add_argument('--localhost', help='request from localhost', action='store_true')
    parser.add_argument('source', help='project file or directory')
    args = parser.parse_args()

    if args.localhost:
        token_url = '{0}/{1}'.format(LOCALHOST, TOKEN_PATH)
        import_url = '{0}/{1}'.format(LOCALHOST, IMPORT_PATH)
    else:
        token_url = '{0}/{1}'.format(PRODUCTION_HOST, TOKEN_PATH)
        import_url = '{0}/{1}'.format(PRODUCTION_HOST, IMPORT_PATH)

    token = get_user_auth_token(token_url)

    if token:
        if os.path.isfile(args.source):
            import_project(token, args.source)
        elif os.path.isdir(args.source):
            for root, dirs, files in os.walk(args.source):
                for file in files:
                    import_project(token, os.path.join(root, file))
    else:
        sys.exit('Invalid login.')
