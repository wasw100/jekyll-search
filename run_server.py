# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify
from git import Repo

app = Flask(__name__)
app.config.from_object('settings')


@app.route('/')
def index():
    return 'index'


@app.route('/git-pull')
def git_pull():
    repo_path = app.config['LOCAL_REPO_PATH']
    repo = Repo(repo_path)
    origin = repo.remotes.origin
    pull_result = origin.pull()
    return jsonify(code=0, data=pull_result)


@app.route('/create_index')
def create_index():
    return 'create index'


@app.route('/query')
def query():
    q = request.args.get('q')
    if not q:
        return 'not query str'
    return 'query'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8887)