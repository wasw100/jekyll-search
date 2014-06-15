# -*- coding: utf-8 -*-

import json, re

from flask import Flask, request, jsonify, render_template
from git import Repo
from index import build_index
from search import query

app = Flask(__name__)
app.config.from_object('settings')


@app.route('/')
def index():
    return 'index'


@app.route('/git-pull')
def git_pull():
    """git pull"""
    repo_path = app.config['LOCAL_REPO_PATH']
    repo = Repo(repo_path)
    origin = repo.remotes.origin
    pull_result = origin.pull()
    return jsonify(code=0, data=pull_result)


@app.route('/create-index')
def create_index():
    build_index()
    return 'create index'


FILENAME_PATTERN = re.compile(r'\d+-\d+-\d+-(.+)\.md')

@app.route('/search')
def search():
    q = request.args.get('q')
    if not q:
        return 'not query str'
    items = query(q)
    return render_template('search.html', items=items)

    # return 'query-%s' % q


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8887)