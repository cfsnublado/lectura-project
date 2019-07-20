import argparse
import json
import os
import sys

from bs4 import BeautifulSoup
from markdownify import markdownify as md
import markdown2
import requests

from base import get_mimetype, get_user_auth_token, print_color


'''
Usage: import_reading.py [-h] [--localhost] source

Required:
    source: path to reading file(s). If it's a directory, the files in its top level are processed.

Options:
    --localhost: if provided, the localhost api is called. Otherwise, the production api is called.
'''


def import_reading(token, filename):
    print_color(96, filename)

    with open(filename, 'r') as file:
        mimetype = get_mimetype(filename)

        if mimetype == 'application/json':
            data = json.load(file)
        elif mimetype == 'text/markdown':
            data = convert_markdown_to_dict(file.read())
        else:
            sys.exit('File must be json or markdown.')

    headers = {'Authorization': 'token {0}'.format(token)}

    requests.post(import_url, headers=headers, json=data)


def convert_markdown_to_dict(md_text, display_html=False):
    html = markdown2.markdown(md_text, extras=['metadata', 'markdown-in-html'])
    reading_data = {}
    project_data = {}

    if 'project_name' not in html.metadata:
        raise TypeError('Missing project_name attribute in metadata.')

    project_data['name'] = html.metadata['project_name']

    if 'reading_name' not in html.metadata:
        raise TypeError('Missing reading_name attribute in metadata.')

    reading_data['name'] = html.metadata['reading_name']

    if 'reading_audio_url' in html.metadata:
        reading_data['audio_url'] = html.metadata['source_type']

    if 'reading_description' in html.metadata:
        reading_data['description'] = html.metadata['reading_description']

    data_dict = {
        'project_data': project_data,
        'reading_data': reading_data
    }
    soup = BeautifulSoup(html, 'html.parser')

    if display_html:
        print_color(92, '\n\nReading html')
        print(soup.prettify())

    return data_dict


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Import reading json data.')
    parser.add_argument('--localhost', help='request from localhost', action='store_true')
    parser.add_argument('source', help='reading file or directory')
    args = parser.parse_args()
    localhost_base = 'http://127.0.0.1:8000'
    host_base = 'http://cfslectura.herokuapp.com'
    token_path = 'api/api-token-auth/'
    import_path = 'api/reading/reading/import/'

    if args.localhost:
        token_url = '{0}/{1}'.format(localhost_base, token_path)
        import_url = '{0}/{1}'.format(localhost_base, import_path)
    else:
        token_url = '{0}/{1}'.format(host_base, token_path)
        import_url = '{0}/{1}'.format(host_base, import_path)

    token = get_user_auth_token(token_url)

    if token:
        if os.path.isfile(args.source):
            import_reading(token, args.source)
        elif os.path.isdir(args.source):
            for root, dirs, files in os.walk(args.source):
                for file in files:
                    import_reading(token, os.path.join(root, file))
    else:
        sys.exit('Invalid login.')
