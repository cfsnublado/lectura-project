import argparse
import json
import os
import sys

import markdown2
import requests

from base import get_mimetype, get_user_auth_token, print_color


'''
Usage: import_post.py [-h] [--localhost] source

Required:
    source: path to post file(s). If it's a directory, the files in its top level are processed.

Options:
    --localhost: if provided, the localhost api is called. Otherwise, the production api is called.
'''

LOCALHOST = 'http://127.0.0.1:8000'
PRODUCTION_HOST = 'http://cfslectura.herokuapp.com'
TOKEN_PATH = 'api/api-token-auth/'
IMPORT_PATH = 'api/reading/post/import/'


def import_post(token, filename):
    with open(filename, 'r') as file:
        mimetype = get_mimetype(filename)

        if mimetype == 'application/json':
            data = json.load(file)
        elif mimetype == 'text/markdown':
            markdown = file.read()
            data = markdown_to_dict(markdown)
        else:
            sys.exit('File must be json or markdown.')

    headers = {'Authorization': 'token {0}'.format(token)}

    requests.post(import_url, headers=headers, json=data)
    print_color(96, filename)


def strip_markdown_metadata(s):
    start = s.find('---')
    end = len(s) - s[::-1].find('---')
    return s[start:end]


def markdown_to_dict(md_text, display_html=False):
    markdown_metadata = strip_markdown_metadata(md_text)
    html = markdown2.markdown(markdown_metadata, extras=['metadata', 'markdown-in-html'])
    post_data = {}
    project_data = {}

    if 'project_name' not in html.metadata:
        raise TypeError('Missing project_name attribute in metadata.')

    project_data['name'] = html.metadata['project_name']

    if 'post_name' not in html.metadata:
        raise TypeError('Missing post_name attribute in metadata.')

    post_data['name'] = html.metadata['post_name']

    if 'post_description' in html.metadata:
        post_data['description'] = html.metadata['post_description']

    post_data['content'] = md_text.replace(markdown_metadata, '')

    data_dict = {
        'project': project_data,
        'post': post_data
    }

    return data_dict


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Import post json or markdown data.')
    parser.add_argument('--localhost', help='request from localhost', action='store_true')
    parser.add_argument('source', help='post file or directory')
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
            import_post(token, args.source)
        elif os.path.isdir(args.source):
            for root, dirs, files in os.walk(args.source):
                for file in files:
                    import_post(token, os.path.join(root, file))
    else:
        sys.exit('Invalid login.')
