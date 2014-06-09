# -*- coding: utf-8 -*-

from flask import Flask, request

app = Flask(__name__)
app.config['DEBUG'] = True


@app.route('/')
def index():
    return 'index'


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